import whois
import socket
import dns.resolver
from ipwhois import IPWhois

def get_domain_info(domain_name):
    # Get basic domain information using whois
    domain_info = whois.whois(domain_name)

    # IP address
    try:
        ip_address = socket.gethostbyname(domain_name)
        domain_info['ip_address'] = ip_address

        # Geolocation information based on IP address
        ipwhois_result = IPWhois(ip_address)
        ip_info = ipwhois_result.lookup_rdap()
        domain_info['geolocation'] = ip_info.get('asn_description', None)
    except socket.gaierror as e:
        print(f"Error: {e}")
        domain_info['ip_address'] = None
        domain_info['geolocation'] = None

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
