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

def single_index(i, j):
    return LED_MATRIX_IDX[i][j]

def blink_single_index(i, interval=1, r=20, g=20, b=20):
    write_single_index(i, r, g, b)
    time.sleep(interval)
    write_single_index(i, 0, 0, 0)

def blink(i, j, interval=1, r=20, g=20, b=20):
    blink_single_index(single_index(i,j), interval, r,g,b)

def write_single_index(i, r=20, g=20, b=20):
    """
    Acende o LED na posição i,j da matriz de LEDs com a cor definida por r,g,b

    Parâmetros:
        i, j (int): Coordenadas entre 0 a 4. i indica a linha, j indica a colunna
        r, g, b (int): Índices RGB para as cores. Valores entre 0 e 255
    """
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

def write(i, j, r=20, g=20, b=20):
    """
    Acende o LED na posição i,j da matriz de LEDs com a cor definida por r,g,b

    Parâmetros:
        i, j (int): Coordenadas entre 0 a 4. i indica a linha, j indica a colunna
        r, g, b (int): Índices RGB para as cores. Valores entre 0 e 255
    """
    if i > 4:
        return f'Valor escolhido i={i} invalido, escolha um valor entre 0 e 4'
    elif j > 4:
        return f'Valor escolhido j={j} invalido, escolha um valor entre 0 e 4'
    elif r > 255 or g > 255 or b > 255:
        return f'Valor escolhido de cor ({r},{g},{b}) inválido, escolha um valor entre 0 e 255 para cada cor'
    else:
        write_single_index(single_index(i,j), r,g,b)
        return f'Posicao: i={i} e j={j} na cor: ({r},{g},{b})'


def clear():
    """
    Apaga todos os LEDs da Matriz de LEDs
    """
    led_matrix.fill((0,0,0))
    led_matrix.write()
