# 🌐 Subnet Calculator

> **CPAN226 · Network Programming**  
> A web-based subnet calculator built with Python and Streamlit.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Network info** | Network address, broadcast address, first & last usable host |
| **Flexible input** | CIDR notation (e.g. `/24`) or subnet mask (e.g. `255.255.255.0`) |
| **Validation** | IP address validation before calculation |
| **Masks** | Subnet mask and wildcard mask |
| **Host counts** | Total and usable number of hosts |
| **IP class** | Class A, B, C, D, or E |
| **Binary view** | Binary representation of IP and subnet mask |

---

## 🚀 Quick Start

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the app**

```bash
python -m streamlit run subnet_calculator.py
```

**3. Open in browser** → [http://localhost:8501](http://localhost:8501)

---

## 📖 Usage

1. Enter an **IPv4 address** (e.g. `192.168.1.0`).
2. Choose **CIDR** or **Subnet Mask** as input type.
3. Set the prefix (e.g. `/24`) or type the mask (e.g. `255.255.255.0`).
4. Click **Calculate** to see the results.

---

## 📁 Project Structure

```
Subnet_Calculator/
├── subnet_calculator.py   # Main Streamlit application
├── requirements.txt       # Python dependencies
├── start_subnet_calculator.bat   # Optional: double-click to run
└── README.md
```

---

## 🔧 Optional: Virtual Environment

Use a virtual environment to keep dependencies isolated:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

---

## 📄 License & Course

Project for **CPAN226 Network Programming**.
