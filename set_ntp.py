import paramiko
import argparse

def main():
    print("🚀 Starting script")
    parser = argparse.ArgumentParser(description='configure NTP')
    parser.add_argument('--host', help="hostname or IP")
    parser.add_argument('--username', help="SSH username")
    parser.add_argument('--password', help="SSh password")

    args = parser.parse_args()
    host = args.host
    username = args.username
    password = args.password

    ssh = connect_ssh(host, username, password)
    print("🔐 Connected via SSH")
    configure_ntp(ssh)
    print("✅ Configuration function completed")
    ssh.close()

def connect_ssh(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, username, password)
    return ssh

def configure_ntp(ssh):
    print("""############ configure the NTP Server ############""")
    cmd = "bash -c \"echo 'server ntp.esl.cisco.com' >> /etc/chrony.conf && systemctl restart chronyd\""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("✅ NTP configuration succeeded")
    else:
        print("❌ NTP configuration failed")
    print("\n📅 Current time on the server:")
    stdin, stdout, stderr = ssh.exec_command("date")
    print(stdout.read().decode())
