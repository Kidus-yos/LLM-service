# Import the 'requests' library to make HTTP requests (used to fetch data from the SEC)
import requests
import requests  # Library for making HTTP requests to web APIs
from markdownify import markdownify as md  # Library to convert HTML to markdown format
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents


class CIKLookup:
    def __init__(self):
        self.name_dict = {}
        self.ticker_dict = {}
        self.url = "https://www.sec.gov/files/company_tickers.json"
        self.__load_data()
    
    def __load_data(self):
        """Private method to download SEC data and populate the dictionaries"""
        response = requests.get(
            self.url,
            headers={"User-Agent": "MLT Student Contact kidusyosef81@gmail.com"}
        )
        
        data = response.json()
        
        # Populate dictionaries
        for entry in data.values():
            company_name = entry['title']
            ticker = entry['ticker']
            cik = str(entry['cik_str']).zfill(10)  # Pad CIK to 10 digits
            
            self.name_dict[company_name] = cik
            self.ticker_dict[ticker] = cik
    
    def get_cik_by_name(self, company_name):
        """Get CIK by company name"""
        return self.name_dict.get(company_name)
    
    def get_cik_by_ticker(self, ticker):
        """Get CIK by stock ticker"""
        return self.ticker_dict.get(ticker.upper())
    
    def __get_submissions(self, cik):
        """Private method to get all submissions for a CIK"""
        # Ensure CIK is 10 digits
        cik_padded = str(cik).zfill(10)
        
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
        response = requests.get(
            url,
            headers={"User-Agent": "MLT Student Contact kidusyosef81@gmail.com"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch submissions for CIK {cik_padded}")
    
    def __find_filing(self, cik, form_type, year, quarter=None):
        """Private helper method to find a specific filing"""
        submissions = self.__get_submissions(cik)
        
        # Get the recent filings data
        recent = submissions.get('filings', {}).get('recent', {})
        
        # Extract arrays
        forms = recent.get('form', [])
        filing_dates = recent.get('filingDate', [])
        accession_numbers = recent.get('accessionNumber', [])
        primary_documents = recent.get('primaryDocument', [])
        
        # Search through filings
        for i in range(len(forms)):
            if forms[i] == form_type:
                filing_date = filing_dates[i]
                filing_year = int(filing_date.split('-')[0])
                
                # Check if year matches
                if filing_year == year:
                    # For quarterly, also check quarter
                    if quarter is not None:
                        filing_month = int(filing_date.split('-')[1])
                        # Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec
                        filing_quarter = (filing_month - 1) // 3 + 1
                        
                        if filing_quarter != quarter:
                            continue
                    
                    # Build the document URL
                    # Remove dashes from accession number for URL
                    accession_clean = accession_numbers[i].replace('-', '')
                    cik_clean = str(cik).lstrip('0')  # Remove leading zeros for URL
                    
                    document_url = (
                        f"https://www.sec.gov/Archives/edgar/data/"
                        f"{cik_clean}/{accession_clean}/{primary_documents[i]}"
                    )
                    
                    return {
                        'form': forms[i],
                        'filing_date': filing_dates[i],
                        'accession_number': accession_numbers[i],
                        'primary_document': primary_documents[i],
                        'document_url': document_url
                    }
        
        return None
    
    def annual_filing(self, cik, year):
        """
        Get the 10-K annual filing for a company in a specific year
        
        Args:
            cik: Company CIK number (string or int)
            year: Year of the filing (int)
            
        Returns:
            Dictionary with filing information including document URL
        """
        return self.__find_filing(cik, '10-K', year)
    
    def quarterly_filing(self, cik, year, quarter):
        """
        Get the 10-Q quarterly filing for a company
        
        Args:
            cik: Company CIK number (string or int)
            year: Year of the filing (int)
            quarter: Quarter number (1, 2, 3, or 4)
            
        Returns:
            Dictionary with filing information including document URL
        """
        if quarter not in [1, 2, 3, 4]:
            raise ValueError("Quarter must be 1, 2, 3, or 4")
        
        return self.__find_filing(cik, '10-Q', year, quarter)


# Example usage
if __name__ == "__main__":
    # Initialize the lookup
    lookup = CIKLookup()
    
    # Get Apple's CIK
    apple_cik = lookup.get_cik_by_ticker("AAPL")
    print(f"Apple CIK: {apple_cik}")
    
    # Get Apple's 2023 annual filing (10-K)
    print("\n=== Annual Filing (10-K) ===")
    annual = lookup.annual_filing(apple_cik, 2023)
    if annual:
        print(f"Form: {annual['form']}")
        print(f"Filing Date: {annual['filing_date']}")
        print(f"Document URL: {annual['document_url']}")
    else:
        print("No 10-K found for 2023")
    
    # Get Apple's Q2 2023 quarterly filing (10-Q)
    print("\n=== Quarterly Filing (10-Q) ===")
    quarterly = lookup.quarterly_filing(apple_cik, 2023, 2)
    if quarterly:
        print(f"Form: {quarterly['form']}")
        print(f"Filing Date: {quarterly['filing_date']}")
        print(f"Document URL: {quarterly['document_url']}")
    else:
        print("No 10-Q found for Q2 2023")