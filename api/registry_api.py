#!/usr/bin/env python3
"""
Byte World Registry API with Prometheus Metrics
"""

import os
import yaml
import ipaddress
from fastapi import FastAPI, HTTPException, Response
from typing import Dict, Any, List
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
    title="Byte World Registry API",
    description="Query ASN, prefix, and service allocations for Byte World",
    version="1.1.0",
)

REGISTRY_PATHS = {
    "asn": "registry/asn",
    "ipv4": "registry/ipv4",
    "ipv6": "registry/ipv6",
    "services": "services",
}

asn_data: Dict[str, Dict[str, Any]] = {}
ipv4_data: Dict[str, Dict[str, Any]] = {}
ipv6_data: Dict[str, Dict[str, Any]] = {}
service_data: Dict[str, List[Dict[str, Any]]] = {}

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter("registry_api_requests_total", "Total API requests", ["endpoint"])
ASN_COUNT = Gauge("registry_asn_total", "Total registered ASNs")
IPV4_COUNT = Gauge("registry_ipv4_prefixes_total", "Total registered IPv4 prefixes")
IPV6_COUNT = Gauge("registry_ipv6_prefixes_total", "Total registered IPv6 prefixes")
SERVICE_COUNT = Gauge("registry_services_total", "Total services by type", ["service_type"])


def load_yaml_file(path: str) -> Any:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_registry():
    """Load all registry data into memory and update metrics"""
    global asn_data, ipv4_data, ipv6_data, service_data
    asn_data.clear()
    ipv4_data.clear()
    ipv6_data.clear()
    service_data.clear()

    # ASN, IPv4, IPv6 records
    for key in ["asn", "ipv4", "ipv6"]:
        base = REGISTRY_PATHS[key]
        if not os.path.exists(base):
            continue
        for root, _, files in os.walk(base):
            for file in files:
                if not file.endswith(".yml"):
                    continue
                path = os.path.join(root, file)
                record = load_yaml_file(path)
                if not record:
                    continue
                if key == "asn":
                    asn_data[record["asn"]] = record
                elif key == "ipv4":
                    ipv4_data[record["ipv4"]] = record
                elif key == "ipv6":
                    ipv6_data[record["ipv6"]] = record

    # Services
    base = REGISTRY_PATHS["services"]
    if os.path.exists(base):
        for root, _, files in os.walk(base):
            for file in files:
                if not file.endswith(".yml"):
                    continue
                path = os.path.join(root, file)
                service_type = file.replace(".yml", "")
                record = load_yaml_file(path)
                if record and "services" in record:
                    service_data[service_type] = record["services"]

    # Update metrics
    ASN_COUNT.set(len(asn_data))
    IPV4_COUNT.set(len(ipv4_data))
    IPV6_COUNT.set(len(ipv6_data))
    for stype, entries in service_data.items():
        SERVICE_COUNT.labels(service_type=stype).set(len(entries))


@app.on_event("startup")
def startup_event():
    load_registry()


# --- API Endpoints ---

@app.get("/asn/{asn}")
def get_asn(asn: str):
    REQUEST_COUNT.labels(endpoint="/asn").inc()
    if asn not in asn_data:
        raise HTTPException(status_code=404, detail="ASN not found")
    return asn_data[asn]


@app.get("/ipv4/{prefix}")
def get_ipv4(prefix: str):
    REQUEST_COUNT.labels(endpoint="/ipv4").inc()
    try:
        ipaddress.ip_network(prefix)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid IPv4 prefix")

    if prefix not in ipv4_data:
        raise HTTPException(status_code=404, detail="IPv4 prefix not found")
    return ipv4_data[prefix]


@app.get("/ipv6/{prefix}")
def get_ipv6(prefix: str):
    REQUEST_COUNT.labels(endpoint="/ipv6").inc()
    try:
        ipaddress.ip_network(prefix)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid IPv6 prefix")

    if prefix not in ipv6_data:
        raise HTTPException(status_code=404, detail="IPv6 prefix not found")
    return ipv6_data[prefix]


@app.get("/services/{stype}")
def get_services(stype: str):
    REQUEST_COUNT.labels(endpoint="/services").inc()
    if stype not in service_data:
        raise HTTPException(status_code=404, detail="Service type not found")
    return service_data[stype]


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {
        "message": "Welcome to Byte World Registry API",
        "endpoints": [
            "/asn/{asn}",
            "/ipv4/{prefix}",
            "/ipv6/{prefix}",
            "/services/{type}",
            "/metrics"
        ]
    }
