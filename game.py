from random import randint
import time

from machine import Pin
import peripherals.led_matrix as ledmat
import peripherals.oled as oled

button_white = Pin(5, Pin.IN, Pin.PULL_UP)
button_blue = Pin(6, Pin.IN, Pin.PULL_UP)

class Game:
    def __init__(self, speed=1):
        self.level = 0
        self.speed = speed
        self.sequence = list()
        
        self.x_cursor = 0
        self.y_cursor = 0

        self.state = 'IDLE'

        self.increase_level()


    def run(self):
        # Comandos do display.
        oled.send_message_clear("Iniciar jogo?", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.

        for i in range(0, 4):
            self.increase_level()

        print(f"Speed: {self.speed}, Level: {self.level}")
        print(f"Current Sequence: {self.sequence}")
        sequence_index = 0

        while True:
            self.get_user_input()

    def increase_level(self):
        if(self.level >= 25):
            print("Maximum level reached.")
            return

        self.level += 1

        new_point = randint(0,24)
        first_new_point = new_point
        while new_point in self.sequence:
            new_point += 1
            if(new_point == first_new_point):
                print("Couldn't find new level. This line should have never executed.")
                return
            if(new_point >= 25):
                new_point = 0

        self.sequence.append(new_point)


    def get_user_input(self):
        if self.state == 'IDLE':
            if button_blue.value() == 0:
                self.state = 'SHOWING_SEQUENCE'

        elif self.state == 'SHOWING_SEQUENCE':
            for led_index in self.sequence:
                ledmat.blink_single_index(led_index)

            self.state = 'IDLE'

        elif self.state == 'PLAYER_MOVE':
            
