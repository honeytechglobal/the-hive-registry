# Byte World 🌐

*A decentralized practice network inspired by DN42 — by Honeytech Solutions Inc.*

---

## Overview

**Byte World** is a private, experimental network designed to simulate real-world Internet operations.
It provides an environment for developers, network engineers, and students to practice:

* BGP routing and AS interconnections
* IPv4/IPv6 address planning
* Anycast deployments
* Running DNS, mail, and web services in a distributed environment
* VPN-based overlay networking

Byte World is **not connected to the public Internet** and is intended for **educational and research purposes only**.

---

## Architecture

* **Transport:** VPN-based (WireGuard, OpenVPN, GRE, or IPsec)
* **Routing:** BGP sessions between Autonomous Systems
* **Addressing:**

  * IPv4: `172.24.0.0/13`
  * IPv6: `fd00::/8` (allocated as `/32` per participant)
* **Registry:** Centralized database for ASN and IP allocations
* **Governance:** Community-driven with minimal rules

---

## Getting Started

### 1. Prerequisites

* A Linux server (VPS, bare-metal, or home lab)
* Installed VPN software (recommended: WireGuard)
* `bird`, `frr`, or `bgpd` for BGP routing
* Basic networking knowledge

### 2. Request Resources

Open an issue in the **[Byte World Registry](registry)** repository with:

```yaml
asn: "650xx"
ipv4: "172.24.x.0/24"
ipv6: "fd00:xxxx::/32"
peering: "WireGuard / OpenVPN"
contact: "you@example.com"
```

You will be assigned:

* An ASN
* IPv4/IPv6 prefixes
* Peering instructions

### 3. Configure VPN

Example WireGuard config:

```ini
[Interface]
PrivateKey = <your_private_key>
Address = 172.24.x.1/24, fd00:xxxx::1/32

[Peer]
PublicKey = <peer_public_key>
Endpoint = peer.example.com:51820
AllowedIPs = 172.24.y.0/24, fd00:yyyy::/32
```

### 4. Configure BGP

Example BIRD config:

```conf
protocol bgp {
    local as 650xx;
    neighbor 172.24.y.1 as 650yy;
    ipv4 {
        import all;
        export all;
    };
    ipv6 {
        import all;
        export all;
    };
}
```

---

## Contribution

We welcome contributions in the following areas:

* Improving documentation
* Building monitoring tools
* Creating automation for registry management
* Running shared services (DNS, NTP, CDN, etc.)

To contribute:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -m "Added feature X"`)
4. Push branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## Rules & Code of Conduct

* No abuse (DDoS, scanning, malware)
* Respect other participants’ allocations
* Keep configs and services stable where possible
* Byte World is **for learning — not production traffic**

---

## Roadmap 🗺️

* [ ] Automated ASN/IP registry with API
* [ ] Web-based portal for peering requests
* [ ] Anycast DNS and CDN service deployment
* [ ] Monitoring stack (Prometheus + Grafana)
* [ ] Documentation site

---

## License

MIT License © 2025 Honeytech Solutions Inc.

---

🚀 **Byte World — your Internet lab without the risks.**

---
