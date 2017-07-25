# requires RPi_I2C_driver.py
import RPi_I2C_driver


mylcd = RPi_I2C_driver.lcd()



def clear_all():
    mylcd.lcd_clear()
    
def lcd_clear_line(line):
    if((line == 3) or (line == 4)):
        mylcd.lcd_display_string_pos("                ",line, -4)
    else:
        mylcd.lcd_display_string_pos("                ",line, 0)
        

def lcd_display(msg, line, start):
    if((line == 3) or (line == 4)):
        start = start - 4
        
    mylcd.lcd_display_string_pos(str(msg),line,start)
