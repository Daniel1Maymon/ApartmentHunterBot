import requests

def run_scraper():
    response = requests.get('http://localhost:5000/run_scraper')
    print(f"Status code: {response.status_code}")

if __name__ == '__main__':
    print("Scraper is running...")
    run_scraper()
    print("Scraper is finish...")
    print("---------------")
