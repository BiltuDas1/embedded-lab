from machine import Pin
import time

lazer = Pin(15, Pin.OUT)

def find_max_bandwidth():
    print("--- STARTING BANDWIDTH CHARACTERIZATION (PRIMED) ---")
    
    # 1. PREAMBLE (2s) & GAP (1s)
    lazer.on(); t=time.ticks_us()
    while time.ticks_diff(time.ticks_us(), t) < 2000000: pass
    lazer.off(); t=time.ticks_us()
    while time.ticks_diff(time.ticks_us(), t) < 1000000: pass

    # 2. SWEEP: 2 Baud to 100 Baud
    for baud in range(2, 101, 2):
        bit_dur = int(1000000 / baud)
        print(f"Testing {baud} Baud...")
        
        # --- THE WARM-UP (Start Bit) ---
        # 100ms ON to stabilize LDR chemistry
        lazer.on(); t=time.ticks_us()
        while time.ticks_diff(time.ticks_us(), t) < 100000: pass
        
        # --- THE DATA BURST (101010...) ---
        for _ in range(5):
            # Pulse ON
            lazer.on(); t=time.ticks_us()
            while time.ticks_diff(time.ticks_us(), t) < bit_dur: pass
            # Pulse OFF
            lazer.off(); t=time.ticks_us()
            while time.ticks_diff(time.ticks_us(), t) < bit_dur: pass
            
        # 3. RECOVERY GAP (1s)
        t=time.ticks_us()
        while time.ticks_diff(time.ticks_us(), t) < 1000000: pass

try:
    find_max_bandwidth()
except:
    lazer.off()