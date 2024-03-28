# AdGuardHome-Exporter
Minimal AdGuardHome-Exporter

## How to use it:
1. Please set env vars **Please encode it in B64**:

| Environment Variable        | Default Value |
|-----------------------------|---------------|
| `ADGUARDHOME_IP`            | `localhost`   |
| `ADGUARDHOME_PORT`          | `5432`        |
| `ADGUARDHOME_USERNAME`      | `none`        |
| `ADGUARDHOME_PASSWORD`      | `none`        |
| `ADGUARDHOME_PORT`          | `80`          |
| `ADGUARDHOME_EXPORTER_PORT` | `9100`        |
|-----------------------------|---------------|

2. Create systemd service:
```bash
sudo vim /etc/systemd/system/adguardhome_exporter.service
```

with this content:
```plaintext
[Unit]
Description=AdGuardHome Exporter Service
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /usr/local/bin/aguardhome_exporter.py

[Install]
WantedBy=multi-user.target
```

3. Place aguardhome_exporter.py in /usr/local/bin/
```bash
sudo mv aguardhome_exporter.py /usr/local/bin/ && chmod +x /usr/local/bin/aguardhome_exporter.py
```

4. Start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable adguardhome_exporter.service
sudo systemctl start adguardhome_exporter.service
```

5. Check the Status: You can check the status of the service to ensure it's running without errors:
```bash
sudo systemctl status adguardhome_exporter.service
````
