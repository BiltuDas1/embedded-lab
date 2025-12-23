from machine import Pin
import time

lazer = Pin(15, Pin.OUT)
MESSAGE = "THE QUICK BROWN FOX JUMPS OVER 13 LAZY DOGS! @2025"

# 40Hz timing: 25,000us per bit
BIT_TIME = 25000 

def send_word_fast(text):
    print(f"Sending message (Efficient 40Hz): {text}")
    
    # 1. PREAMBLE (Reduced to 1s for speed)
    lazer.on()
    time.sleep(1)
    lazer.off()
    time.sleep(0.5) # Ready Gap
    
    anchor = time.ticks_us()

    for char in text:
        bits = [int(i) for i in "{:08b}".format(ord(char))]
        
        # --- Start Bit (25ms) ---
        anchor = time.ticks_add(anchor, BIT_TIME)
        lazer.on()
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
        
        # --- Data Bits (8 x 25ms) ---
        for b in bits:
            anchor = time.ticks_add(anchor, BIT_TIME)
            lazer.value(b)
            while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
            
        # --- Character Gap (25ms) ---
        anchor = time.ticks_add(anchor, BIT_TIME)
        lazer.off()
        while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    print("Transmission Complete.")

try:
    send_word_fast(MESSAGE)
except KeyboardInterrupt:
    lazer.off()