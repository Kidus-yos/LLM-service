# test_sec.py
from cik_lookup import CIKLookup, SECFilings

def main():
    # initialize lookup (this fetches company_tickers.json from SEC)
    print("Initializing CIKLookup (this may call SEC)...")
    cik_lookup = CIKLookup()

    # try by ticker and by name
    print("Lookup by ticker 'AAPL':", cik_lookup.ticker_to_cik("AAPL"))
    print("Lookup by name 'Apple Inc.':", cik_lookup.name_to_cik("apple inc."))

    # pick a CIK to test SEC filings (use the padded CIK)
    cik_tuple = cik_lookup.ticker_to_cik("AAPL")
    if not cik_tuple:
        print("CIK not found for AAPL")
        return
    cik = cik_tuple[0]  # '0000320193'

    # initialize SECFilings with same user agent as your code
    sec_filings = SECFilings(user_agent="Kidus Assefa kidusyosef81@gmail.com")

    # get latest 10-Q (no year) and print URL (or None)
    q_url = sec_filings.quarterly_filing(cik)
    print("Latest 10-Q URL:", q_url)

    # get latest 10-K
    k_url = sec_filings.annual_filing(cik)
    print("Latest 10-K URL:", k_url)

if __name__ == "__main__":
    main()