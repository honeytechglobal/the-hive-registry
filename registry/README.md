# Byte World Registry 📖

The **Byte World Registry** is the authoritative source for:

* ASN allocations
* IPv4/IPv6 prefix assignments
* Peering and service metadata

This repository ensures consistency across the Byte World network and acts like a miniature version of a real Internet registry (similar to RIR/IRR).

---

## Directory Structure

```
registry/
├── asn/           # Autonomous System (ASN) records
│   ├── 65001.yml
│   ├── 65002.yml
│   └── ...
├── ipv4/          # IPv4 prefix allocations
│   ├── 172.24.1.0-24.yml
│   └── ...
├── ipv6/          # IPv6 prefix allocations
│   ├── fd00-1234--48.yml
│   └── ...
├── services/      # Optional services (DNS, NTP, CDN, etc.)
│   ├── dns.yml
│   ├── ntp.yml
│   └── ...
└── README.md      # This file
```

---

## How to Request Resources

1. **Fork this repository**
2. **Copy the template**: [`registry.yml`](../registry.yml)
3. Fill in your details (ASN, IPs, VPN info, BGP neighbors, services)
4. Save the file under the correct directory:

   * `asn/650xx.yml` → your ASN record
   * `ipv4/172.24.x.0-24.yml` → your IPv4 prefix
   * `ipv6/fd00-xxxx--48.yml` → your IPv6 prefix
   * `services/<service>.yml` → if you are running a shared service
5. Commit and submit a **Pull Request (PR)**

Maintainers will review and approve your allocation.

---

## Example

**File:** `asn/65010.yml`

```yaml
asn: "65010"
org: "ExampleNet"
contact: "admin@example.net"
location: "Nairobi, Kenya"
ipv4: "172.24.10.0/24"
ipv6: "fd00:10::/48"
vpn:
  type: "WireGuard"
  endpoint: "example.net:51820"
  pubkey: "base64key=="
  tunnel_ipv4: "10.10.10.1/30"
  tunnel_ipv6: "fd00:10::1/64"
bgp:
  router_id: "172.24.10.1"
  neighbors:
    - asn: "65020"
      ipv4: "172.24.20.1"
      ipv6: "fd00:20::1"
services:
  dns: true
  ntp: false
  web: false
notes: |
  Running an experimental Anycast DNS service.
```

---

## Services

Shared services are tracked under `registry/services/`.
Examples:

* `dns.yml` → authoritative/recursive DNS servers
* `ntp.yml` → time servers
* `cdn.yml` → Anycast CDN nodes

If you run a service, document it here so others can peer or use it.

---

## Rules

* Prefixes must not overlap with other allocations
* ASN must be unique (65000–65534 range)
* Services should be **optional** and **documented**
* PRs must follow the template

---

## Future Plans

* Automated validation of YAML files (CI)
* API for querying ASN/prefix allocations
* Web portal for registry browsing

---

✅ This registry is the **source of truth** for Byte World allocations.
Contribute responsibly and keep the data accurate.

---
