from machine import Pin
import time

# --- TIMING CONFIGURATION (40Hz) ---
# 1 second / 40 bits = 0.025 seconds = 25,000 microseconds
BIT_TIME = 40000 

def send_bits(lazer: Pin, blocks: list):
    """
    Sends a list of 8-bit Hamming blocks via laser.
    Each block is preceded by a Start Bit (ON) and followed by a Gap (OFF).
    """
    # 1. INITIAL ANCHOR
    # We use a single anchor and increment it to prevent "Time Drift"
    anchor = time.ticks_us()

    # 2. PREAMBLE (1s ON) 
    # This wakes up the receiver and establishes the noise floor
    lazer.on()
    anchor = time.ticks_add(anchor, 1000000)
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
    
    # 3. READY GAP (0.5s OFF)
    # This tells the receiver: "Get ready, the real data starts now"
    lazer.off()
    anchor = time.ticks_add(anchor, 500000)
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    print(f"Blasting {len(blocks)} Hamming blocks...")

    # 4. DATA TRANSMISSION LOOP
    for block in blocks:
        # --- START BIT (Always ON) ---
        # The receiver triggers exactly when this bit hits
        lazer.on()
        anchor = time.ticks_add(anchor, BIT_TIME)
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
        
        # --- 8 DATA BITS (The Hamming Word) ---
        # We iterate through the bits provided by the Hamming encoder
        for bit in block:
            lazer.value(bit)
            anchor = time.ticks_add(anchor, BIT_TIME)
            while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
            
        # --- CHARACTER GAP (Always OFF) ---
        # We hold the laser OFF for BIT_TIME ms
        # This prevents the receiver from "missing the train" for the next byte
        lazer.off()
        anchor = time.ticks_add(anchor, BIT_TIME)
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    # 5. FINAL SHUTDOWN
    lazer.off()
    print("Transmission Complete.")