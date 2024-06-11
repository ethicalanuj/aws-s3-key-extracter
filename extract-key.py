import requests
from bs4 import BeautifulSoup
import sys

def get_s3_keys_from_xml(xml_content):
    soup = BeautifulSoup(xml_content, features="xml")  # Specify features="xml" to use the XML parser
    keys = [key.text for key in soup.find_all('Key')]
    return keys

def check_domain_for_s3(domain):
    try:
        response = requests.get(domain)
        if 'Content-Type' in response.headers and 'application/xml' in response.headers['Content-Type']:
            return get_s3_keys_from_xml(response.content)
    except Exception as e:
        print(f"An error occurred for domain {domain}: {e}")
    return []

def main(domains, output_file):
    all_keys = []
    for domain in domains:
        print(f"Checking domain: {domain}")
        keys = check_domain_for_s3(domain)
        if keys:
            all_keys.extend(keys)
    
    with open(output_file, 'w') as file:
        for key in all_keys:
            file.write(f"{key}\n")
    print(f"Keys have been saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract-key.py <output_file> <domain1> <domain2> ... <domainN>")
        sys.exit(1)

    output_file = sys.argv[1]
    domains = sys.argv[2:]

    main(domains, output_file)

