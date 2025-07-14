def get_walmart_prices_near_zip(upc, zip_code):
    # This is placeholder data. Replace this logic with real Walmart API/scraper integration.
    stores = [
        {"store": "Walmart San Diego", "distance": 2.5, "price": 15.00},
        {"store": "Walmart El Cajon", "distance": 6.8, "price": 10.00},
        {"store": "Walmart Chula Vista", "distance": 12.3, "price": 17.00},
        {"store": "Walmart Oceanside", "distance": 20.1, "price": 20.00},
    ]
    return sorted(stores, key=lambda x: x["distance"])
