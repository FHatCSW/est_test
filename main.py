import est.client
import re
import json

class ESTClientWrapper:
    def __init__(self, host, port, alias, implicit_trust_anchor_cert_path):
        self.client = est.client.Client(host, port, alias, implicit_trust_anchor_cert_path)

    def configure_basic_auth(self, username, password):
        self.client.set_basic_auth(username, password)

    def get_cacerts(self):
        return self.client.cacerts()

    def create_csr(self, common_name, organization, organizational_unit, country, subject_alt_name):
        priv, csr = self.client.create_csr(
            common_name=common_name,
            organization=organization,
            organizational_unit=organizational_unit,
            country=country,
            subject_alt_name=subject_alt_name
        )
        m = re.search(r"(?<=-----BEGIN CERTIFICATE REQUEST-----).*?(?=-----END CERTIFICATE REQUEST-----)", csr.decode(), flags=re.DOTALL)
        csr = m.group()
        return priv, csr

    def simpleenroll(self, csr):
        return self.client.simpleenroll(csr)

def load_credentials_from_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        config_data = json.load(file)
    return (
        config_data.get('username'),
        config_data.get('password'),
        config_data.get('client_alias'),
        config_data.get('server_alias')
    )

def handle_alias(username, password, host, port, alias, implicit_trust_anchor_cert_path, common_name, country, organization, organization_unit, subject_alt_name):

    est_wrapper = ESTClientWrapper(host, port, alias, implicit_trust_anchor_cert_path)
    est_wrapper.configure_basic_auth(username, password)

    ca_certs = est_wrapper.get_cacerts()

    priv, csr = est_wrapper.create_csr(common_name, organization, organization_unit, country, subject_alt_name)

    client_cert = est_wrapper.simpleenroll(csr)

    print(f'-----{alias.upper()} CERTIFICATE-----')
    print(client_cert)

if __name__ == "__main__":
    port = 443
    implicit_trust_anchor_cert_path = 'bin/OiPKIMngCA-chain.pem'
    common_name = 'my_cn'
    country = 'DE'
    organization = 'my_o'
    organization_unit = 'my_ou'
    subject_alt_name = b'URI:http://www.ietf.org/rfc/rfc3986.txt'

    host, username, password, client_alias, server_alias = load_credentials_from_config()

    handle_alias(username, password, host, port, client_alias, implicit_trust_anchor_cert_path, common_name, country, organization, organization_unit, subject_alt_name)

    handle_alias(username, password, host, port, server_alias, implicit_trust_anchor_cert_path, common_name, country, organization, organization_unit, subject_alt_name)
