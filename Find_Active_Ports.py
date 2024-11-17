from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import argparse

def connect_and_check_ports(ip_or_dns, username, password):
    # Define connection parameters for SSH
    device = {
        'device_type': 'cisco_ios',  # Start with SSH
        'host': ip_or_dns,
        'username': username,
        'password': password,
    }

    try:
        # Attempt connection via SSH first
        connection = ConnectHandler(**device)
        print("SSH connection successful")
    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        print("SSH connection failed, trying Telnet")
        
        # Change to Telnet if SSH fails
        device['device_type'] = 'cisco_ios_telnet'
        
        try:
            # Attempt connection via Telnet
            connection = ConnectHandler(**device)
            print("Telnet connection successful")
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            print(f"Connection failed for both SSH and Telnet: {str(e)}")
            return None

    # Run command to check the status of the ports
    output = connection.send_command("show interface status")
    connection.disconnect()
    
    # Count how many ports are up, excluding portchannel interfaces
    active_ports = sum(1 for line in output.splitlines() if "connected" in line.lower() and not line.lower().startswith("po"))

    return active_ports

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Check active ports on a network device.')
    parser.add_argument('--ip', required=True, help='IP address or DNS of the device')
    parser.add_argument('--username', default='nmtg', help='Username for the device')
    parser.add_argument('--password', default='NRSFHn31', help='Password for the device')
    
    args = parser.parse_args()

    # Use provided arguments
    active_ports = connect_and_check_ports(args.ip, args.username, args.password)
    
    if active_ports is not None:
        print("\n\n")
        print(f"Found {active_ports} active ports on the device.")
        print("test for git on VScode")
    else:
        print("\n\n")
        print("Failed to connect to the device.")
