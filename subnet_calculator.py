"""Web-based IPv4 subnet calculator using Flask."""

import ipaddress
import math
from flask import Flask, render_template, request

app = Flask(__name__)


def subnet_mask_to_cidr(mask_str: str) -> int:
    """Convert dotted decimal subnet mask to CIDR notation."""
    try:
        mask_int = int(ipaddress.IPv4Address(mask_str))
        binary = format(mask_int, "032b")
        if "01" in binary:
            return -1
        return binary.count("1")
    except ipaddress.AddressValueError:
        return -1


def _hosts_per_subnet(prefix_len: int) -> int:
    size = 2 ** (32 - prefix_len)
    return max(0, size - 2)


def _derive_new_prefix(base_prefix: int, mode: str, raw_value: str):
    """
    Determine new subnet prefix from selected subnetting mode.

    Modes:
    - subnets: number of required subnets
    - host_bits: number of host bits in each subnet
    - hosts_per_subnet: required usable hosts in each subnet
    """
    try:
        value = int(raw_value)
    except ValueError:
        return None, "Selected value must be an integer."

    if mode == "subnets":
        if value < 1:
            return None, "Number of subnets must be at least 1."
        borrow_bits = math.ceil(math.log2(value))
        new_prefix = base_prefix + borrow_bits
        if new_prefix > 32:
            return None, "Cannot create that many subnets from this base network."
        return new_prefix, None

    if mode == "host_bits":
        if value < 0 or value > 32:
            return None, "Host bits must be between 0 and 32."
        new_prefix = 32 - value
        if new_prefix < base_prefix:
            return None, "Host bits are too large for the selected base network."
        return new_prefix, None

    if mode == "hosts_per_subnet":
        if value < 0:
            return None, "Hosts per subnet cannot be negative."
        host_bits = math.ceil(math.log2(value + 2)) if value > 0 else 1
        new_prefix = 32 - host_bits
        if new_prefix < base_prefix:
            return None, "Base network is too small for requested hosts per subnet."
        return new_prefix, None

    return None, "Invalid subnetting mode."


def calculate_subnets(ip_str: str, base_prefix: int, mode: str, value: str):
    try:
        base_network = ipaddress.ip_network(f"{ip_str}/{base_prefix}", strict=False)
    except ValueError as exc:
        return None, str(exc)

    new_prefix, error = _derive_new_prefix(base_prefix, mode, value)
    if error:
        return None, error
    if new_prefix < base_network.prefixlen:
        return None, "New subnet prefix cannot be less specific than base prefix."

    subnet_list = list(base_network.subnets(new_prefix=new_prefix))
    total_subnets = len(subnet_list)
    if total_subnets > 4096:
        return None, "Too many subnets to display. Please use a smaller split."

    rows = []
    for subnet in subnet_list:
        hosts = list(subnet.hosts())
        first_host = str(hosts[0]) if hosts else "N/A"
        last_host = str(hosts[-1]) if hosts else "N/A"
        rows.append(
            {
                "network_address": str(subnet.network_address),
                "broadcast_address": str(subnet.broadcast_address),
                "first_usable_ip": first_host,
                "last_usable_ip": last_host,
                "total_hosts": _hosts_per_subnet(subnet.prefixlen),
            }
        )

    return {
        "new_subnet_mask": str(ipaddress.ip_network(f"0.0.0.0/{new_prefix}").netmask),
        "total_subnets": total_subnets,
        "subnets": rows,
    }, None


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    results = None
    form = {
        "network_address": "192.168.1.0",
        "mask_mode": "cidr",
        "prefix_length": "24",
        "network_mask": "255.255.255.0",
        "calc_mode": "subnets",
        "num_subnets": "4",
        "host_bits": "6",
        "hosts_per_subnet": "62",
    }

    if request.method == "POST":
        form["network_address"] = request.form.get("network_address", "").strip()
        form["mask_mode"] = request.form.get("mask_mode", "cidr")
        form["prefix_length"] = request.form.get("prefix_length", "24").strip()
        form["network_mask"] = request.form.get("network_mask", "255.255.255.0").strip()
        form["calc_mode"] = request.form.get("calc_mode", "subnets")
        form["num_subnets"] = request.form.get("num_subnets", "1").strip()
        form["host_bits"] = request.form.get("host_bits", "8").strip()
        form["hosts_per_subnet"] = request.form.get("hosts_per_subnet", "2").strip()

        try:
            ipaddress.IPv4Address(form["network_address"])
        except ipaddress.AddressValueError:
            error = "Please enter a valid IPv4 address."
            return render_template("index.html", error=error, results=results, form=form)

        if form["mask_mode"] == "mask":
            base_prefix = subnet_mask_to_cidr(form["network_mask"])
            if base_prefix < 0:
                error = "Invalid subnet mask. Example: 255.255.255.0"
                return render_template("index.html", error=error, results=results, form=form)
        else:
            try:
                base_prefix = int(form["prefix_length"])
                if not 0 <= base_prefix <= 32:
                    raise ValueError
            except ValueError:
                error = "Network prefix length must be a number between 0 and 32."
                return render_template("index.html", error=error, results=results, form=form)

        if form["calc_mode"] == "subnets":
            input_value = form["num_subnets"]
        elif form["calc_mode"] == "host_bits":
            input_value = form["host_bits"]
        else:
            input_value = form["hosts_per_subnet"]

        results, calc_error = calculate_subnets(
            form["network_address"],
            base_prefix,
            form["calc_mode"],
            input_value,
        )
        if calc_error:
            error = calc_error

    return render_template("index.html", error=error, results=results, form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
