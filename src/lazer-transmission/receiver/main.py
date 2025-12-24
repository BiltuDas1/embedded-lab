from machine import Pin
import time
import hamming

# --- HARDWARE SETUP ---
ldr = Pin(0, Pin.IN)

# --- TIMING CONFIGURATION (25Hz) ---
BIT_TIME = 40000  
SAMPLE_DELAY = BIT_TIME // 2 

def get_bit():
    return 0 if ldr.value() else 1

print("--- 25Hz HIGH-SPEED HAMMING RECEIVER READY ---")

while True:
    # 1. WAIT FOR PREAMBLE
    while get_bit() == 0: pass
    p_start = time.ticks_us()
    while get_bit() == 1: pass
    
    diff = time.ticks_diff(time.ticks_us(), p_start)
    if diff < 800000 or diff > 1200000:
        continue
        
    print("\n[Signal Detected] Receiving data...")
    data_list = []
    t_start_data = None

    # 2. DATA WORD LOOP
    first_block_message = True
    while True:
        t_sync = time.ticks_us()
        word_found = False
        
        # If 1.5 second no data is receiving then stop data processing
        while get_bit() == 0:
            if time.ticks_diff(time.ticks_us(), t_sync) > 1500000:
                break
        else:
            word_found = True
            if t_start_data is None:
                t_start_data = time.ticks_us()
        
        if not word_found:
            break

        anchor = time.ticks_us()
        received_byte = 0
        first_sample = time.ticks_add(anchor, int(BIT_TIME * 1.5))
        
        for i in range(8):
            target = time.ticks_add(first_sample, i * BIT_TIME)
            while time.ticks_diff(target, time.ticks_us()) > 0:
                pass
            received_byte = (received_byte << 1) | get_bit()
        
        if first_block_message:
            first_block_message = False
            if received_byte != 0:
                data_list.append(received_byte)
                print(f"\rCaptured: {len(data_list)} blocks", end="")
        else:
            data_list.append(received_byte)
            print(f"\rCaptured: {len(data_list)} blocks", end="")

        guard_time = time.ticks_add(anchor, BIT_TIME * 10) # Waiting for end bit
        while time.ticks_diff(guard_time, time.ticks_us()) > 0:
            pass

    t_end_data = time.ticks_us()

    # 4. POST-PROCESSING
    print("\n\n--- TRANSMISSION REPORT ---")
    print(f"Raw Data Captured: {data_list}") # CRITICAL DEBUG INFO
    
    collected_nibbles = []
    data_corrupted = False
    errors_corrected = 0
    
    for val in data_list:
        # Hamming uses 7 bits + 1 guard bit. Convert val to bits.
        bits = [(val >> i) & 1 for i in range(7, -1, -1)]
        
        error_pos = hamming.verify_hamming_7_4(tuple(bits))
        
        if error_pos == -1:
            data_corrupted = True
            print(f"BLOCK ERROR: Value {val} has multiple bit errors.")
            continue # Try to process other blocks anyway
        
        if error_pos is not None:
            bits[error_pos] ^= 1
            errors_corrected += 1
            
        nibble_bits = hamming.decode_hamming_7_4(tuple(bits))
        nibble_val = 0
        for b in nibble_bits:
            nibble_val = (nibble_val << 1) | b
        collected_nibbles.append(nibble_val)

    # 5. RECONSTRUCT MESSAGE
    if len(collected_nibbles) >= 2:
        message_chars = []
        for i in range(0, len(collected_nibbles) - 1, 2):
            char_code = (collected_nibbles[i] << 4) | collected_nibbles[i+1]
            if 32 <= char_code <= 126:
                message_chars.append(chr(char_code))
        
        full_message = "".join(message_chars)
        total_seconds = (time.ticks_diff(t_end_data, t_start_data) - 1500000) / 1000000

        print(f"Decoded Message: {full_message if full_message else '[Empty]'}")
        print(f"Status:          {'CORRUPTED' if data_corrupted else 'CLEAN/REPAIRED'}")
        print(f"Fixes:           {errors_corrected} bits")
        print(f"Time:            {total_seconds:.2f}s")
    else:
        print("RESULT: Insufficient data to form a character.")
    
    print("-" * 30)