from machine import Pin
import time

ldr_digital = Pin(0, Pin.IN)
# LDR Logic: 0 when light hits (usually), so we invert it for data
def get_data(): return 0 if ldr_digital.value() else 1

# --- TIMING CONFIGURATION ---
BIT_TIME_US = 25000      
START_BIT_US = 25000   
SAMPLE_START_US = START_BIT_US + (BIT_TIME_US // 2)

print("--- 40Hz HIGH-SPEED RECEIVER READY ---")

while True:
    # 1. WAIT FOR PREAMBLE
    while get_data() == 0: pass
    p_start = time.ticks_us()
    while get_data() == 1: pass
    
    # Validation: Preamble must be at least 0.5s
    if time.ticks_diff(time.ticks_us(), p_start) < 500000: continue
        
    print("\nReceiving: ", end="")
    message_list = []
    t_start_data = None 

    # 2. THE WORD LOOP
    while True:
        if t_start_data is None:
            # Sit and wait for the very first Start Bit
            while get_data() == 0: pass
            t_start_data = time.ticks_us() # The clock starts NOW
        else:
            # 1-second timeout to detect when the sender has stopped
            timeout_us = 1000000 
            wait_start = time.ticks_us()
            word_ended = False
            while get_data() == 0:
                if time.ticks_diff(time.ticks_us(), wait_start) > timeout_us:
                    word_ended = True
                    break
            if word_ended: break 

        # 3. SYNC TO START BIT
        data_anchor = time.ticks_us()
        received_value = 0
        
        # 4. READ 8 BITS
        for i in range(8):
            deadline = time.ticks_add(data_anchor, SAMPLE_START_US + (i * BIT_TIME_US))
            while time.ticks_diff(deadline, time.ticks_us()) > 0: pass
            
            bit = get_data()
            received_value = (received_value << 1) | bit
        
        # 5. PROCESS CHARACTER
        try:
            char = chr(received_value)
            message_list.append(char)
            print(char, end="") 
        except:
            message_list.append("?")
            print("?", end="")

        # 6. CHARACTER COOLDOWN (30ms)
        cooldown = time.ticks_add(time.ticks_us(), 30000)
        while time.ticks_diff(cooldown, time.ticks_us()) > 0: pass

    # 7. FINAL PERFORMANCE REPORT
    t_end_data = time.ticks_us()
    full_message = "".join(message_list)
    
    if t_start_data:
        # Duration = (End Time - Start Time - The 1s we spent waiting for timeout)
        total_time_us = time.ticks_diff(t_end_data, t_start_data) - 1000000
        total_seconds = total_time_us / 1000000
        
        print(f"\n\n--- TRANSMISSION REPORT ---")
        print(f"Total Message: {full_message}")
        print(f"Total Time:    {total_seconds:.2f} seconds")
        print(f"Speed:         {len(message_list)/total_seconds:.2f} chars/sec")
        print("-" * 30)