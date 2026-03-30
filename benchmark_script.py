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
import csv
from lightphe import LightPHE

# Check for tabulate, if not found, use a simple fallback formatter
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def run_benchmark():
    print("="*80)
    print("IBM i PASE: Homomorphic Encryption Algorithm Comparison")
    print("Environment: Python 3.9 on Power Systems")
    print("="*80)

    # All primary algorithms supported by LightPHE
    algorithms = [
        "RSA", 
        "ElGamal", 
        "Exponential-ElGamal", 
        "Paillier", 
        "Damgard-Jurik", 
        "Okamoto-Uchiyama", 
        "Benaloh", 
        "Naccache-Stern", 
        "Goldwasser-Micali", 
        "EllipticCurve-ElGamal"
    ]

    results = []

    for alg in algorithms:
        print(f"Testing {alg}...", end="\r")
        try:
            # --- STEP 1: KEY GENERATION ---
            start = time.time()
            cs = LightPHE(algorithm_name=alg)
            t_keygen = time.time() - start

            # --- STEP 2: ENCRYPTION ---
            m1, m2 = 10, 5
            start = time.time()
            c1 = cs.encrypt(m1)
            c2 = cs.encrypt(m2)
            t_encrypt = (time.time() - start) / 2  # Avg per op

            # --- STEP 3: HOMOMORPHIC MATH ---
            # Attempt Additive; if fail, use Multiplicative
            start = time.time()
            try:
                res_cipher = c1 + c2 
                op_type = "Add"
            except:
                res_cipher = c1 * c2
                op_type = "Mult"
            t_math = time.time() - start

            # --- STEP 4: DECRYPTION ---
            start = time.time()
            decrypted = cs.decrypt(res_cipher)
            t_decrypt = time.time() - start

            results.append({
                "Algorithm": alg,
                "Type": op_type,
                "KeyGen": round(t_keygen, 4),
                "Encrypt": round(t_encrypt, 4),
                "Math": round(t_math, 4),
                "Decrypt": round(t_decrypt, 4)
            })

        except Exception as e:
            # Catching algorithms that might require specific key sizes or 3rd party libs
            results.append({
                "Algorithm": alg,
                "Type": "N/A",
                "KeyGen": "Error",
                "Encrypt": "-",
                "Math": "-",
                "Decrypt": f"Check dependencies"
            })

    # --- OUTPUT SECTION ---
    headers = ["Algorithm", "Math Type", "KeyGen (s)", "Encrypt (s)", "Math (s)", "Decrypt (s)"]
    
    if HAS_TABULATE:
        # Format for terminal display
        table_data = [[r["Algorithm"], r["Type"], r["KeyGen"], r["Encrypt"], r["Math"], r["Decrypt"]] for r in results]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # Simple fallback if tabulate isn't installed
        print("\nAlgorithm | Type | KeyGen | Encrypt | Math | Decrypt")
        print("-" * 75)
        for r in results:
            print(f"{r['Algorithm']} | {r['Type']} | {r['KeyGen']} | {r['Encrypt']} | {r['Math']} | {r['Decrypt']}")

    # --- EXPORT TO CSV ---
    csv_file = "he_benchmark_results.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n[SUCCESS] Results exported to: {csv_file}")

if __name__ == "__main__":
    run_benchmark()