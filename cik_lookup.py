# Import the 'requests' library to make HTTP requests (used to fetch data from the SEC)
import requests
import requests  # Library for making HTTP requests to web APIs
from markdownify import markdownify as md  # Library to convert HTML to markdown format
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents


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




class SecEdgar:
    def __init__(self, fileurl):
        # Initialize the class with the SEC company tickers JSON URL
        self.fileurl = fileurl  # Store the URL to the SEC company tickers file
        self.namedict = {}  # Dictionary to store company name -> CIK mappings
        self.tickerdict = {}  # Dictionary to store ticker symbol -> CIK mappings
        
        # Set up headers with user identification (required by SEC)
        headers = {"user-agent": "Kidus Assefa kidusyosef81@gmail.com"}
        # Make HTTP request to get the company tickers JSON file from SEC
        r = requests.get(self.fileurl, headers=headers)
        
        # Parse the JSON response into a Python dictionary
        self.filejson = r.json()
        
        # Debug prints to see what we received
        print(r.text)  # Print the raw response text
        print(self.filejson)  # Print the parsed JSON data
        print(type(self.filejson))  # Print the data type
        
        # Loop through each company entry in the JSON data
        for entry in self.filejson.values():
            # Store company info in namedict using company title as key
            # Value is tuple: (CIK, company name, ticker symbol)
            self.namedict[entry['title']] = (entry['cik_str'], entry['title'], entry['ticker'])
            
            # Store company info in tickerdict using ticker symbol as key
            # Value is tuple: (CIK, company name, ticker symbol)
            self.tickerdict[entry['ticker']] = (entry['cik_str'], entry['title'], entry['ticker'])
    
    def name_to_cik(self, title):
        # Function to look up company CIK using company name
        if title not in self.namedict:  # Check if company name exists in our data
            return "Not found"  # Return error message if not found
        return self.namedict[title]  # Return the tuple (CIK, name, ticker) if found
    
    def ticker_to_cik(self, ticker):
        # Function to look up company CIK using ticker symbol
        if ticker not in self.tickerdict:  # Check if ticker exists in our data
            return "Not found"  # Return error message if not found
        return self.tickerdict[ticker]  # Return the tuple (CIK, name, ticker) if found
    
    def _get_filing_content(self, url):
        # Private method to fetch the actual content of a SEC filing document
        # Takes a URL and returns the HTML content of that document
        headers = {"user-agent": "Kidus Assefa kidusyosef81@gmail.com"}  # Required SEC header
        
        # Add delay to respect SEC rate limits
        import time
        time.sleep(0.1)
        
        try:
            response = requests.get(url, headers=headers, timeout=15)  # Make HTTP request to get document
            if response.status_code == 200:
                return response.text  # Return the raw HTML content of the document
            else:
                print(f"ERROR: Failed to fetch document, status: {response.status_code}")
                return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def _clean_filing_content(self, html_content):
        # Private method to convert HTML to clean, readable text
        if not html_content:
            return None
            
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines and join into single string
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return clean_text
    
    def _get_submissions_data(self, cik):
        # Private method to get all filing submissions data for a company
        # Takes a CIK and returns the recent filings data from SEC API
        
        # Make sure CIK is properly formatted (10 digits with leading zeros)
        padded_cik = str(cik).zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
        headers = {"user-agent": "Kidus Assefa kidusyosef81@gmail.com"}
        
        print(f"DEBUG: Requesting URL: {url}")  # Debug info
        
        # Add delay to respect SEC rate limits (10 requests per second max)
        import time
        time.sleep(0.1)
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"DEBUG: Response status: {response.status_code}")  # Debug info
            
            if response.status_code != 200:
                print(f"ERROR: SEC API returned status {response.status_code}")
                print(f"Response text: {response.text[:200]}")
                return None
            
            data = response.json()  # Parse JSON response
            return data['filings']['recent']  # Return only the recent filings section
            
        except requests.exceptions.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON response from SEC API")
            print(f"Response text: {response.text[:200]}")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def annual_filing(self, cik, year):
        # Function to get the content of a 10-K annual filing for a specific year
        # Takes company CIK and year, returns the actual document content
        filings_recent = self._get_submissions_data(cik)  # Get all recent filings for this company
        
        # Check if we got valid data
        if filings_recent is None:
            return "Error: Could not retrieve filing data from SEC"
        
        # Loop through all the filings to find the right 10-K for the specified year
        for i in range(len(filings_recent['form'])):
            form = filings_recent['form'][i]  # Get the form type (10-K, 10-Q, etc.)
            if form == "10-K":  # Check if this is an annual report (10-K)
                date = filings_recent['filingDate'][i]  # Get the filing date
                if date.startswith(str(year)):  # Check if filing is from the requested year
                    # Extract the accession number and remove dashes for URL formatting
                    accession = filings_recent['accessionNumber'][i].replace("-", "")
                    # Get the primary document filename
                    document = filings_recent['primaryDocument'][i]
                    # Build the complete URL to the SEC document
                    file_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
                    # Fetch and return the actual document content (not just the URL)
                    content = self._get_filing_content(file_url)
                    return content
        
        # If no 10-K found for that year, return error message
        return "No 10-K found for that year"
    
    def quarterly_filing(self, cik, year, quarter):
        # Function to get the CLEAN TEXT content of a 10-Q quarterly filing for a specific year and quarter
        # Takes company CIK, year, and quarter (1,2,3,4), returns the actual document content as readable text
        filings_recent = self._get_submissions_data(cik)  # Get all recent filings for this company
        
        # Check if we got valid data
        if filings_recent is None:
            return "Error: Could not retrieve filing data from SEC"
        
        # Loop through all the filings to find the right 10-Q for the specified year and quarter
        for i in range(len(filings_recent['form'])):
            form = filings_recent['form'][i]  # Get the form type (10-K, 10-Q, etc.)
            if form == "10-Q":  # Check if this is a quarterly report (10-Q)
                date = filings_recent['filingDate'][i]  # Get the filing date
                if date.startswith(str(year)):  # Check if filing is from the requested year
                    # Extract the month from the filing date to determine which quarter
                    month = int(date.split("-")[1])  # Split date and get month number
                    
                    # Determine which quarter this filing belongs to based on month
                    if month in [1,2,3]:  # January, February, March = Q1
                        this_quarter = 1
                    elif month in [4,5,6]:  # April, May, June = Q2
                        this_quarter = 2
                    elif month in [7,8,9]:  # July, August, September = Q3
                        this_quarter = 3
                    elif month in [10,11,12]:  # October, November, December = Q4
                        this_quarter = 4
                    
                    # Check if this filing matches the requested quarter
                    if this_quarter == quarter:
                        # Extract the accession number and remove dashes for URL formatting
                        accession = filings_recent['accessionNumber'][i].replace("-", "")
                        # Get the primary document filename
                        document = filings_recent['primaryDocument'][i]
                        # Build the complete URL to the SEC document
                        file_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
                        # Fetch the HTML content
                        html_content = self._get_filing_content(file_url)
                        # Convert HTML to clean readable text and return it
                        clean_content = self._clean_filing_content(html_content)
                        return clean_content
        
        # If no 10-Q found for that year and quarter, return error message
        return "No 10-Q found for that year"

# Example usage - Create an instance of SecEdgar with the SEC company tickers URL
sec = SecEdgar('https://www.sec.gov/files/company_tickers.json')

# Test the ticker lookup function with NVIDIA
print(sec.ticker_to_cik('NVDA'))

# Test the company name lookup function with Apple
print(sec.name_to_cik('Apple Inc'))

# Test the company name lookup function with Amazon
print(sec.name_to_cik('AMAZON COM INC'))

# Get Apple's 2024 annual filing content (CIK 320193 is Apple's identifier)
print(sec.annual_filing(320193, 2024))

# Get Apple's Q3 2024 quarterly filing content
print(sec.quarterly_filing(320193, 2024, 3))