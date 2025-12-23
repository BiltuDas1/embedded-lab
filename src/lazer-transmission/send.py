from machine import Pin
import time

lazer = Pin(15, Pin.OUT)
MESSAGE = "THE QUICK BROWN FOX JUMPS OVER 13 LAZY DOGS! @2025"

# 40Hz Calculation: 1,000,000us / 40 bits = 25,000us per bit
BIT_TIME_40HZ = 25000 

def send_word_40hz(text):
    print(f"Sending message (Data bits at 40Hz): {text}")
    
    # 1. INITIAL ANCHOR (Using microseconds for high precision)
    anchor = time.ticks_us()

    # 2. PREAMBLE (2.0s ON)
    anchor = time.ticks_add(anchor, 2000000)
    lazer.on()
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    # 3. READY GAP (1.0s OFF)
    anchor = time.ticks_add(anchor, 1000000)
    lazer.off()
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    # 4. LOOP THROUGH EACH CHARACTER
    for char in text:
        # Convert character to 8 bits
        bits = [int(i) for i in "{:08b}".format(ord(char))]
        
        # --- Start Bit (0.1s ON = 100,000us) ---
        # Keeping this slow to prime the LDR
        anchor = time.ticks_add(anchor, 100000)
        lazer.on()
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
        
        # --- Data Bits (8 x 40Hz) ---
        # This is the part that is now 40Hz
        for b in bits:
            anchor = time.ticks_add(anchor, BIT_TIME_40HZ)
            lazer.value(b)
            while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
            
        # --- Character Gap (0.1s OFF) ---
        anchor = time.ticks_add(anchor, 100000)
        lazer.off()
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    print("Transmission Complete.")

# Run the function
try:
    send_word_40hz(MESSAGE)
except KeyboardInterrupt:
    lazer.off()