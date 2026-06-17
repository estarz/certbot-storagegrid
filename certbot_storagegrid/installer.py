# certbot_storagegrid/installer.py
import logging
from certbot import interfaces, errors
from certbot.plugins import common

logger = logging.getLogger(__name__)

class Installer(common.Plugin, interfaces.Installer):
    description = "StorageGRID Certificate Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("api-url", help="StorageGRID Management API URL")
        add("username", help="Admin username")
        add("password", help="Admin password")
        add("cert-type", help="Certificate type: management or s3", default="management")
        add("no-verify-ssl", action="store_true", help="Disable SSL verification")

    def prepare(self):
        """Prepare the plugin - validate config."""
        self.api_url = self.conf("api-url")
        self.username = self.conf("username")
        self.password = self.conf("password")
        self.cert_type = self.conf("cert-type")
        self.verify_ssl = not self.conf("no-verify-ssl")

        if not all([self.api_url, self.username, self.password]):
            raise errors.PluginError(
                "StorageGRID API URL, username, and password are required."
            )

    def more_info(self):
        return "Installs certificates on NetApp StorageGRID via the Management API."

    def get_all_names(self):
        return []

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        """Deploy certificate to StorageGRID."""
        from .storagegrid_client import StorageGRIDClient

        logger.info(f"🔐 Deploying certificate for {domain} to StorageGRID...")

        with open(fullchain_path, 'r') as f:
            cert_pem = f.read()
        with open(key_path, 'r') as f:
            key_pem = f.read()

        chain_pem = None
        if chain_path:
            with open(chain_path, 'r') as f:
                chain_pem = f.read()

        client = StorageGRIDClient(
            self.api_url, self.username, self.password, self.verify_ssl
        )

        if self.cert_type == "s3":
            client.update_s3_certificate(cert_pem, key_pem, chain_pem)
        else:
            client.update_management_certificate(cert_pem, key_pem, chain_pem)

        logger.info(f"✅ Certificate deployed successfully to StorageGRID ({self.cert_type})")

    def enhance(self, domain, enhancement, options=None):
        pass

    def supported_enhancements(self):
        return []

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def recovery_routine(self):
        pass

    def restart(self):
        pass

    def config_test(self):
        pass
