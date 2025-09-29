# Import the 'requests' library to make HTTP requests (used to fetch data from the SEC)
import requests
# Define a class called CIKLookup
class CIKLookup:
    # The constructor method: runs automatically when an object of this class is created
    def __init__(self):
        # Dictionary to store CIK data using the company name as the key
        self.name_dict = {}
        # Dictionary to store CIK data using the stock ticker as the key
        self.ticker_dict = {}
        # URL to the SEC's JSON file that contains the mapping of companies to their CIKs
        self.url = "https://www.sec.gov/files/company_tickers.json"
        # Call the helper method to download and store the data
        self._load_data()

    # Private method to download SEC data and populate the dictionaries
    def _load_data(self):
        # Send an HTTP GET request to the SEC URL with a custom User-Agent (required by SEC)
        response = requests.get(
            self.url,
            headers={"User-Agent": "MLT Student Contact kidusyosef81@gmail.com"}
        )

        # If the request fails (not 200 OK), raise an error
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from SEC: {response.status_code}")

        # Parse the JSON response into a Python dictionary
        data = response.json()

        # Loop through each company's data in the response
        for entry in data.values():
            # Convert the CIK number to a string and pad it with leading zeros to be 10 digits
            cik_str = str(entry["cik_str"]).zfill(10)
            # Get the company name and convert it to lowercase for consistent lookup
            name = entry["title"].lower()
            # Get the ticker symbol and convert it to lowercase for consistent lookup
            ticker = entry["ticker"].lower()

            # Store the CIK info in name_dict with the lowercase company name as the key
            self.name_dict[name] = (cik_str, entry["title"], entry["ticker"])
            # Store the CIK info in ticker_dict with the lowercase ticker as the key
            self.ticker_dict[ticker] = (cik_str, entry["title"], entry["ticker"])

    # Method to look up a company's CIK using its name
    def name_to_cik(self, company_name):
        # Convert the input to lowercase and return the tuple from the name_dict
        return self.name_dict.get(company_name.lower(), None)

    # Method to look up a company's CIK using its stock ticker
    def ticker_to_cik(self, ticker):
        # Convert the input to lowercase and return the tuple from the ticker_dict
        return self.ticker_dict.get(ticker.lower(), None)

class SECFilings:
    def __init__(self, user_agent):
        self.headers = {"User-Agent": user_agent}


    def _get_submission_data(self, cik):
        padded_cik = str(cik).zfill(10)   # -> "0000320193"
        url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
        headers = {"User-Agent": "Kidus Assefa kidusyosef81@gmail.com"}
        print("DEBUG: fetching submissions URL:", url)  # helpful debug
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            body_snippet = (response.text[:200] + "...") if response.text else ""
            raise Exception(
            f"Failed to fetch submission data: {response.status_code} for URL {url}. "
            f"Response snippet: {body_snippet}"
        )
        return response.json()
    


    def _find_filing(self, data, form_type, year=None, quarter=None):
        recent_filings = data["filings"]["recent"]
        forms = recent_filings["form"]
        accession_numbers = recent_filings["accessionNumber"]
        primary_docs = recent_filings["primaryDocument"]
        filing_dates = recent_filings["filingDate"]

        for i in range(len(forms)):
            if forms[i] != form_type:
                continue
            if year and int(filing_dates[i][:4]) != year:
                continue
            if quarter:
                month = int(filing_dates[i][5:7])
                if (quarter == 1 and month not in [1, 2, 3]) or \
                   (quarter == 2 and month not in [4, 5, 6]) or \
                   (quarter == 3 and month not in [7, 8, 9]) or \
                   (quarter == 4 and month not in [10, 11, 12]):
                    continue

            acc_no = accession_numbers[i].replace("-", "")
            cik = data["cik"]
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no}/{primary_docs[i]}"
            return doc_url

        return None

    def annual_filing(self, cik, year=None):
        data = self._get_submission_data(cik)
        return self._find_filing(data, "10-K", year=year)

    def quarterly_filing(self, cik, year=None, quarter=None):
        data = self._get_submission_data(cik)
        return self._find_filing(data, "10-Q", year=year, quarter=quarter)

