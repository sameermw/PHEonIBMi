# test_lightphe.py
import time
from lightphe import LightPHE

print("--- Starting 'lightphe' POC ---")

# 1. Initialize the Cryptosystem (Generates keys automatically)
print("Building LightPHE cryptosystem (Algorithm: Paillier)...")
start_time = time.time()
cs = LightPHE(algorithm_name="Paillier")
print(f"Initialization took {time.time() - start_time:.4f} seconds.\n")

# 2. Encrypting Data
val1 = 50
val2 = 75
scalar = 4

print(f"Encrypting data: val1={val1}, val2={val2}")
c1 = cs.encrypt(plaintext=val1)
c2 = cs.encrypt(plaintext=val2)

# 3. Homomorphic Operations
print(f"Performing homomorphic math...")
c_add = c1 + c2              # Homomorphic addition
c_scalar = c1 * scalar       # Homomorphic scalar multiplication

# 4. Decrypting Results
print("\nDecrypting results:")
dec_add = cs.decrypt(c_add)
dec_scalar = cs.decrypt(c_scalar)

print(f"Expected Addition (50 + 75) = 125 | Decrypted = {dec_add}")
print(f"Expected Scalar Mult (50 * 4) = 200 | Decrypted = {dec_scalar}")

if dec_add == 125 and dec_scalar == 200:
    print("SUCCESS: 'lightphe' operations verified.\n")