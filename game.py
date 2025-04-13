from random import randint
import time

import peripherals.led_matrix as ledmat
import peripherals.oled as oled


class Game:
    def __init__(self, speed=1):
        self.level = 0
        self.speed = speed
        self.sequence = list()
        
        self.x_cursor = 0
        self.y_cursor = 0

        self.increase_level()


    def run(self):
        # Comandos do display.
        oled.send_message_clear("Iniciar jogo?", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.

        for i in range(0, 28):
            self.increase_level()

        print(f"Speed: {self.speed}, Level: {self.level}")
        print(f"Current Sequence: {self.sequence}")
        sequence_index = 0

        while True:
            if(sequence_index >= len(self.sequence)):
                sequence_index = 0

            ledmat.blink_single_index(self.sequence[sequence_index])
            time.sleep(1)

            sequence_index += 1


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


    def get_user_input():
        ...


    def update():
        ...
