import base64
import ctypes

import est.client
import re

host = 'campuspki.germanywestcentral.cloudapp.azure.com'
alias = '/Test_PC_OPC_Client'
#alias = '/Test_PC_OPC_Server'
port = 443
implicit_trust_anchor_cert_path = 'ManagementCA-chain.pem'

client = est.client.Client(host, port, alias, implicit_trust_anchor_cert_path)

# Get CSR attributes from EST server as an OrderedDict.
#csr_attrs = client.csrattrs()

# Get EST server CA certs.
ca_certs = client.cacerts()

username = 'plcnext'
password = 'foo123'
client.set_basic_auth(username, password)
# Create CSR and get private key used to sign the CSR.
common_name = 'est-Test1014.campuspki.test'
country = 'DE'
organization = 'PhoenixContact'
organization_unit = 'BUAS'
subject_alt_name = b'URI:http://www.ietf.org/rfc/rfc3986.txt'

priv, csr = client.create_csr(common_name=common_name,
                              organization=organization,
                              organizational_unit=organization_unit,
                              country=country,
                              #subject_alt_name=subject_alt_name
                              )
# EJBCA don't want Header files
m = re.search(r"(?<=-----BEGIN CERTIFICATE REQUEST-----).*?(?=-----END CERTIFICATE REQUEST-----)", csr.decode(), flags=re.DOTALL)
csr = m.group()
client_cert = client.simpleenroll(csr)
print(client_cert)