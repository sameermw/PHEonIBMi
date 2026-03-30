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

def trace_ec_elgamal_execution():
    print("="*60)
    print("IBM i PASE: Elliptic Curve ElGamal (EC-ElGamal) Trace")
    print("="*60)

    # --- STEP 1: INITIALIZATION & CURVE GENERATION ---
    # EC-ElGamal uses a predefined curve (like NIST P-256)
    algorithm = "EllipticCurve-ElGamal"
    print(f"\n[STEP 1] Initializing {algorithm}...")
    print("Action: System is defining the Elliptic Curve and Base Point (G).")
    
    start = time.time()
    # Note: lightphe uses a default curve if not specified
    cs = LightPHE(algorithm_name=algorithm)
    end = time.time()
    
    print(f"Result: ECC Cryptosystem ready. Private key (scalar) and Public key (point) generated.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 2: ENCRYPTION (Point Mapping) ---
    val_1 = 25
    print(f"\n[STEP 2] Encrypting Value: {val_1}")
    print("Action: Mapping the integer to a point on the curve and blinding it.")
    
    start = time.time()
    c1 = cs.encrypt(plaintext=val_1)
    end = time.time()
    
    print(f"Result: Ciphertext created as a pair of curve points (C1, C2).")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 3: HOMOMORPHIC ADDITION ---
    val_2 = 15
    c2 = cs.encrypt(plaintext=val_2)
    
    print(f"\n[STEP 3] Homomorphic Addition: [Encrypted {val_1}] + [Encrypted {val_2}]")
    print("Action: Performing Elliptic Curve Point Addition on the ciphertexts.")
    print("Formula: (C1_a + C1_b, C2_a + C2_b)")
    
    start = time.time()
    c_sum = c1 + c2
    end = time.time()
    
    print(f"Result: New ciphertext point pair generated.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 4: HOMOMORPHIC SCALAR MULTIPLICATION ---
    multiplier = 2
    print(f"\n[STEP 4] Homomorphic Scalar Multiplication: [Encrypted Sum] * {multiplier}")
    print(f"Action: Performing Scalar Multiplication (repeated point addition).")
    
    start = time.time()
    c_final = c_sum * multiplier
    end = time.time()
    
    print(f"Result: Resulting ciphertext point ready.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 5: DECRYPTION (The Discrete Log Problem) ---
    print("\n[STEP 5] Decrypting Final Result...")
    print("Action: Solving the Elliptic Curve Discrete Logarithm Problem (ECDLP).")
    print("Warning: EC-ElGamal decryption is slow for very large results because it uses a lookup/search.")
    
    start = time.time()
    decrypted_val = cs.decrypt(c_final)
    end = time.time()
    
    print(f"Final Decrypted Value: {decrypted_val}")
    print(f"Mathematical Verification: (25 + 15) * 2 = {decrypted_val}")
    print(f"Decryption Time: {end - start:.4f} seconds.")
    print("\n" + "="*60)

if __name__ == "__main__":
    trace_ec_elgamal_execution()
