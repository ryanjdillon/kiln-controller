#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# GPIO to LCD mapping
LCD_RS = 22  # Pi pin 15
LCD_E = 27  # Pi pin 13
LCD_D4 = 10  # Pi pin 19
LCD_D5 = 9  # Pi pin 21
LCD_D6 = 11  # Pi pin 23
LCD_D7 = 17  # Pi pin 11

# Device constants
LCD_CHR = True  # Character mode
LCD_CMD = False  # Command mode
LCD_CHARS = 16  # Characters per line (16 max)

# LCD memory location for 1st line
LINES = {1: 0x80, 2: 0xC0}


class LCDWriter:
    """
    Parameters
    ----------
    E: int
    RS: int
    D4: int
    D5: int
    D6: int
    D7: int
    command: bool
    chars_per_line: int = 16
    char_mode: bool = True
    """

    def __init__(
        self,
        E: int,
        RS: int,
        D4: int,
        D5: int,
        D6: int,
        D7: int,
        command: bool,
        chars_per_line: int = 16,
        char_mode: bool = True,
    ):
        """
        Initialize and clear display
        """
        self.command = command
        self.E = E
        self.RS = RS
        self.D4 = D4
        self.D5 = D5
        self.D6 = D6
        self.D7 = D7
        self.hi_bits = {0x10: D4, 0x20: D5, 0x40: D6, 0x80: D7}
        self.lo_bits = {0x01: D4, 0x02: D5, 0x04: D6, 0x08: D7}
        self.chars_per_line = chars_per_line
        self.char_mode = char_mode

        GPIO.setwarnings(False)

        # Use BCM GPIO numbers
        GPIO.setmode(GPIO.BCM)

        # Set GPIO's to output mode
        for pin in [E, RS, D4, D5, D6, D7]:
            GPIO.setup(pin, GPIO.OUT)

        self.write(0x33, command)  # Initialize
        self.write(0x32, command)  # Set to 4-bit mode
        self.write(0x06, command)  # Cursor move direction
        self.write(0x0C, command)  # Turn cursor off
        self.write(0x28, command)  # 2 line display
        self.write(0x01, command)  # Clear display

        # Delay to allow commands to process
        time.sleep(0.0005)

    def __del__(self):
        GPIO.cleanup()

    def null_bits(self):
        for output in [self.D4, self.D5, self.D6, self.D7]:
            GPIO.output(output, False)

    def write(self, line_bits, command: bool):
        """
        Write bits to LCD module
        """
        GPIO.output(self.RS, command)
        for bit_map in [self.hi_bits, self.lo_bits]:
            self.null_bits()
            for bit in bit_map.keys():
                if line_bits & bit == bit:
                    GPIO.output(bit_map[bit], True)
            self.toggle_enable()

    def toggle_enable(self):
        """
        Toggle 'Enable' pin
        """
        time.sleep(0.0005)
        GPIO.output(self.E, True)
        time.sleep(0.0005)
        GPIO.output(self.E, False)
        time.sleep(0.0005)

    def text(self, message: str, line_number: int):
        """
        Send text to display
        """
        message = message.ljust(self.chars_per_line, " ")

        self.write(LINES[line_number], self.command)

        for i in range(self.chars_per_line):
            self.write(ord(message[i]), self.char_mode)


if __name__ == "__main__":
    writer = LCDWriter(
        LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_CMD, LCD_CHARS, LCD_CHR
    )

    writer.text("Hello World!", 1)
    writer.text("It works!", 2)

    time.sleep(5)

    writer.text("THE", 1)
    writer.text("END", 2)

    time.sleep(5)
