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
from phe import paillier

def trace_execution():
    print("="*60)
    print("IBM i PASE: Homomorphic Encryption Trace (Paillier)")
    print("="*60)

    # --- STEP 1: KEY GENERATION ---
    print("\n[STEP 1] Generating Keypair...")
    print("Action: System is accessing /dev/urandom to find two large primes (p and q).")
    
    start = time.time()
    public_key, private_key = paillier.generate_paillier_keypair(n_length=1024) 
    end = time.time()
    
    print(f"Result: Public Key 'n' generated. Length: {len(str(public_key.n))} digits.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 2: ENCRYPTION ---
    val_a = 50
    print(f"\n[STEP 2] Encrypting Plaintext: {val_a}")
    print("Action: Computing c = (g^m * r^n) mod n^2.")
    
    start = time.time()
    enc_a = public_key.encrypt(val_a)
    end = time.time()
    
    # We truncate the ciphertext for display because it is massive
    ciphertext_str = str(enc_a.ciphertext())
    print(f"Result (Truncated): {ciphertext_str[:50]}...{ciphertext_str[-50:]}")
    print(f"Observation: The number '50' is now a {len(ciphertext_str)} character integer.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 3: HOMOMORPHIC ADDITION ---
    val_b = 75
    print(f"\n[STEP 3] Encrypting Plaintext: {val_b}")
    print("Action: Computing c = (g^m * r^n) mod n^2.")

    start = time.time()
    enc_b = public_key.encrypt(val_b)
    end = time.time()

     # We truncate the ciphertext for display because it is massive
    ciphertext_str = str(enc_b.ciphertext())
    print(f"Result (Truncated): {ciphertext_str[:75]}...{ciphertext_str[-75:]}")
    print(f"Observation: The number '75' is now a {len(ciphertext_str)} character integer.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    
    print(f"\n[STEP 4] Performing Homomorphic Addition: [Encrypted {val_a}] + [Encrypted {val_b}]")
    print("Action: Multiplying the two ciphertexts together modulo n^2.")
    print("--- WHY MULTIPLY? ---")
    print("In the Paillier cryptosystem, the product of two ciphertexts ")
    print("corresponds to the sum of their underlying plaintexts.")
    print("Mathematically: Decrypt(C1 * C2) = (M1 + M2).")
    print("----------------------")
    print("Note: The CPU never sees the values 50 or 75 during this step!")
    
    start = time.time()
    enc_sum = enc_a + enc_b
    end = time.time()
    ciphertext_str = str(enc_sum.ciphertext())

    print(f"Result: New ciphertext generated.")
    print(f"Result (Truncated): {ciphertext_str[:125]}...{ciphertext_str[-125:]}")
    print(f"Observation: The number '125' is now a {len(ciphertext_str)} character integer.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 4: HOMOMORPHIC SCALAR MULTIPLICATION ---
    multiplier = 4
    print(f"\n[STEP 5] Performing Scalar Multiplication: [Encrypted Sum] * {multiplier}")
    print(f"Action: Raising the ciphertext of the sum to the power of {multiplier}.")
    
    start = time.time()
    enc_final = enc_sum * multiplier
    end = time.time()
    
    print(f"Result: Final encrypted result ready for decryption.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 5: DECRYPTION ---
    print("\n[STEP 6] Decrypting Final Result...")
    print("Action: Using private key (factors p and q) to reverse the modular exponentiation.")
    
    start = time.time()
    decrypted_val = private_key.decrypt(enc_final)
    end = time.time()
    
    print(f"Final Decrypted Value: {decrypted_val}")
    print(f"Mathematical Verification: (50 + 75) * 4 = {decrypted_val}")
    print(f"Decryption Time: {end - start:.4f} seconds.")
    print("\n" + "="*60)

if __name__ == "__main__":
    trace_execution()
