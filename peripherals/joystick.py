from machine import Pin, ADC

joy_y = ADC(Pin(26))
joy_x = ADC(Pin(27))

adc_min = 1000
adc_max = 45535

def direction():
    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()

    if x_val > adc_max:
        return 'esq'
    elif x_val < adc_min:
        return 'dir'
    elif y_val > adc_max:
        return 'baixo'
    elif y_val < adc_min:
        return 'cima'
    else: 
        return 'none'
