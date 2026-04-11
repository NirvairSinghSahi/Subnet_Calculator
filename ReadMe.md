# CPAN226 Network Programming - Final Project Report

## Cover Page

- **Project Title:** Online/Web-based IPv4 Subnet Calculator
- **Course:** CPAN226 - Network Programming
- **Team Members:**
  - Nirvair Singh Sahi
  - Maninder Kaur
  - Chanpreet Singh
- **Submission Type:** Group Project Final Report
- **Date:** 2026-04-08

---

## Table of Contents

1. Introduction
2. Background and Literature Review
3. Design and Implementation
4. Results and Discussion
5. Conclusion
6. References (IEEE Style)


---

## 1. Introduction

The objective of this project is to design and implement an online/web-based IPv4 Subnet Calculator to support networking students and professionals in performing subnet calculations quickly and accurately.

The main goals of this project are:

- Provide a simple and intuitive web interface for subnet calculation inputs.
- Support common subnetting input methods such as network prefix length and subnet mask.
- Allow subnet planning by number of subnets, host bits, or hosts required per subnet.
- Display subnetting results instantly in a clear and organized format.

---

## 2. Background and Literature Review

IPv4 subnetting is a key concept in network design and management. Subnetting helps divide a large network into smaller logical segments to improve address utilization, routing efficiency, and security.

Important background concepts used in this project include:

- **IPv4 Addressing:** 32-bit addressing format represented in dotted decimal form.
- **Subnet Masking and CIDR:** Methods to define network and host portions of an IP address.
- **Broadcast and Usable Host Ranges:** Determining first and last assignable host addresses in each subnet.

Existing online subnet calculators were reviewed to understand standard UI patterns and output formats. Based on this review, the application design emphasizes simplicity, validation, and accurate subnet-level outputs.

---

## 3. Design and Implementation

### 3.1 Project Architecture / Topology

The project follows a client-server web architecture:

- **Client Device (Web Browser):** User enters subnet parameters and views results.
- **Web Application Server (Python Flask):** Processes user requests and performs subnet calculations.
- **Calculation Module (IPv4 Subnet Logic):** Computes subnet mask, subnet list, host ranges, and broadcast addresses.


### 3.2 Functional Modules and Functionalities

1. **Input Module**
   - Accepts network address.
   - Accepts network mask or prefix length.
   - Accepts one subnetting method:
     - number of subnets, or
     - number of host bits, or
     - number of hosts per subnet.

2. **Validation Module**
   - Validates IPv4 address format.
   - Validates subnet mask and prefix length ranges.
   - Validates numeric input constraints.

3. **Subnet Calculation Module**
   - Computes new subnet mask.
   - Calculates total number of subnets.
   - Generates subnet-wise details:
     - network address
     - broadcast address
     - first usable host
     - last usable host
     - total hosts per subnet

4. **Output Module**
   - Displays summarized values and subnet table in browser.
   - Shows user-friendly error messages when input is invalid.

### 3.3 Implementation Steps and Configuration

1. Set up Python environment and project files.
2. Install required package(s) from `requirements.txt`.
3. Develop backend logic in `subnet_calculator.py`.
4. Build frontend template in `templates/index.html`.
5. Add styling in `static/style.css`.
6. Test with multiple subnet input scenarios.
7. Run locally using:
   - `pip install -r requirements.txt`
   - `python subnet_calculator.py`
   - Access via `http://localhost:5000`

---

## 4. Results and Discussion

The implemented web application produces subnetting results in real time after user input. The system correctly displays:

- New subnet mask
- Total number of subnets
- Subnet-by-subnet network and broadcast addresses
- First and last usable IP addresses per subnet
- Total hosts per subnet

### Screenshots for Final Submission

Included screenshots of:

1. Input interface before calculation
2. Successful calculation output table
3. Invalid input example and validation message
4. Different subnetting mode outputs (subnets/host bits/hosts per subnet)

### Discussion

The application meets the project objective by providing a simple UI and accurate subnet results. The use of a Python web framework enables easy deployment and modular structure for future enhancements.

---

## 5. Conclusion

This project helped the team strengthen understanding of:

- IPv4 addressing and subnetting logic
- CIDR and subnet mask conversion
- Web application development with Python
- Input validation and user-centered output design

### Challenges Faced

- Correctly deriving subnet boundaries for multiple input methods
- Handling edge cases in host calculations
- Designing a clean and readable web interface for technical output

### Future Work

- Add Variable Length Subnet Masking (VLSM) support
- Add IPv6 subnet calculator support
- Add export options (CSV/PDF) for subnet reports
- Improve visualization with subnet diagrams/charts

### Team Member Contributions

- **Nirvair Singh Sahi:** Project coordination, backend subnet calculation logic, deployment support
- **Maninder Kaur:** Frontend UI design, testing, report documentation
- **Chanpreet Singh:** Input validation, debugging, result verification and quality checks

---

## 6. References (IEEE Style)

[1] A. S. Tanenbaum and D. J. Wetherall, *Computer Networks*, 5th ed. Boston, MA, USA: Pearson, 2011.  
[2] W. Stallings, *Data and Computer Communications*, 10th ed. Boston, MA, USA: Pearson, 2013.  
[3] Python Software Foundation, "ipaddress - IPv4/IPv6 manipulation library," Python Docs. [Online]. Available: https://docs.python.org/3/library/ipaddress.html  
[4] Flask Documentation, "Flask Web Development Framework." [Online]. Available: https://flask.palletsprojects.com/

---

