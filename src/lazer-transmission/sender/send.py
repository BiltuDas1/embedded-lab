from machine import Pin
import time


# 40Hz timing: 25,000us per bit
BIT_TIME = 25000

def send_bits(lazer: Pin, bits_stream: tuple[tuple[bytes]]):
    # 1. INITIAL ANCHOR
    anchor = time.ticks_us()

    # 2. PREAMBLE (1s ON) - Non-blocking high precision
    anchor = time.ticks_add(anchor, 1000000)
    lazer.on()
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass
    
    # 3. READY GAP (0.5s OFF)
    anchor = time.ticks_add(anchor, 500000)
    lazer.off()
    while time.ticks_diff(anchor, time.ticks_us()) > 0: pass

    # 4. DATA LOOP
    for bits in bits_stream:       
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

