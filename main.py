import est.client
import re

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

def handle_alias(host, port, alias, implicit_trust_anchor_cert_path, username, password, common_name, country, organization, organization_unit, subject_alt_name):
    est_wrapper = ESTClientWrapper(host, port, alias, implicit_trust_anchor_cert_path)
    est_wrapper.configure_basic_auth(username, password)

    ca_certs = est_wrapper.get_cacerts()

    priv, csr = est_wrapper.create_csr(common_name, organization, organization_unit, country, subject_alt_name)

    client_cert = est_wrapper.simpleenroll(csr)

    print(client_cert)

if __name__ == "__main__":
    host = '74.234.234.46'
    port = 443
    implicit_trust_anchor_cert_path = 'OiPKIMngCA-chain.pem'
    username = 'plcnext'
    password = 'g2hjOhO7h5a6'
    client_alias = '/PhoenixContact-OpcClient'
    server_alias = '/PhoenixContact-OpcServer'
    common_name = 'test_plc_002'
    country = 'DE'
    organization = 'PC'
    organization_unit = 'BUAS'
    subject_alt_name = b'URI:http://www.ietf.org/rfc/rfc3986.txt'

    print('-----CLIENT CERTIFICATE-----')
    handle_alias(host, port, client_alias, implicit_trust_anchor_cert_path, username, password, common_name, country, organization, organization_unit, subject_alt_name)

    print('-----SERVER CERTIFICATE-----')
    handle_alias(host, port, server_alias, implicit_trust_anchor_cert_path, username, password, common_name, country, organization, organization_unit, subject_alt_name)




