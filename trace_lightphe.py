import time
from lightphe import LightPHE

def trace_lightphe_execution():
    print("="*60)
    print("IBM i PASE: lightphe Multi-Algorithm Trace")
    print("="*60)

    # --- STEP 1: INITIALIZATION & KEY GEN ---
    # LightPHE wraps key generation into the class initialization.
    algorithm = "Paillier"
    print(f"\n[STEP 1] Initializing {algorithm} Cryptosystem...")
    print(f"Action: lightphe is setting up the {algorithm} mathematical group.")
    
    start = time.time()
    cs = LightPHE(algorithm_name=algorithm)
    end = time.time()
    
    print(f"Result: Cryptosystem ready. Public/Private keys stored in memory.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 2: ENCRYPTION ---
    val_1 = 50
    print(f"\n[STEP 2] Encrypting Value: {val_1}")
    print("Action: lightphe converts the integer into a 'Ciphertext' object.")
    
    start = time.time()
    c1 = cs.encrypt(plaintext=val_1)
    end = time.time()
    
    # lightphe ciphertexts are stored as lists or objects depending on the algorithm
    print(f"Result: Ciphertext object created.")
    print(f"Internal Data Type: {type(c1)}")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 3: HOMOMORPHIC ADDITION ---
    val_2 = 75
    c2 = cs.encrypt(plaintext=val_2)
    
    print(f"\n[STEP 3] Homomorphic Addition: [Encrypted {val_1}] + [Encrypted {val_2}]")
    print("Action: lightphe's operator overloading performs the modular multiplication.")
    
    start = time.time()
    c_sum = c1 + c2
    end = time.time()
    
    print(f"Result: Ciphertext sum created.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 4: HOMOMORPHIC SCALAR MULTIPLICATION ---
    multiplier = 4
    print(f"\n[STEP 4] Homomorphic Scalar Multiplication: [Encrypted Sum] * {multiplier}")
    print(f"Action: lightphe raises the sum's ciphertext to the power of {multiplier}.")
    
    start = time.time()
    c_final = c_sum * multiplier
    end = time.time()
    
    print(f"Result: Resulting ciphertext object ready.")
    print(f"Time Taken: {end - start:.4f} seconds.")

    # --- STEP 5: DECRYPTION & VERIFICATION ---
    print("\n[STEP 5] Decrypting Final Result...")
    print("Action: Applying the private key to the ciphertext.")
    
    start = time.time()
    decrypted_val = cs.decrypt(c_final)
    end = time.time()
    
    print(f"Final Decrypted Value: {decrypted_val}")
    print(f"Mathematical Verification: (50 + 75) * 4 = {decrypted_val}")
    print(f"Decryption Time: {end - start:.4f} seconds.")
    print("\n" + "="*60)

if __name__ == "__main__":
    trace_lightphe_execution()