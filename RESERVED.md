# 🛑 The Hive Reserved Address Space

Certain IPv4 and IPv6 ranges are **reserved** for internal infrastructure, backbone services, IXPs, and future expansion.  
These prefixes **must not be allocated to members** unless explicitly noted.

---

## 📡 IPv4 Reserved Blocks

| Prefix          | Purpose                                |
|-----------------|----------------------------------------|
| 172.31.0.0/16   | The Hive backbone, infra & special use |

---

## 🌍 IPv6 Reserved Blocks

| Prefix            | Purpose                                    |
|-------------------|--------------------------------------------|
| fd00:3120::/32    | The Hive backbone services & infra         |
| fd31::/16         | IXP services & anycast infrastructure      |
| fd32::/16         | Future expansion & internal infrastructure |

---

## ✅ Notes

- Reserved blocks use **ASN = 0** in the registry.  
- They are tracked in `registry/ipv4/_reserved*.yml` and `registry/ipv6/_reserved*.yml`.  
- The **validator enforces** that no member allocations fall within these ranges.  
- If you believe you need addresses from a reserved block (e.g., to participate in an IXP project), open an issue or contact **noc@honeytech.net**.
