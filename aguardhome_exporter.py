import asyncio
import base64
import daemon
import time
import os
from adguardhome import AdGuardHome
from prometheus_client import start_http_server, Gauge


def define_exporter_port():
    if os.getenv("ADGUARDHOME_EXPORTER_PORT"):
        return int(os.getenv("ADGUARDHOME_EXPORTER_PORT"))
    else:
        return 9101


def decode_base64_env_var(env_var_name):
    """
    Decode a base64-encoded environment variable.

    Args:
    - env_var_name: Name of the environment variable containing the base64-encoded string.

    Returns:
    - Decoded string if successful, None otherwise.
    """
    encoded_value = os.environ.get(env_var_name)
    if encoded_value is None:
        print(f"Environment variable '{env_var_name}' not found.")
        return None

    try:
        decoded_bytes = base64.b64decode(encoded_value)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"Error decoding environment variable '{env_var_name}': {e}")
        return None

async def check_protection_status(host="localhost", username="", password="", port=""):
    """Show example how to get status of your AdGuard Home instance."""
    async with AdGuardHome(host=host, username=username, password=password, port=80) as adguard:
        version = await adguard.version()
        print("AdGuard version:", version)

        active = await adguard.protection_enabled()
        active = 1 if active else 0
    return active

def main():
    exporter_port = define_exporter_port()
    protection_status = Gauge('adguard_protection_status', 'Total number of DNS queries processed by AdGuard Home')
    # Start the HTTP server to expose metrics
    start_http_server(exporter_port)  # Different port to avoid conflict with the previous example

    # Periodically collect and update metrics
    while True:
        status = asyncio.run(check_protection_status(host=decode_base64_env_var("ADGUARDHOME_IP"), username=decode_base64_env_var("ADGUARDHOME_USERNAME"), password=decode_base64_env_var("ADGUARDHOME_PASSWORD"), port=80))
        protection_status.set(status)
        time.sleep(60)  # Adjust the interval as needed

if __name__ == '__main__':
    # Run the main function as a daemon
    # with daemon.DaemonContext():
    main()
