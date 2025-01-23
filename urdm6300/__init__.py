from machine import UART, Pin
import time

class RDM6300:
    """
        Micro python Library for RDM6300 Module. This application will read serial data,
        Check the Start Byte, End Byte and checksum validation
        Return 
    """
    _RFID_STARTCODE = 0x02
    _RFID_ENDCODE = 0x03

    def __init__(self, uart_id=0, tx_pin=16, rx_pin=17, baudrate=9600, timeout=100):
        self.uart = UART(
            uart_id,
            baudrate=baudrate,
            tx=Pin(tx_pin),
            rx=Pin(rx_pin),
            timeout=timeout
        )
        self.current_fragment = []
        self.last_read_at = None
        self.card = None

    def read(self):
        """Reads data from the RFID reader."""
        while self.uart.any():
            received_byte = self.uart.read(1)
            if received_byte:
                byte = received_byte[0]
                if byte == self._RFID_STARTCODE:
                    self.current_fragment = []
                elif byte == self._RFID_ENDCODE:
                    return self._process_fragment(self.current_fragment)
                else:
                    try:
                        # Convert the byte to ASCII and interpret as hex
                        self.current_fragment.append(int(chr(byte), 16))
                    except ValueError:
                        # Invalid data, reset the fragment
                        self.current_fragment = []
        return None

    def _process_fragment(self, fragment):
        """Processes the received fragment and returns CardData."""
        if len(fragment) != 12:
            return None

        calculated_checksum = 0
        for i in range(0, 10, 2):
            byte = (fragment[i] << 4) | fragment[i + 1]
            calculated_checksum ^= byte

        received_checksum = (fragment[10] << 4) | fragment[11]
        card_value = 0
        for i in range(2, 10):
            card_value = (card_value << 4) | fragment[i]

        card_type = (fragment[0] << 4) | fragment[1]
        is_valid = received_checksum == calculated_checksum

        return is_valid, card_value, received_checksum, card_type
