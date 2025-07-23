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
       
sec = CIKLookup()
print(sec.name_to_cik("apple inc."))
print(sec.ticker_to_cik("msft"))