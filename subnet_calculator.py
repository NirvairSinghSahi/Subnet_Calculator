"""
Subnet Calculator - CPAN226 Network Programming Project
A web-based subnet calculator built with Python and Streamlit.
"""

import streamlit as st
import ipaddress


def validate_ip(ip_str: str) -> bool:
    """Validate if the given string is a valid IPv4 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def cidr_to_subnet_mask(cidr: int) -> str:
    """Convert CIDR notation to dotted decimal subnet mask."""
    if cidr < 0 or cidr > 32:
        return "Invalid"
    mask = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
    return ".".join(
        str((mask >> (8 * (3 - i))) & 0xFF) for i in range(4)
    )


def subnet_mask_to_cidr(mask_str: str) -> int:
    """Convert dotted decimal subnet mask to CIDR notation."""
    try:
        mask = ipaddress.ip_address(mask_str)
        binary = bin(int(mask))[2:].zfill(32)
        return binary.count("1")
    except (ValueError, ipaddress.AddressValueError):
        return -1


def calculate_subnet(ip_str: str, cidr: int):
    """Calculate all subnet information for the given IP and CIDR."""
    try:
        network = ipaddress.ip_network(f"{ip_str}/{cidr}", strict=False)
    except ValueError as e:
        return None, str(e)

    results = {
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "subnet_mask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "cidr_notation": f"{network.network_address}/{cidr}",
        "total_hosts": network.num_addresses,
        "usable_hosts": max(0, network.num_addresses - 2),
        "first_host": str(list(network.hosts())[0]) if network.num_addresses > 1 else "N/A",
        "last_host": str(list(network.hosts())[-1]) if network.num_addresses > 1 else "N/A",
        "ip_class": get_ip_class(ip_str),
        "subnet_binary": format(int(network.netmask), "032b"),
        "ip_binary": format(int(ipaddress.ip_address(ip_str)), "032b"),
    }
    return results, None


def get_ip_class(ip_str: str) -> str:
    """Determine the class of an IP address (classful addressing)."""
    first_octet = int(ip_str.split(".")[0])
    if first_octet < 128:
        return "Class A"
    elif first_octet < 192:
        return "Class B"
    elif first_octet < 224:
        return "Class C"
    elif first_octet < 240:
        return "Class D (Multicast)"
    else:
        return "Class E (Reserved)"


def main():
    st.set_page_config(
        page_title="Subnet Calculator",
        page_icon="🌐",
        layout="centered",
    )

    st.title("🌐 Subnet Calculator")
    st.markdown("*CPAN226 Network Programming Project*")
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        ip_input = st.text_input(
            "IP Address",
            value="192.168.1.0",
            placeholder="e.g., 192.168.1.0",
            help="Enter a valid IPv4 address",
        )

    with col2:
        mask_option = st.radio(
            "Mask input",
            ["CIDR (/)", "Subnet Mask"],
            horizontal=True,
        )

    if mask_option == "CIDR (/)":
        cidr = st.slider("CIDR Prefix", 0, 32, 24)
    else:
        mask_input = st.text_input(
            "Subnet Mask",
            value="255.255.255.0",
            placeholder="e.g., 255.255.255.0",
        )
        cidr = subnet_mask_to_cidr(mask_input) if mask_input else 24
        if cidr < 0 and mask_input:
            st.error("Invalid subnet mask. Use format: 255.255.255.0")

    if st.button("Calculate", type="primary"):
        if not validate_ip(ip_input):
            st.error("❌ Please enter a valid IPv4 address")
        elif cidr < 0 or cidr > 32:
            st.error("❌ Invalid CIDR or subnet mask")
        else:
            results, error = calculate_subnet(ip_input, cidr)
            if error:
                st.error(f"❌ {error}")
            else:
                st.success("✅ Subnet calculated successfully!")
                st.divider()

                st.subheader("📊 Results")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Network Address", results["network_address"])
                    st.metric("Broadcast Address", results["broadcast_address"])
                    st.metric("First Usable Host", results["first_host"])
                    st.metric("Last Usable Host", results["last_host"])

                with col_b:
                    st.metric("Subnet Mask", results["subnet_mask"])
                    st.metric("Wildcard Mask", results["wildcard_mask"])
                    st.metric("Total Hosts", results["total_hosts"])
                    st.metric("Usable Hosts", results["usable_hosts"])

                st.info(f"**CIDR Notation:** {results['cidr_notation']} | **IP Class:** {results['ip_class']}")

                with st.expander("🔢 Binary Representation"):
                    st.code(f"IP Address:  {results['ip_binary']}\nSubnet Mask: {results['subnet_binary']}", language=None)

    st.divider()
    st.caption("Built with Python & Streamlit | CPAN226 Network Programming")

if __name__ == "__main__":
    main()
