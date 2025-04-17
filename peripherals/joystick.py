from machine import Pin, ADC

joy_y = ADC(Pin(26))
joy_x = ADC(Pin(27))

adc_min = 1000
adc_max = 45535

# @brief Retorna uma string indicando para que direção o usuário moveu o joystick
def direction():
    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()

    if x_val > adc_max:
        return 'right'
    elif x_val < adc_min:
        return 'left'
    elif y_val > adc_max:
        return 'up'
    elif y_val < adc_min:
        return 'down'
    else: 
        return 'none'
