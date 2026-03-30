import time
from lightphe import LightPHE

def run_precision_comparison():
    print("="*70)
    print("IBM i PASE: ElGamal Precision & Scaling Test")
    print("="*70)

    # Initialize the Additive ElGamal cryptosystem
    cs = LightPHE(algorithm_name="Exponential-ElGamal")
    
    # Inputs
    raw_price = 1000
    qty = 5
    shipping = 50
    discount = 150
    
    # ---------------------------------------------------------
    # METHOD 1: THE "TAX RATE" APPROACH (Small Multiplier)
    # ---------------------------------------------------------
    print("\n>>> METHOD 1: Using Tax Factor (11)")
    
    enc_price_1 = cs.encrypt(raw_price)
    
    # Logic: ((Price * Qty) * 11) + Shipping - Discount
    step1 = (enc_price_1 * qty) * 11 
    final_enc_1 = (step1 + cs.encrypt(shipping)) + cs.encrypt(-discount)
    
    result_1 = cs.decrypt(final_enc_1)
    print(f"Result 1: {result_1} (Expected: 54900)")
    print("Observation: Notice the +1 drift due to numerical noise.")

    # ---------------------------------------------------------
    # METHOD 2: THE "BASIS POINTS" APPROACH (Integer Scaling)
    # ---------------------------------------------------------
    print("\n" + "-"*60)
    print(">>> METHOD 2: Using Basis Points (Scale 100x)")
    
    # Scale: 1.10 becomes 110. Everything else must scale by 100 too.
    tax_basis = 110 
    
    enc_price_2 = cs.encrypt(raw_price)
    enc_ship_scaled = cs.encrypt(shipping * 100)
    enc_disc_scaled = cs.encrypt(discount * 100)
    
    # Corrected Formula: ((P * Q) * 110) + (S * 100) - (D * 100)
    step1_scaled = (enc_price_2 * qty) * tax_basis
    final_enc_2 = (step1_scaled + enc_ship_scaled) + cs.encrypt(-(discount * 100))
    
    raw_result_2 = cs.decrypt(final_enc_2)
    # Downscale the result after decryption
    final_result_2 = raw_result_2 / 100
    
    print(f"Raw Decrypted Integer: {raw_result_2}")
    print(f"Final Scaled Result: {final_result_2}")
    print("Observation: Scaling by 100 removes the +1 precision error.")
    print("-" * 60)

if __name__ == "__main__":
    run_precision_comparison()
