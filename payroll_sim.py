# -----------------------------------------------------------------------------
# © 2026 Sameera Wijayasiri | theQSECOFR.com
#
# This script was developed as part of a Proof of Concept (POC) for 
# Implementing Homomorphic Encryption on IBM i Power Systems.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in the software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# -----------------------------------------------------------------------------


import time
from lightphe import LightPHE
from tabulate import tabulate

def run_payroll_simulation():
    # 1. SETUP: Initialize the champion additive algorithm from your benchmark
    print("\n[INIT] Initializing Exponential-ElGamal for Payroll...")
    cs = LightPHE(algorithm_name="Exponential-ElGamal")
    
    # 2. DATA: Mock salaries that would typically come from a Db2 table
    salaries = [5200, 4800, 6100, 3900, 5500, 7200, 4100, 4950]
    print(f"[DATA] Preparing to process {len(salaries)} salary records.")

    # 3. ENCRYPTION: Imagine this happens on a secure "On-Prem" IBM i partition
    print(f"[SECURE] Encrypting salaries...")
    start_enc = time.time()
    encrypted_salaries = [cs.encrypt(s) for s in salaries]
    end_enc = time.time()
    
    # 4. PROCESSING: This is the Homomorphic Sum (done on "Cloud" or "Untrusted" job)
    # In Exponential-ElGamal, the sum is initialized with an encryption of 0
    print("[PROCESS] Calculating total payroll homomorphically (Ciphertext Math)...")
    start_math = time.time()
    
    total_payroll_encrypted = cs.encrypt(0) # Start with encrypted zero
    for enc_salary in encrypted_salaries:
        total_payroll_encrypted = total_payroll_encrypted + enc_salary
    
    end_math = time.time()

    # 5. DECRYPTION: Only the final total is decrypted back on the secure partition
    print("[SECURE] Decrypting final payroll total...")
    start_dec = time.time()
    final_total = cs.decrypt(total_payroll_encrypted)
    end_dec = time.time()

    # --- REPORTING ---
    report = [
        ["Total Records", len(salaries)],
        ["Calculated Total", f"${final_total:,.2f}"],
        ["Actual Sum Check", f"${sum(salaries):,.2f}"],
        ["Encryption Time", f"{end_enc - start_enc:.4f}s"],
        ["Math Time (Sum)", f"{end_math - start_math:.4f}s"],
        ["Decryption Time", f"{end_dec - start_dec:.4f}s"]
    ]

    print("\n" + tabulate(report, tablefmt="fancy_grid", headers=["Metric", "Value"]))

if __name__ == "__main__":
    run_payroll_simulation()
