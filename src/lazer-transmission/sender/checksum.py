def calculate_checksum(text):
    checksum = 0
    for char in text:
        checksum ^= ord(char)
    return checksum