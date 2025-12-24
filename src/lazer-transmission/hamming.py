def is_even(bits, indices):
    return sum(bits[i] for i in indices) % 2 == 0

def hamming_7_4(nibble_bits):
    d1, d2, d3, d4 = nibble_bits
    
    # Calculate Parity bits so that the sum of the group is EVEN
    p1 = (d1 + d2 + d4) % 2
    p2 = (d1 + d3 + d4) % 2
    p3 = (d2 + d3 + d4) % 2
    
    # Assembly: [Global, P1, P2, D1, P4, D2, D3, D4]
    # Indices:    0      1   2   3   4   5   6   7
    block = [0, p1, p2, d1, p3, d2, d3, d4]
    
    # Global parity makes the sum of ALL 8 bits even
    block[0] = sum(block[1:]) % 2
    return block

def verify_hamming_7_4(bits):
    # Check syndromes - each parity bit covers itself + specific data bits
    s1 = 1 if not is_even(bits, [1, 3, 5, 7]) else 0
    s2 = 2 if not is_even(bits, [2, 3, 6, 7]) else 0
    s3 = 4 if not is_even(bits, [4, 5, 6, 7]) else 0
    
    syndrome = s1 + s2 + s3
    global_fault = sum(bits) % 2 != 0
    
    if syndrome == 0:
        if not global_fault: return None
        return 0 # Error in Global parity bit itself
    
    if global_fault:
        return syndrome
    
    return -1 

def decode_hamming_7_4(bits):
    # Extract data bits from indices 3, 5, 6, 7
    return (bits[3], bits[5], bits[6], bits[7])