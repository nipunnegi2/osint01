import whois
import socket
import dns.resolver

def get_domain_info(domain_name):
    # Get basic domain information using whois
    domain_info = whois.whois(domain_name)

    #ip
    try:
        ip_address = socket.gethostbyname(domain_name)
        domain_info['ip_address'] = ip_address
    except socket.gaierror as e:
        print(f"Error: {e}")
        domain_info['ip_address'] = None

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
