#!/usr/bin/env python3
import os
import sys
import yaml
import ipaddress

REGISTRY_DIR = "registry"

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def validate_asn(data, path):
    required = ["asn", "org", "contact"]
    for field in required:
        if field not in data:
            print(f"[ERROR] {path} missing field: {field}")
            return False
    return True

def validate_prefix(prefix, path):
    try:
        ipaddress.ip_network(prefix)
        return True
    except ValueError:
        print(f"[ERROR] {path} invalid prefix: {prefix}")
        return False

def main():
    success = True
    for root, _, files in os.walk(REGISTRY_DIR):
        for file in files:
            if file.endswith(".yml"):
                path = os.path.join(root, file)
                try:
                    data = load_yaml(path)
                except Exception as e:
                    print(f"[ERROR] {path} failed to parse: {e}")
                    success = False
                    continue

                # ASN validation
                if "asn" in root:
                    if not validate_asn(data, path):
                        success = False

                # IPv4 / IPv6 validation
                if "ipv4" in root and "ipv4" in data:
                    if not validate_prefix(data["ipv4"], path):
                        success = False
                if "ipv6" in root and "ipv6" in data:
                    if not validate_prefix(data["ipv6"], path):
                        success = False

    if success:
        print("[OK] Registry validation passed ✅")
        sys.exit(0)
    else:
        print("[FAIL] Registry validation failed ❌")
        sys.exit(1)

if __name__ == "__main__":
    main()
