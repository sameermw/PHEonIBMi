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


import pickle
import time
import os
from lightphe import LightPHE

def run_storage_simulation():
    # --- PART 1: THE ENCRYPTION JOB (e.g., Run on Monday) ---
    print("\n[JOB A] Initializing Cryptosystem and Encrypting...")
    cs = LightPHE(algorithm_name="Exponential-ElGamal")
    
    payroll_total = 41750
    encrypted_obj = cs.encrypt(payroll_total)
    
    # Define IFS path
    ifs_path = "payroll_vault.dat"
    
    print(f"[JOB A] Saving encrypted object to IFS: {os.path.abspath(ifs_path)}")
    with open(ifs_path, "wb") as f:
        pickle.dump(encrypted_obj, f)
    print("[JOB A] Done. Data is now sitting as a binary blob on disk.")

    # --- PART 2: THE DECRYPTION JOB (e.g., Run on Friday) ---
    print("\n" + "-"*40)
    print("[JOB B] Starting Decryption Job...")
    
    if os.path.exists(ifs_path):
        print(f"[JOB B] Reading blob from IFS...")
        with open(ifs_path, "rb") as f:
            loaded_encrypted_obj = pickle.load(f)
        
        print("[JOB B] Decrypting reloaded object...")
        start_dec = time.time()
        decrypted_result = cs.decrypt(loaded_encrypted_obj)
        end_dec = time.time()
        
        print(f"[JOB B] Success! Decrypted Value: ${decrypted_result:,.2f}")
        print(f"[JOB B] Decryption Time: {end_dec - start_dec:.4f}s")
    else:
        print("[ERROR] File not found on IFS.")

if __name__ == "__main__":
    run_storage_simulation()
