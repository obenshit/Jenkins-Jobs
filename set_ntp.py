import paramiko
import argparse

def main():
    try:
        print
        print("\n🚀 Starting script", flush=True)
        parser = argparse.ArgumentParser(description='configure NTP')
        parser.add_argument('--host', help="hostname or IP")
        parser.add_argument('--username', help="SSH username")
        parser.add_argument('--password', help="SSh password")

        args = parser.parse_args()
        host = args.host
        username = args.username
        password = args.password

        ssh = connect_ssh(host, username, password)
        print("🔐 Connected via SSH", flush=True)
        configure_ntp(ssh)
        print("✅ Configuration function completed", flush=True)
        ssh.close()
    except Exception as e:
        print(f"❌ Exception caught: {e}", flush=True)

def connect_ssh(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, username, password)
    return ssh

def configure_ntp(ssh):
    print("############ configure the NTP Server ############", flush=True)
    cmd = "echo 'server ntp.esl.cisco.com' | tee -a /etc/chrony.conf && systemctl restart chronyd"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("✅ NTP configuration succeeded", flush=True)
    else:
        print("❌ NTP configuration failed", flush=True)
        err = stderr.read().decode()
        print(f"Error details:\n{err}", flush=True)
    print("🕒 Setting timezone to Asia/Jerusalem", flush=True)
    stdin, stdout, stderr = ssh.exec_command("sudo timedatectl set-timezone Asia/Jerusalem")
    stdout.channel.recv_exit_status()
    print("\n📅 Current time on the server:", flush=True)
    stdin, stdout, stderr = ssh.exec_command("date")
    print(stdout.read().decode(), flush=True)

if __name__ == "__main__":
    main()
