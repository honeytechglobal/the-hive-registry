# Byte World Services Registry 🚀

The **services registry** tracks all shared infrastructure services available on the Byte World network.
This is similar to how the real Internet uses registries for DNS root servers, NTP pools, and CDN nodes.

Participants can register services they operate so others know how to connect, peer, or use them.

---

## Directory Structure

```
services/
├── dns.yml      # Authoritative, recursive, and Anycast DNS servers
├── ntp.yml      # Stratum1, stratum2, and Anycast NTP servers
├── cdn.yml      # Anycast/regional CDN nodes
└── README.md    # This file
```

---

## Service Types

### 1. DNS (`dns.yml`)

* **authoritative** → Hosts zones (e.g., `byteworld.arpa`)
* **recursive** → Provides DNS resolution for Byte World members
* **anycast** → Distributed nodes sharing the same IPs

See: [`dns.yml`](dns.yml)

---

### 2. NTP (`ntp.yml`)

* **stratum1** → Connected to hardware time sources (GPS, PTP, etc.)
* **stratum2** → Syncs from stratum1 servers
* **anycast** → Distributed pool of NTP servers with the same IPs

See: [`ntp.yml`](ntp.yml)

---

### 3. CDN (`cdn.yml`)

* **regional** → A single-location caching/proxy server
* **anycast** → Globally distributed CDN nodes announced via BGP
* **experimental** → Testing deployments, not production-like

See: [`cdn.yml`](cdn.yml)

---

## How to Add a Service

1. Fork this repository
2. Open the correct YAML file (e.g., `dns.yml`, `ntp.yml`, `cdn.yml`)
3. Copy an existing entry and modify it with your details:

```yaml
- name: "MyLab DNS"
  operator: "MyLabNet (ASN 65042)"
  contact: "admin@mylab.net"
  type: "recursive"
  location: "Cape Town, South Africa"
  ipv4: "172.24.42.53"
  ipv6: "fd00:42::53"
  notes: |
    Recursive resolver available to all Byte World participants.
    Limited to 100 queries/sec per client.
```

4. Commit and submit a **Pull Request (PR)**
5. A maintainer will review and merge your entry

---

## Rules

* Only register **services that are stable** and intended for community use
* Use correct `type` values (`authoritative`, `recursive`, `anycast`, etc.)
* Add meaningful `notes` so others know how the service behaves
* Abuse or unstable services may be removed

---

## Future Services

The following may be added in the future:

* `services/vpn.yml` → Registry of public VPN endpoints for participants
* `services/mail.yml` → Experimental mail relays and MX servers
* `services/monitoring.yml` → Prometheus/Grafana monitoring nodes

---

✅ By documenting services here, Byte World ensures transparency and easy access for all participants.

---
