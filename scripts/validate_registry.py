#!/usr/bin/env python3
"""
Byte World Registry Validator
-----------------------------
Validates ASN, IPv4/IPv6 allocations, and service definitions.
Run in CI/CD (GitHub Actions, GitLab CI) to ensure consistency.
"""

import os
import sys
import yaml
import ipaddress

# Allowed service types
DNS_TYPES = {"authoritative", "recursive", "anycast"}
NTP_TYPES = {"stratum1", "stratum2", "anycast"}
CDN_TYPES = {"regional", "anycast", "experimental"}

# Track allocations for uniqueness
asn_set = set()
ipv4_set = set()
ipv6_set = set()


def load_yaml_file(path):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse YAML: {path} ({e})")
        sys.exit(1)


def validate_asn_record(data, path):
    required = ["asn", "org", "contact", "ipv4", "ipv6"]
    for field in required:
        if field not in data:
            print(f"[ERROR] Missing '{field}' in {path}")
            sys.exit(1)

    # ASN uniqueness
    if data["asn"] in asn_set:
        print(f"[ERROR] Duplicate ASN {data['asn']} found in {path}")
        sys.exit(1)
    asn_set.add(data["asn"])

    # Validate IP formats
    try:
        ipaddress.ip_network(data["ipv4"])
    except Exception:
        print(f"[ERROR] Invalid IPv4 prefix in {path}: {data['ipv4']}")
        sys.exit(1)

    try:
        ipaddress.ip_network(data["ipv6"])
    except Exception:
        print(f"[ERROR] Invalid IPv6 prefix in {path}: {data['ipv6']}")
        sys.exit(1)

    # Prefix uniqueness
    if data["ipv4"] in ipv4_set:
        print(f"[ERROR] Duplicate IPv4 allocation {data['ipv4']} in {path}")
        sys.exit(1)
    if data["ipv6"] in ipv6_set:
        print(f"[ERROR] Duplicate IPv6 allocation {data['ipv6']} in {path}")
        sys.exit(1)

    ipv4_set.add(data["ipv4"])
    ipv6_set.add(data["ipv6"])


def validate_service_record(service_type, data, path):
    if "type" not in data:
        print(f"[ERROR] Missing 'type' in {path}")
        sys.exit(1)

    valid_types = {
        "dns": DNS_TYPES,
        "ntp": NTP_TYPES,
        "cdn": CDN_TYPES
    }

    if service_type not in valid_types:
        print(f"[ERROR] Unknown service file {path}")
        sys.exit(1)

    if data["type"] not in valid_types[service_type]:
        print(f"[ERROR] Invalid {service_type} type '{data['type']}' in {path}")
        sys.exit(1)

    # Validate IP addresses
    if "ipv4" in data:
        try:
            ipaddress.ip_address(data["ipv4"])
        except Exception:
            print(f"[ERROR] Invalid IPv4 in {path}: {data['ipv4']}")
            sys.exit(1)

    if "ipv6" in data:
        try:
            ipaddress.ip_address(data["ipv6"])
        except Exception:
            print(f"[ERROR] Invalid IPv6 in {path}: {data['ipv6']}")
            sys.exit(1)


def main():
    base_dirs = ["registry/asn", "registry/ipv4", "registry/ipv6", "services"]
    for base in base_dirs:
        if not os.path.exists(base):
            continue
        for root, _, files in os.walk(base):
            for file in files:
                if not file.endswith(".yml"):
                    continue
                path = os.path.join(root, file)
                data = load_yaml_file(path)

                # Services contain a list, others are single dict
                if base.startswith("services"):
                    service_type = os.path.basename(file).replace(".yml", "")
                    if not data or "services" not in data:
                        print(f"[ERROR] Missing 'services' list in {path}")
                        sys.exit(1)
                    for svc in data["services"]:
                        validate_service_record(service_type, svc, path)
                else:
                    if not data:
                        print(f"[ERROR] Empty file: {path}")
                        sys.exit(1)
                    validate_asn_record(data, path)

    print("[OK] Registry validation passed ✅")


if __name__ == "__main__":
    main()
