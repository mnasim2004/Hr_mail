import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

def fetch_website(url):
    session = create_session_with_retries()
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = session.get(url)
            if response.status_code == 200:
                print("Success:")
                print(response.text[:500])  # Print the first 500 characters of the response
                return response.text
            elif response.status_code == 429:
                print(f"Rate limit exceeded, retrying... ({retry_count+1}/{max_retries})")
                retry_count += 1
                time.sleep(10 * retry_count)  # Exponential backoff
            else:
                print(f"Failed to retrieve page. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            retry_count += 1
            time.sleep(10 * retry_count)  # Exponential backoff

    print("Max retries exceeded. Unable to fetch the website.")
    return None

if __name__ == "__main__":
    url = 'https://cusat.ac.in/'  # Replace with the URL you want to test
    fetch_website(url)
