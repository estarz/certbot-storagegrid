# Certbot Plugin for StorageGRID

## Update management and API certificates from certbot

- proof of concept

# Setup in LOD
- Launch "Getting Started with StorageGRID v2.1"
- SSH to host "ansible"
- Update and install prereqs "sudo apt update && sudo apt upgrade -y && sudo apt install python3 python3-dev python3-venv augeas-devel gcc"
- Download certbot source and storagegrid plugins "mkdir work && cd work && git clone https://github.com/certbot/certbot && git clone https://github.com/estarz/certbot-storagegrid"
- setup venv "cd certbot && python3 tools/venv.py"
- enter venv "source venve/bin/activate"
- install storagegrid plugin "pip install -e ../certbot-staorgegrid/"
- test plugins "certbot_test plugins"

# Update API (S3) certificate
- certbot_test run --no-verify-ssl --http-01-port 5002 --https-port 5001 --config-dir --installer storagegrid --storagegrid-api-url https://192.168.0.80/ --storagegrid-username 'root' --storagegrid-password 'Netapp1!' --storagegrid-cert-type s3 -d s3.demo.netapp.com --storagegrid-no-verify-ssl --standalone
