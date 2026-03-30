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


# test_phe.py
import time
from phe import paillier

print("--- Starting 'phe' (Paillier) POC ---")

# 1. Key Generation
print("Generating RSA keypair...")
start_time = time.time()
public_key, private_key = paillier.generate_paillier_keypair()
print(f"Key generation took {time.time() - start_time:.4f} seconds.\n")

# 2. Encrypting Data
num1 = 50
num2 = 75
scalar = 4

print(f"Encrypting data: num1={num1}, num2={num2}")
enc_num1 = public_key.encrypt(num1)
enc_num2 = public_key.encrypt(num2)

# 3. Homomorphic Operations (Done on ciphertext without decrypting!)
print(f"Performing homomorphic math...")
enc_addition = enc_num1 + enc_num2       # Encrypted + Encrypted
enc_scalar_mult = enc_num1 * scalar      # Encrypted * Plaintext

# 4. Decrypting Results
print("\nDecrypting results:")
dec_addition = private_key.decrypt(enc_addition)
dec_scalar_mult = private_key.decrypt(enc_scalar_mult)

print(f"Expected Addition (50 + 75) = 125 | Decrypted = {dec_addition}")
print(f"Expected Scalar Mult (50 * 4) = 200 | Decrypted = {dec_scalar_mult}")

if dec_addition == 125 and dec_scalar_mult == 200:
    print("SUCCESS: 'phe' operations verified.\n")
