# 🔐 Linux Hardening Audit Tool

A lightweight Python-based script to **audit a Linux system's security configuration**, evaluate it based on **CIS Benchmarks**, and provide actionable hardening recommendations.

---

## 📌 Objective

To help system administrators and cybersecurity enthusiasts:

* Identify misconfigurations
* Evaluate system security
* Improve Linux hardening practices

---

## 🛠️ Features

* ✅ **Firewall Check** (UFW / iptables)
* ✅ **Unused Services Detection**
* ✅ **SSH Configuration Audit**
* ✅ **Sensitive File Permissions Audit**
* ✅ **Rootkit Detection** using `chkrootkit` / `rkhunter`
* ✅ **Compliance Scoring** (out of 6)
* ✅ **Hardening Recommendations**
* ✅ Generates `audit_report.txt` in plain text

---

## 🚀 Getting Started

### 📦 Prerequisites

Make sure your system has the following installed:

```bash
sudo apt update
sudo apt install python3 ufw chkrootkit rkhunter -y
```

---

### ▶️ Run the Script

```bash
sudo python3 linux_audit.py
```

> ⚠️ Run as `sudo` to allow checks that require root privileges.

---

## 📂 Output

* A detailed **audit report** will be saved as:

  ```bash
  audit_report.txt
  ```
* Report includes:

  * Security configuration status
  * Compliance score (out of 6)
  * Recommendations for each failed check

---

## 📊 Compliance Criteria (CIS-based)

| Check                                    | Points |
| ---------------------------------------- | ------ |
| Firewall Enabled                         | 1      |
| Unused Services Disabled                 | 1      |
| Secure SSH Settings                      | 1      |
| File Permissions (/etc/shadow)           | 0.5    |
| File Permissions (/etc/passwd)           | 0.5    |
| Rootkit Clean (`chkrootkit`, `rkhunter`) | 2      |
| **Total**                                | **6**  |

---

## 📎 Sample Usage

```bash
sudo python3 linux_audit.py
cat audit_report.txt
```

---

## 📌 Recommendations Included

The tool suggests hardening actions such as:

* Enabling UFW/iptables
* Disabling unnecessary services
* Hardening SSH settings
* Correcting file permissions
* Running rootkit scans regularly

---

## 📁 Files

* `linux_audit.py` – Main audit script
* `audit_report.txt` – Generated system audit report

---

## 🤝 Contributing

Feel free to fork the repo and contribute with more CIS checks, advanced scoring, or multi-format reports (e.g., PDF, HTML).

---

## 📜 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

