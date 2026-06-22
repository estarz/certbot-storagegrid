# Certbot Plugin for StorageGRID

## Update management and API certificates from certbot

This is just a proof of concept

## Possible enhancements

Store plugin parameters in a config file 

# Setup in LOD
- Launch "Getting Started with StorageGRID v2.1"
- From StorageGRID UI, create admin group with full permissions and a user belonging to that grou
  In this POC, a user named "cerbot" with the password "netapp1234" was created
  
- SSH to host "ansible"
- Update and install prereqs
  ```
  sudo apt update
  sudo apt upgrade -y
  sudo apt install python3 python3-dev python3-venv libaugeas-dev gcc
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
If the server stops and you want to restart it, make sure to delete the temp dir, ".certbot_test_workspace", before the restart


# Update API (S3) certificate
For some reason, I can't get certbot_test to work, it will hard fail on the TLS warning from the StorageGRID plugin
Hence running certbot with all the same options certbot_test adds, in addition to the storagegrid 
The -storagegrid-no-verify-ssl flag is being honoured, without it there is an error instead of the warning...

`PYTHONWARNINGS="ignore::urllib3.exceptions.InsecureRequestWarning"`

The -storagegrid-cert-type has 2 valid values, "s3" and "management" which will update the S3 API certificate and Management interface certificate respectively

- in the first SSH session run
  ```
  certbot --no-verify-ssl --http-01-port 5002 --https-port 5001 \
  --config-dir /home/ansible/work/certbot/.certbot_test_workspace/conf \
  --work-dir /home/ansible/work/certbot/.certbot_test_workspace/work \
  --logs-dir /home/ansible/work/certbot/.certbot_test_workspace/logs \
  --non-interactive --no-redirect --agree-tos --register-unsafely-without-email \
  --debug -vv run \
  --installer storagegrid --storagegrid-api-url https://192.168.0.80/ \
  --storagegrid-username 'certbot' \
  --storagegrid-password 'netapp1234' \
  --storagegrid-cert-type management \
  -d s3-admin.demo.netapp.com \
  --standalone --storagegrid-no-verify-ssl --no-random-sleep-on-renew --server https://localhost:14000/dir
  ```
