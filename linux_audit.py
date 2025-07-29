import os
import subprocess

# Report and score trackers
report = []
score = 0
max_score = 6

def check_firewall():
    global score
    report.append(" Firewall Check:")
    try:
        ufw_status = subprocess.getoutput("ufw status")
        if "Status: active" in ufw_status:
            report.append(" UFW is active.")
            score += 1
        else:
            iptables = subprocess.getoutput("iptables -L")
            if "Chain" in iptables:
                report.append(" iptables is configured.")
                score += 1
            else:
                report.append(" No active firewall found.")
    except Exception as e:
        report.append(f" Error checking firewall: {e}")

def check_services():
    global score
    report.append("\n Service Check:")
    try:
        services = subprocess.getoutput("systemctl list-units --type=service --state=running")
        unnecessary = [s for s in services.splitlines() if "bluetooth" in s or "cups" in s]
        if unnecessary:
            report.append(" Unnecessary services running:")
            for s in unnecessary:
                report.append(f"     - {s}")
        else:
            report.append(" No unnecessary services found.")
            score += 1
    except Exception as e:
        report.append(f" Error checking services: {e}")

def check_ssh_settings():
    global score
    report.append("\n SSH Configuration Check:")
    try:
        with open("/etc/ssh/sshd_config") as f:
            config = f.read()
            if "PermitRootLogin no" in config and "Protocol 2" in config:
                report.append(" SSH is configured securely.")
                score += 1
            else:
                report.append("  Insecure SSH settings detected.")
    except Exception as e:
        report.append(f" SSH config check failed: {e}")

def check_file_permissions():
    global score
    report.append("\n File Permission Check:")
    try:
        shadow_perm = oct(os.stat("/etc/shadow").st_mode)[-3:]
        passwd_perm = oct(os.stat("/etc/passwd").st_mode)[-3:]
        if shadow_perm == "000" or shadow_perm == "640":
            report.append("  /etc/shadow permissions are secure.")
            score += 0.5
        else:
            report.append(f"  /etc/shadow has wrong permissions: {shadow_perm}")

        if passwd_perm in ["644", "640"]:
            report.append("  /etc/passwd permissions are secure.")
            score += 0.5
        else:
            report.append(f"  /etc/passwd has wrong permissions: {passwd_perm}")
    except Exception as e:
        report.append(f"  File permission check failed: {e}")

def check_rootkits():
    global score
    report.append("\n🧬 Rootkit Check:")
    try:
        chkrootkit = subprocess.getoutput("which chkrootkit")
        rkhunter = subprocess.getoutput("which rkhunter")
        found = False
        if chkrootkit:
            output = subprocess.getoutput("sudo chkrootkit")
            if "INFECTED" in output:
                report.append(" Rootkit detected by chkrootkit.")
            else:
                report.append(" chkrootkit found no issues.")
                score += 1
                found = True
        if rkhunter:
            output = subprocess.getoutput("sudo rkhunter --check --sk")
            if "Warning" in output:
                report.append(" rkhunter warning found.")
            else:
                report.append(" rkhunter found no issues.")
                score += 1 if not found else 0.5
    except Exception as e:
        report.append(f" Rootkit check failed: {e}")

def generate_summary():
    report.append("\n Summary:")
    report.append(f"  Compliance Score: {score}/{max_score}")
    if score >= 5:
        report.append(" System is mostly compliant.")
    elif score >= 3:
        report.append(" System needs improvements.")
    else:
        report.append(" System is not compliant.")

def recommend_actions():
    report.append("\n Recommendations:")
    report.append("  - Enable and configure UFW or iptables.")
    report.append("  - Disable unused services (like cups, bluetooth).")
    report.append("  - Harden SSH settings: disable root login, enforce protocol 2.")
    report.append("  - Set proper permissions for sensitive files.")
    report.append("  - Run rootkit scanners regularly.")

if __name__ == "__main__":
    check_firewall()
    check_services()
    check_ssh_settings()
    check_file_permissions()
    check_rootkits()
    generate_summary()
    recommend_actions()

    print("\n".join(report))
    with open("audit_report.txt", "w") as f:
        f.write("\n".join(report))
