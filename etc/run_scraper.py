import requests
from datetime import datetime

def run_scraper():
    # response = requests.get('http://localhost:5000/run_scraper')
    response = requests.get('http://localhost:5001/get_posts')
    print(f"Status code: {response.status_code}")

if __name__ == '__main__':
    current_time = datetime.now()
    print(f"time: {current_time.strftime('%H:%M:%S')}")
    print("Scraper is running...")
    run_scraper()
    print("Scraper is finish...")
    print("---------------")
