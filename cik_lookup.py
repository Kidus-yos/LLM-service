import requests  # lets Python make HTTP requests (to download data from the SEC website)

class SecEdgar:
    def __init__(self, fileurl):
        # It takes fileurl (the SEC data URL) as an input and sets up the object.
        self.fileurl = fileurl  # instance variable that stores the SEC file URL
        self.namedict = {}      # instance variable is a dictionary you’ll use to look up by company name
        self.tickerdict = {}    # instance variable you’ll use to look up by ticker symbol

        headers = {
            'user-agent': 'MLT asse4874@stthomas.edu'
        }

        # Sends a GET request to the SEC to download the JSON file using the headers above.
        r = requests.get(self.fileurl, headers=headers)

        # Parses the response as JSON and saves it to filejson
        self.filejson = r.json()

        # Debugging output (optional)
        print(r.text)
        print(self.filejson)

        # Calls another method (defined below) to process the JSON and populate your namedict and tickerdict
        self.cik_json_to_dict()

    def cik_json_to_dict(self):
        # This method processes the JSON data and populates the name and ticker dictionaries.
        # Reset the name and ticker dictionaries to start fresh before filling them.
        self.name_dict = {}
        self.ticker_dict = {}

# Run the code
se = SecEdgar("https://www.sec.gov/files/company_tickers.json")  # Initializes lookup dictionaries 
