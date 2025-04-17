# ========================= Bibliotecas ============================
import peripherals.led_matrix as ledmat
from game import Game

from machine import Pin
from utime import sleep
from time import time
from random import randint

led_blue = Pin(12, Pin.OUT) #vermelho
led_green = Pin(11, Pin.OUT) # verde
led_red = Pin(13, Pin.OUT) # azul

# ========================= MAIN =============================
def main():
    setup()

    # led_red.value(1) #azul
    # led_blue.value(1) #vermelho
    # led_green.value(1)
    # ledmat.write(2,2)
    game = Game(2)
    game.run()


# ========================= Funções ==========================
def setup():
    """
    Realiza o setup inicial da placa. O setup consiste em:
        - Apagar o LED RGB
        - Apagar a Matriz de LEDs
    """
    led_red.value(0)
    led_green.value(0)
    led_blue.value(0)

    ledmat.clear()


if __name__ == '__main__':
    main()
