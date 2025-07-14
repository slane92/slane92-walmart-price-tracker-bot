from walmart_api import get_walmart_prices_near_zip

# Example auto-checker (you'll customize this later)
UPC = "884392951955"
ZIP = "92131"

def run_check():
    print(f"Checking Walmart for UPC {UPC} near {ZIP}...")
    results = get_walmart_prices_near_zip(UPC, ZIP)
    for r in results:
        print(f"{r['store']}: ${r['price']} at {r['distance']} miles")

if __name__ == "__main__":
    run_check()
