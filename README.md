# 🐝 The Hive Network  

The Hive is a community-driven, private network (similar to DN42) created by **Honeytech Solutions**.  
It’s designed for learning, experimentation, and collaboration in **networking, routing, and distributed infrastructure**.  

**Tagline:** “Simple, Innovative, Secure.”

---

## ✨ Features  

- 🔗 Private IPv4 and IPv6 network space  
- 🖧 BGP-based peering between members  
- 📡 Community services (DNS, NTP, CDN, VPN gateways, IXPs)  
- 🔐 Safe environment to learn routing, network automation, and infra ops  
- 🛠 Registry-based IP + ASN allocations with CI validation  

---

## 🔗 Peering  

- **Routing protocol:** BGP  

- **IPv4 address space:** `172.24.0.0/13`  
  - 🔒 Reserved: `172.31.0.0/16` (internal infra + backbone services)  

- **IPv6 address space:** `fd32::/8` (each member gets a `/32`)  
  - 🔒 Reserved:  
    - `fd00:3120::/32` (The Hive backbone services)  
    - `fd31::/16` (IXP & Anycast infra)  
    - `fd32::/16` (future expansion, internal infra)  

- **ASN range:** `64512 – 65534`  

📜 Full reserved block list → [RESERVED.md](RESERVED.md)

---

## 📂 Registry Structure  

```

registry/
├── asn/          # Member ASN records (asn.yml files)
├── ipv4/         # Member IPv4 allocations
├── ipv6/         # Member IPv6 allocations
├── services/     # Declared services (DNS, NTP, CDN, etc.)
└── \_reserved/    # Reserved blocks (IPv4 + IPv6)

````

---

## 🛠 Validator  

The Hive includes a **validator script** that checks:  
- Allocation overlaps  
- Required fields (`asn`, `org`, `contact`)  
- Reserved block enforcement  

Run it locally:  

```bash
pip install pyyaml
python3 tools/validator/validator.py
````

Validator also runs automatically in **GitHub Actions** CI on every commit.

---

## 🚀 How to Join

1. Fork the registry repo
2. Create your allocation request (`asn.yml`, `ipv4.yml`, `ipv6.yml`)
3. Submit a Pull Request
4. Wait for CI validation + maintainer approval
5. Configure BGP peering with The Hive

---

## 📡 Community Services

Members may run and declare services such as:

* Authoritative DNS
* Recursive DNS resolvers
* NTP servers
* Web mirrors
* VPN / transit gateways
* CDNs & IXPs

Service declarations live in:

```
registry/services/
```

---

## 🤝 Governance

* Managed by **Honeytech Solutions**
* Open to networking enthusiasts, students, and operators
* Changes managed via pull requests + CI validation
* Reserved resources are documented in [RESERVED.md](RESERVED.md)

---

## 📧 Contact

* NOC: **[noc@honeytech.net](mailto:noc@honeytech.net)**
* Maintainers: Honeytech Solutions Team

---

🐝 **The Hive** – Learn, build, and collaborate in a safe networking sandbox.

---
