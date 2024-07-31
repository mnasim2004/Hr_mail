# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# def get_company_names(csv_file):
#     try:
#         df = pd.read_csv(csv_file)
#         company_names = df['Company Name'].tolist()
#         return company_names
#     except FileNotFoundError:
#         print(f"Error: The file '{csv_file}' was not found.")
#         return []
#     except pd.errors.EmptyDataError:
#         print(f"Error: The file '{csv_file}' is empty.")
#         return []
#     except pd.errors.ParserError:
#         print(f"Error: The file '{csv_file}' is not in a valid CSV format.")
#         return []

# def search_company_domain(company_name):
#     query = f"{company_name} official site"
#     url = f"https://www.google.com/search?q={query}"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     print(f"Debug: Searching for domain of '{company_name}'")
#     print(f"Debug: Google search URL: {url}")
#     print(f"Debug: HTTP status code: {response.status_code}")

#     if response.status_code != 200:
#         print("Error: Failed to retrieve search results")
#         return None

#     domain = None
#     for cite in soup.find_all('cite'):
#         domain = cite.text
#         print(f"Debug: Found cite tag: {domain}")
#         break

#     if domain:
#         domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
#         print(f"Debug: Extracted domain: {domain}")
#     else:
#         print("Debug: No domain found")

#     return domain

# def main():
#     csv_file = 'company_name.csv'  # Replace with your CSV file path

#     company_names = get_company_names(csv_file)
    
#     if not company_names:
#         return

#     for company in company_names:
#         print(f"Company: {company}")
        
#         domain = search_company_domain(company)
#         if domain:
#             print(f"Domain: {domain}")
#         else:
#             print("Domain: Not found")
        
#         print("-" * 40)

# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def search_company_domain(company_name):
    query = f"{company_name} official site"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"Debug: Searching for domain of '{company_name}'")
    print(f"Debug: Google search URL: {url}")
    print(f"Debug: HTTP status code: {response.status_code}")

    if response.status_code != 200:
        print("Error: Failed to retrieve search results")
        return None

    domain = None
    for cite in soup.find_all('cite'):
        domain = cite.text
        print(f"Debug: Found cite tag: {domain}")
        break

    if domain:
        domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
        print(f"Debug: Extracted domain: {domain}")
    else:
        print("Debug: No domain found")

    return domain

def search_linkedin_hr_profiles(company_name):
    query = f'"{company_name}" "HR" -intitle:"profiles" -inurl:"dir/+"+site:in.linkedin.com/in/'
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"Debug: Searching for LinkedIn HR profiles of '{company_name}'")
    print(f"Debug: Google search URL: {url}")
    print(f"Debug: HTTP status code: {response.status_code}")

    if response.status_code != 200:
        print("Error: Failed to retrieve search results")
        return None

    profiles = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('https://in.linkedin.com/in/'):
            print(f"Debug: Found LinkedIn profile link: {href}")
            profiles.append(href)

    if not profiles:
        print("Debug: No LinkedIn profiles found")

    return profiles

def main():
    csv_file = 'company_name.csv'  # Replace with your CSV file path

    company_names = get_company_names(csv_file)
    
    if not company_names:
        return

    for company in company_names:
        print(f"Company: {company}")
        
        domain = search_company_domain(company)
        if domain:
            print(f"Domain: {domain}")
        else:
            print("Domain: Not found")
        
        profiles = search_linkedin_hr_profiles(company)
        if profiles:
            print("LinkedIn HR Profiles:")
            for profile in profiles:
                print(profile)
        else:
            print("LinkedIn HR Profiles: Not found")
        
        print("-" * 40)

if __name__ == "__main__":
    main()
