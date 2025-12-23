from machine import Pin
import time

ldr = Pin(0, Pin.IN)
def get_val(): return 0 if ldr.value() else 1

print("--- RECOVERY-AWARE ANALYZER ---")
print("Waiting for Preamble...")

# Initial Sync
while get_val() == 0: pass
while get_val() == 1: pass
print("Sync OK. Monitoring Sweep...")

while True:
    # --- STEP 1: WAIT FOR START BIT (Light ON) ---
    while get_val() == 0: 
        pass # Stays here during the 1s Recovery Gap
    
    t_start_bit = time.ticks_ms()
    
    # --- STEP 2: WAIT FOR START BIT TO END (Light OFF) ---
    while get_val() == 1: 
        pass # Stays here for the 100ms Start Bit duration
    
    start_bit_dur = time.ticks_diff(time.ticks_ms(), t_start_bit)
    
    # If the pulse was roughly 100ms, start the frequency test
    if 80 < start_bit_dur < 120:
        # --- STEP 3: MEASURE DATA BURST ---
        t1 = time.ticks_us()
        edges = 0
        last_state = 0 # It just turned OFF, so last state was 0
        
        # We look for 10 transitions
        while edges < 10:
            current = get_val()
            if current != last_state:
                edges += 1
                last_state = current
            
            # Safety timeout (If it takes longer than 1s, it failed)
            if time.ticks_diff(time.ticks_us(), t1) > 1000000:
                break
        
        t_end = time.ticks_us()
        total_burst_time = time.ticks_diff(t_end, t1)
        
        if edges == 10:
            actual_baud = 10 / (total_burst_time / 1000000)
            print(f"SUCCESS: {actual_baud:>4.1f} Baud")
            
            # --- STEP 4: CLEANUP ---
            # Wait for the laser to definitely be OFF before looping back
            # This prevents it from catching the same start bit twice
            time.sleep_ms(200) 
        else:
            print(f"FAILURE: Only saw {edges} edges. Bandwidth limit reached.")
            break