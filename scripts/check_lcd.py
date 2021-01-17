#!/usr/bin/python

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
