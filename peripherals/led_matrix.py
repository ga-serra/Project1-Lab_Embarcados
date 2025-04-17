import neopixel
import time
from machine import Pin

# ====================== Variáveis Globais =========================
NUM_LEDS = 25  # Número total de LEDs na matriz 5x5
PIN = 7  # Pino onde a matriz Neopixel está conectada
led_matrix = neopixel.NeoPixel(Pin(PIN), NUM_LEDS) # 

LED_MATRIX_IDX = [
    [24, 23, 22, 21, 20],    
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]


# @brief Toma dois índices inteiros i e j, e retorna o índice único associado ao
# LED correspondente na matriz de LEDs. i e j são dados na ordem padrão de matrizes,
# mas com indexação baseada em zero.
#
# Visualmente:
# (0, 0) (0,1)  ...
# (1, 0) (1, 1) ...
#    :     :
def single_index(i, j):
    return LED_MATRIX_IDX[i][j]


# @brief Toma um único índice. Pisca o LED correspondente da matriz de LEDs durante 
# o intervalo especificado, com a cor especificada. Piscará por um segundo e com cor
# branca se não forem especificados.
def blink_single_index(i, interval=1, r=20, g=20, b=20):
    write_single_index(i, r, g, b)
    time.sleep(interval)
    write_single_index(i, 0, 0, 0)


# @brief Toma um dois índices. Pisca o LED correspondente da matriz de LEDs durante 
# o intervalo especificado, com a cor especificada. Piscará por um segundo e com cor
# branca se não forem especificados.
def blink(i, j, interval=1, r=20, g=20, b=20):
    blink_single_index(single_index(i,j), interval, r,g,b)

# @brief Toma um único índice. Ascende o LED correspondente da matriz de LEDs com
# a cor especificada. Terá cor branca se não for especificada.
def write_single_index(i, r=20, g=20, b=20):
    if i <= 24 and r <= 255 and g <=255 and b <= 255:
        led_matrix[i] = (r, g, b)
        led_matrix.write()
        return f'Posicao: i={i} na cor: ({r},{g},{b})'
    elif i > 24:
        return f'Valor escolhido i={i} invalido, escolha um valor entre 0 e 24'
    elif r > 255 or g > 255 or b > 255:
        return f'Valor escolhido de cor ({r},{g},{b}) inválido, escolha um valor entre 0 e 255 para cada cor'
    else:
        return f'Coordenadas invalidas, escolha um valor i<=24 e valores para R G B <= 255.'


# @brief Toma dois índices. Ascende o LED correspondente da matriz de LEDs com
# a cor especificada. Terá cor branca se não for especificada.
def write(i, j, r=20, g=20, b=20):
    if i > 4:
        return f'Valor escolhido i={i} invalido, escolha um valor entre 0 e 4'
    elif j > 4:
        return f'Valor escolhido j={j} invalido, escolha um valor entre 0 e 4'
    elif r > 255 or g > 255 or b > 255:
        return f'Valor escolhido de cor ({r},{g},{b}) inválido, escolha um valor entre 0 e 255 para cada cor'
    else:
        write_single_index(single_index(i,j), r,g,b)
        return f'Posicao: i={i} e j={j} na cor: ({r},{g},{b})'


# @brief Apaga todos os LEDs da matriz de LEDs
def clear():
    """
    Apaga todos os LEDs da Matriz de LEDs
    """
    led_matrix.fill((0,0,0))
    led_matrix.write()
