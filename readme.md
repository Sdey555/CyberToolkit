# 🛡️ CyberToolkit

CyberToolkit is a modular cybersecurity toolkit written in Python. The project is built to learn networking, cybersecurity, and software engineering by implementing practical security tools from scratch.

Each module is developed incrementally with a focus on clean architecture, object-oriented design, and reusable components.

---

## ✨ Current Features

### 🔍 Port Scanner

- TCP Connect Scan
- Scan custom port ranges
- Scan common ports
- Hostname to IP resolution
- Multithreaded scanning using `ThreadPoolExecutor`
- Configurable timeout
- Configurable worker threads
- Service identification
- Generic TCP banner grabbing
- HTTP Server banner detection
- Port latency measurement
- Scan statistics
- Custom exception handling

### 🌐 DNS Lookup

Supports DNS enumeration for:

- A Records
- AAAA Records
- MX Records
- NS Records
- CNAME Records
- PTR (Reverse DNS) Records

Additional features:

- Custom DNS exception handling
- Reverse DNS lookup
- Object-oriented modular design

---

## 📂 Project Structure

```text
CyberToolkit/
│
├── core/
│   ├── controller.py
│   └── exceptions.py
│
├── cli/
│   ├── input.py
│   ├── output.py
│   └── user_menu.py
│
├── modules/
│   ├── port_scanner/
│   │   ├── scanner.py
│   │   ├── banner.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── exceptions.py
│   │
│   └── dns_lookup/
│       ├── dns_lookup.py
│       ├── models.py
│       └── exceptions.py
│
├── assets/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/Sdey555/CyberToolkit.git
cd CyberToolkit
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## 📸 Example Output

### Main Menu

![Main Menu](assets/menu.png)

### Port Scanner

![Port Scanner](assets/port_scanner.png)

### DNS Lookup

![DNS Lookup](assets/dns_lookup.png)

---

## 🛠️ Technologies Used

- Python 3
- socket
- dnspython
- concurrent.futures
- dataclasses
- Object-Oriented Programming (OOP)
- Git & GitHub

---

## 🎯 Learning Objectives

This project is helping me learn:

- Network Programming
- Cybersecurity Fundamentals
- Python Software Engineering
- Object-Oriented Design
- Modular Application Design
- Exception Handling
- Multithreading
- DNS Protocol
- Clean Code Practices
- Git Workflow & Versioning

---

## 🚧 Roadmap

### Completed

- ✅ Multithreaded TCP Port Scanner
- ✅ DNS Lookup Module

### Planned

- 🔜 WHOIS Lookup
- 🔜 SSL Certificate Inspector
- 🔜 Ping Utility
- 🔜 Traceroute
- 🔜 HTTP Header Analyzer
- 🔜 Hash Utilities
- 🔜 Password Utilities

---

## ⚠️ Disclaimer

CyberToolkit is intended for educational and authorized security testing purposes only.

Only use this software on systems you own or have explicit permission to assess.

---

## 👨‍💻 Author

**Shuvadip Dey**

Computer Science & Engineering Student

Building CyberToolkit as a long-term learning project in networking, cybersecurity, and software engineering.