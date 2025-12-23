from machine import Pin
import time
import send
import checksum

lazer = Pin(15, Pin.OUT)
MESSAGE = "THE QUICK BROWN FOX JUMPS OVER 13 LAZY DOGS! @2025"

try:
    BITS = list()
    for char in MESSAGE:
        BITS.append((int(i) for i in "{:08b}".format(ord(char))))
    BITS.append((int(i) for i in "{:08b}".format(checksum.calculate_checksum(MESSAGE))))
    send.send_bits(lazer, tuple(BITS))

except KeyboardInterrupt:
    lazer.off()