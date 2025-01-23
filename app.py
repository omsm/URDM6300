from machine import Pin
from urdm6300 import RDM6300
import utime as time

# Initialize the RDM6300 with TX (GPIO 8) and RX (GPIO 9) pins
rfid_reader = RDM6300(uart_id=1, tx_pin=8, rx_pin=9)

while True:
    card_id = rfid_reader.read()
    if card_id is not None:
        print(card_id)
    time.sleep(0.1)

