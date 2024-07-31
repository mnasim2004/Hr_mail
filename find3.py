import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_company_names(csv_file):
    try:
        df = pd.read_csv(csv_file)
        company_names = df['Company Name'].tolist()
        return company_names
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return []
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty.")
        return []
    except pd.errors.ParserError:
        print(f"Error: The file '{csv_file}' is not in a valid CSV format.")
        return []

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

def search_linkedin_alumni_profiles(session, company_name, university_name):
    query = f'"{company_name}" "{university_name}" -intitle:"profiles" -inurl:"dir/" site:in.linkedin.com/in/'
    url = f"https://www.google.com/search?q={query}"
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        print(f"Error: Failed to retrieve search results for {company_name} and {university_name}")
        return []

    profiles = [link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('https://in.linkedin.com/in/')]
    # Filter profiles to ensure both company and university names are present in the profile URL
    filtered_profiles = [profile for profile in profiles if company_name.lower() in profile.lower() and university_name.lower() in profile.lower()]
    return filtered_profiles

def main():
    csv_file = 'company_name2.csv'  # Replace with your CSV file path
    output_file = 'linkedin_alumni_profiles.csv'  # File to save the results

    company_names = get_company_names(csv_file)
    if not company_names:
        return

    session = create_session_with_retries()
    results = []

    for company in company_names:
        print(f"Company: {company}")
        
        # Assuming university names are also in the CSV or you have a way to provide them
        university_name = 'Cochin University of Science and Technology'  # Replace or modify as needed
        
        profiles = search_linkedin_alumni_profiles(session, company, university_name)
        if profiles:
            print("LinkedIn Alumni Profiles:")
            for profile in profiles:
                print(profile)
        else:
            profiles = ["Not found"]
            print("LinkedIn Alumni Profiles: Not found")
        
        for profile in profiles:
            results.append({'Company': company, 'LinkedIn Profile': profile})
        
        print("-" * 40)
        
        # Add delay to avoid hitting rate limits
        time.sleep(10)  # Adjust delay as needed

    # Create a DataFrame and save it to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Results have been saved to '{output_file}'")

if __name__ == "__main__":
    main()
