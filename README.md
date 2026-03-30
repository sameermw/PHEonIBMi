# IBM i Proof of Concept: Partially Homomorphic Encryption (PHE)

This repository contains a suite of Python-based test cases for implementing **Partially Homomorphic Encryption (PHE)** on IBM i Power Systems. The objective of this POC was to validate the feasibility, performance, and mathematical accuracy of performing "Blind Calculation" on sensitive data within the PASE environment.

## 📋 Environment Specifications
* **Platform:** IBM i (Power Systems)
* **Environment:** PASE (Portable Application Solutions Environment)
* **Language:** Python 3.9
* **Core Libraries:** `lightphe`, `phe`, `tabulate` (for reporting)

---

## 🚀 Test Case Catalog

### Script Reference: Specialized Traces & Core Tests

This section detail the scripts used to "pull back the curtain" on the mathematical operations occurring within the PASE environment.

#### **1. Core Library Validation**
* **`test_phe.py`**:
    * **Focus**: Validates the standard Paillier implementation.
    * **Goal**: Ensures the `phe` library can successfully generate 2048-bit keys and perform basic additive cycles without memory leaks in the Python 3.9 environment.
* **`test_lightphe.py`**:
    * **Focus**: Sanity check for the `lightphe` abstraction layer.
    * **Goal**: Iterates through a "Hello World" encryption/decryption cycle for all registered algorithms to ensure no missing shared libraries (.so files) in PASE.

#### **2. Execution Traces (The "Under the Hood" Series)**
These scripts include verbose logging to explain the internal modular arithmetic steps to the developer.

* **`trace_phe.py` / `trace_lightphe.py`**:
    * **Purpose**: These scripts print the step-by-step transformation of data.
    * **Feature**: They display the "Multiplication is Addition" paradox. You will see the two massive ciphertext integers being multiplied together to result in a decrypted sum.
    * **Use Case**: Ideal for demonstrating the process to System Architects who are skeptical of how "blind math" functions.

* **`trace_ec_elgamal.py`**:
    * **Purpose**: Specifically traces **Elliptic Curve** operations.
    * **Feature**: Unlike the integer-based Paillier, this traces points on a curve $(x, y)$. It demonstrates how the library maps a message to a curve point and performs point addition.
    * **Observation**: This script highlights why ECC is often faster for Key Generation but computationally "noisier" during complex advanced math.

---

### 🛠️ How to Use the Traces
To see the step-by-step mathematical logic for the Elliptic Curve implementation, run:

```bash
python3 trace_ec_elgamal.py
```

**What to look for in the output:**
1.  **The Public Key Point**: A large coordinate representing your "Lock."
2.  **The Ciphertext Pair**: Two distinct coordinates $(C1, C2)$ that hide your data.
3.  **The Decryption Latency**: The time taken to solve the "Discrete Log" for the specific EC curve used (typically `secp256k1`).

---

### 3. The Multi-Algorithm Benchmark
**File:** `benchmark_script.py`  
**Purpose:** Evaluates 10+ algorithms (RSA, Paillier, ElGamal, ECC) to find the most efficient fit for Power Systems.  
**Key Findings:** * **Exponential-ElGamal** is the fastest for encryption on IBM i.
* **Benaloh** is unsuitable due to extreme Key Generation latency (>600s).
* **ECC-ElGamal** offers small ciphertexts but slightly higher mathematical overhead.

### 4. The Real-World Payroll Simulation
**File:** `payroll_sim.py`  
**Purpose:** Simulates an end-to-end business process: encrypting a list of salaries and calculating a "Blind Total."  
**Key Findings:** * Confirmed that **Additive Homomorphism** allows for nearly instant summation of encrypted records.
* Identified the **Decryption Bottleneck** in ElGamal (Discrete Log search takes ~1.3s for large totals).

### 5. The Persistence & IFS Vault
**File:** `secure_storage_sim.py`  
**Purpose:** Demonstrates how to serialize encrypted objects into **Binary Blobs** for storage in the Integrated File System (IFS).  
**Key Findings:** * Ciphertexts can be stored as `BLOB` data in Db2 or as `.dat` files in the IFS using Python’s `pickle` module.

### 6. Advanced Math & Precision Scaling
**File:** `advanced_elgamal_math.py`  
**Purpose:** Investigates linear equations $(Price \times Qty \times Tax) - Discount$ and identifies the "Off-by-One" precision error.  
**Key Findings:** * **Method 1 (Tax Factor):** Revealed a $+1$ integer drift due to numerical noise in high-exponent modular math.
* **Method 2 (Basis Points):** Proved that **Integer Scaling** (e.g., multiplying by 100 to handle decimals) eliminates drift and ensures 100% financial accuracy.

---

## 🧠 Critical Technical Insights

### Multiplication vs. Addition Paradox
In the **Paillier** and **Exponential-ElGamal** systems, the math is counter-intuitive:
* To **ADD** two ciphertexts, the CPU performs **Modular Multiplication**.
* To **MULTIPLY** a ciphertext by a constant, the CPU performs **Modular Exponentiation**.
* **Result:** The IBM i Power CPU handles these operations with extremely low latency because they leverage optimized integer math.

### The "Cents" Rule for IBM i
Because PHE works primarily with integers, all financial calculations must be "scaled up" before encryption. 
> **Standard:** $1.25 \rightarrow 125$ (Scale 100).  
> **Process:** Encrypt $\rightarrow$ Math $\rightarrow$ Decrypt $\rightarrow$ Divide by 100.

---

## 🛠️ How to Run
1.  **Enter Python Virtual Environment:**
    ```bash
    python3 -m venv pyvenv3.9
    source pyvenv3.9/bin/activate
    ```
2.  **Install Dependencies:**
    ```bash
    pip install lightphe phe lightphe tabulate
    ```
3.  **Execute a Test:**
    ```bash
    python3 advanced_elgamal_math.py.py
    ```

---

## 🏁 POC Conclusion
The IBM i is highly capable of running Partially Homomorphic Encryption. For **Write-Heavy** applications (like real-time data ingestion), **Exponential-ElGamal** is recommended. For **Read-Heavy** applications (where fast decryption is required), **Paillier** is the superior choice. Always use **Integer Basis Points** to maintain financial precision.

---

### 🔐 Legal & Licensing
All scripts in this section are covered under the **MIT License**.
* **Copyright**: © 2026 Sameera Wijayasiri | theQSECOFR.com
* **Warranty**: Provided "AS IS"—Testing was performed on IBM i 7.5; results on older versions may vary due to OpenSSL version differences in PASE.

---