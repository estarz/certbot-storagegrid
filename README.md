# Certbot Plugin for StorageGRID

## Update management and API certificates from certbot

- proof of concept

# Setup in LOD
- Launch "Getting Started with StorageGRID v2.1"
- From StorageGRID UI, create admin group with full permissions and a user belonging to that group
  
- SSH to host "ansible"
- Update and install prereqs
  ```
  sudo apt update
  sudo apt upgrade -y
  sudo apt install python3 python3-dev python3-venv augeas-devel gcc
  ```
- Download certbot source and storagegrid plugins
  ```
  mkdir work
  cd work
  git clone https://github.com/certbot/certbot
  git clone https://github.com/estarz/certbot-storagegrid
  ```
- setup venv
  ```
  cd certbot
  python3 tools/venv.py
  ```
- enter venv
  ```
  source venv/bin/activate
  ```
- install storagegrid plugin
  ```
  pip install -e ../certbot-storagegrid/
  ```
- check if the new storagegrid plugin shows up among installed plugins
  ```
  certbot_test plugins
  ```

# Start Pebble ACME server
- Open a 2nd SSH session to host "ansible"
- Start acme server
  ```
  cd work/certbot
  source venv/bin/activate
  run_acme_server
  ```

# Update API (S3) certificate
For some reason, I can't get certbot_test to work, it will hard fail on the TLS warning from the StorageGRID plugin
Hance running certbot with all the same options certbot_test adds, in addition to the storagegrid 

- in the first SSH session run
  ```
  certbot --no-verify-ssl --http-01-port 5002 --https-port 5001 \
  --config-dir /home/ansible/work/certbot/.certbot_test_workspace/conf \
  --work-dir /home/ansible/work/certbot/.certbot_test_workspace/work \
  --logs-dir /home/ansible/work/certbot/.certbot_test_workspace/logs \
  --non-interactive --no-redirect --agree-tos --register-unsafely-without-email \
  --debug -vv run \
  --installer storagegrid --storagegrid-api-url https://10.128.16.40/ \
  --storagegrid-username 'certbot' \
  --storagegrid-password 'netapp1234' \
  --storagegrid-cert-type management \
  -d s3-admin.swelab.local \
  --standalone --storagegrid-no-verify-ssl --no-random-sleep-on-renew --server https://localhost:14000/dir
  ```
