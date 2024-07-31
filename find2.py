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

def search_company_domain(session, company_name):
    time.sleep(5)
    query = f"{company_name} official site"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        print(f"Error: Failed to retrieve search results for {company_name}")
        return None

    for cite in soup.find_all('cite'):
        domain = cite.text.replace('https://', '').replace('http://', '').replace('www.', '')
        return domain

    return None

# def search_company_domain(session, company_name):
#     max_retries = 5
#     retry_delay = 5  # Initial delay in seconds
    
#     for attempt in range(max_retries):
#         time.sleep(retry_delay)
#         query = f"{company_name} official site"
#         url = f"https://www.google.com/search?q={query}"
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
#         try:
#             response = session.get(url, headers=headers)
#             if response.status_code == 429:
#                 print("Rate limit exceeded, retrying...")
#                 retry_delay *= 2  # Exponential backoff
#                 continue
            
#             if response.status_code != 200:
#                 print(f"Error: Failed to retrieve search results for {company_name}")
#                 return None
            
#             soup = BeautifulSoup(response.text, 'html.parser')
#             for cite in soup.find_all('cite'):
#                 domain = cite.text.replace('https://', '').replace('http://', '').replace('www.', '')
#                 return domain

#             return None
        
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed: {e}")
#             return None

#     print("Max retries exceeded")
#     return None


def search_linkedin_hr_profiles(session, company_name):
    query = f'"{company_name}" "HR" -intitle:"profiles" -inurl:"dir/+"+site:in.linkedin.com/in/'
    url = f"https://www.google.com/search?q={query}"
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        print(f"Error: Failed to retrieve search results for {company_name}")
        return []

    profiles = [link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('https://in.linkedin.com/in/')]
    return profiles

def main():
    csv_file = 'trial.csv'  # Replace with your CSV file path

    company_names = get_company_names(csv_file)
    if not company_names:
        return

    session = create_session_with_retries()
    results = []

    for company in company_names:
        print(f"Company: {company}")
        
        domain = search_company_domain(session, company)
        if domain:
            print(f"Domain: {domain}")
        else:
            domain = "Not found"
            print("Domain: Not found")
        
        profiles = search_linkedin_hr_profiles(session, company)
        if profiles:
            print("LinkedIn HR Profiles:")
            for profile in profiles:
                print(profile)
        else:
            profiles = ["Not found"]
            print("LinkedIn HR Profiles: Not found")
        
        company_data = {
            'Company': company,
            'Domain': domain
        }
        
        for i, profile in enumerate(profiles, start=1):
            company_data[f'LinkedIn HR Profile {i}'] = profile
        
        results.append(company_data)
        
        print("-" * 40)
        
        # Add delay to avoid hitting rate limits
        time.sleep(10)  # Adjust delay as needed

    # Create a DataFrame and save it to an Excel file
    results_df = pd.DataFrame(results)
    results_df.to_excel('trial_company_domains_and_hr_profiles.xlsx', index=False)
    print("Results have been saved to 'company_domains_and_hr_profiles2.xlsx'")

if __name__ == "__main__":
    main()
