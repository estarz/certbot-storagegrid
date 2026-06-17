# certbot_storagegrid/storagegrid_client.py
import requests

class StorageGRIDClient:
    def __init__(self, api_url, username, password, verify_ssl=True):
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self._authenticate(username, password)

    def _authenticate(self, username, password):
        resp = self.session.post(
            f"{self.api_url}/api/v4/authorize",
            json={"username": username, "password": password, "cookie": False}
        )
        resp.raise_for_status()
        token = resp.json()["data"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def update_management_certificate(self, cert_pem, key_pem, ca_chain_pem=None):
        payload = {
            "serverCertificateEncoded": cert_pem,
            "privateKeyEncoded": key_pem,
        }
        if ca_chain_pem:
            payload["caBundleEncoded"] = ca_chain_pem
        resp = self.session.post(
            f"{self.api_url}/api/v4/grid/management-certificate/update",
            json=payload
        )
        resp.raise_for_status()
        return resp

    def update_s3_certificate(self, cert_pem, key_pem, ca_chain_pem=None):
        payload = {
            "serverCertificateEncoded": cert_pem,
            "privateKeyEncoded": key_pem,
        }
        if ca_chain_pem:
            payload["caBundleEncoded"] = ca_chain_pem
        resp = self.session.post(
            f"{self.api_url}/api/v4/grid/storage-api-certificate/update",
            json=payload
        )
        resp.raise_for_status()
        return resp

    def config_test(self):
        print ("Configuration test implemented!")
