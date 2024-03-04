import whois
import socket
import dns.resolver
import requests

def get_hosting_region(ip_address):
    

    try:
        response = requests.get(f"https://ipinfo.io/8.8.8.8/json?token=c0ec2816fd3065")
        data = response.json()
        hosting_region = data.get("country", None)
        return hosting_region
    except requests.RequestException as e:
        print(f"Error retrieving hosting region: {e}")
        return None

def get_domain_info(domain_name):
    # Get basic domain information using whois
    domain_info = whois.whois(domain_name)

    # Get IP address
    try:
        ip_address = socket.gethostbyname(domain_name)
        domain_info['ip_address'] = ip_address

        # Get hosting region using IPinfo API
        hosting_region = get_hosting_region(ip_address)
        domain_info['hosting_region'] = hosting_region
    except socket.gaierror as e:
        print(f"Error: {e}")
        domain_info['ip_address'] = None
        domain_info['hosting_region'] = None

    # DNS information 
    try:
        dns_records = dns.resolver.resolve(domain_name, 'A')
        domain_info['dns_records'] = [record.address for record in dns_records]
    except dns.resolver.NXDOMAIN:
        print(f"DNS Error: Domain not found.")
        domain_info['dns_records'] = None
    except dns.resolver.NoAnswer:
        print(f"DNS Error: No A records found.")
        domain_info['dns_records'] = None

    return domain_info

if __name__ == "__main__":
    domain_name = input("Enter the domain name: ")
    result = get_domain_info(domain_name)
    print(result)

