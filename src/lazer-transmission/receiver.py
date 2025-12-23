from machine import Pin
import time

ldr_digital = Pin(0, Pin.IN)
def get_data(): return 0 if ldr_digital.value() else 1

# --- TIMING CONFIGURATION ---
BIT_TIME_US = 25000      
START_BIT_US = 100000    
SAMPLE_START_US = START_BIT_US + (BIT_TIME_US // 2)

print("--- 40Hz WORD MODE RECEIVER READY ---")

while True:
    # 1. WAIT FOR PREAMBLE
    while get_data() == 0: pass
    p_start = time.ticks_us()
    while get_data() == 1: pass
    if time.ticks_diff(time.ticks_us(), p_start) < 1500000: continue
        
    print("\nPreamble OK. Receiving: ", end="")
    
    # Using a list for efficiency
    message_list = []
    t_start_data = None # To track transmission time

    # 2. THE WORD LOOP
    while True:
        # Wait for Start Bit or Timeout (1 second)
        timeout_us = 1000000 
        wait_start = time.ticks_us()
        word_ended = False
        
        while get_data() == 0:
            if time.ticks_diff(time.ticks_us(), wait_start) > timeout_us:
                word_ended = True
                break
        
        if word_ended:
            break 

        # Record start time when the very first letter arrives
        if t_start_data is None:
            t_start_data = time.ticks_us()

        # 3. SYNC TO START BIT
        data_anchor = time.ticks_us()
        received_value = 0
        
        # 4. READ 8 BITS
        for i in range(8):
            deadline = time.ticks_add(data_anchor, SAMPLE_START_US + (i * BIT_TIME_US))
            while time.ticks_diff(deadline, time.ticks_us()) > 0: pass
            
            bit = get_data()
            received_value = (received_value << 1) | bit
        
        # 5. CONVERT AND APPEND
        try:
            char = chr(received_value)
            message_list.append(char)
            print(char, end="") 
        except:
            message_list.append("?")
            print("?", end="")

        # 6. CHARACTER COOLDOWN
        cooldown = time.ticks_add(time.ticks_us(), 110000)
        while time.ticks_diff(cooldown, time.ticks_us()) > 0: pass

    # 7. FINAL REPORT
    t_end_data = time.ticks_us()
    full_message = "".join(message_list) # JOINING THE LIST
    
    print(f"\n[Finished] Word: {full_message}")
    
    if t_start_data:
        # Calculate time: (End Time - Start Time - 1s Timeout)
        # Note: We subtract the 1s timeout because the code had to wait for it to realize the word ended
        total_time = (time.ticks_diff(t_end_data, t_start_data) - 1000000) / 1000000
        print(f"Total Transmission Time: {total_time:.2f} seconds")
        print(f"Characters per second: {len(message_list)/total_time:.2f}")
        
    print("-" * 30)