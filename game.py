from random import randint
import time

from machine import Pin, ADC
import peripherals.led_matrix as ledmat
import peripherals.oled as oled
import peripherals.joystick as joystick

button_white = Pin(5, Pin.IN, Pin.PULL_UP)
button_blue = Pin(6, Pin.IN, Pin.PULL_UP)

led_red = Pin(12, Pin.OUT) #vermelho
led_green = Pin(11, Pin.OUT) # verde
led_blue = Pin(13, Pin.OUT) # azul

def send_start_message():
    oled.display.fill(0)
    oled.display.text("Pressione ", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.text("qualquer botao", 0, 10) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.text("para iniciar", 0, 20) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.show()

def send_death_message():
    oled.display.fill(0)
    oled.display.text("Voce perdeu...", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.text("Pressione o", 0, 10) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.text("botao para jogar", 0, 20) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.text("novamente", 0, 30) # Segundo, escreve "Ola, Mundo!" no centro do display.
    oled.display.show()

class Game:
    def __init__(self, speed=1):
        self.level = 0
        self.speed = speed
        self.sequence = list()
        
        self.x_cursor = 2
        self.y_cursor = 2

        self.player_points = 0

        self.state = 'IDLE'

        self.increase_level()


    def run(self):
        send_start_message()

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

            self.state = 'PLAYER_MOVE'
            ledmat.write(self.y_cursor, self.x_cursor)

        elif self.state == 'PLAYER_MOVE':
            ledmat.write(self.y_cursor, self.x_cursor, 5, 5, 40)
            dir = joystick.direction()
            if dir != 'none':
                self.walk_cursor(dir)
                ledmat.clear()
                ledmat.write(self.y_cursor, self.x_cursor, 5, 5, 40)
                time.sleep(0.2)
            
            if button_blue.value() == 0:
                right_pos = self.sequence[self.player_points]
                if(ledmat.single_index(self.y_cursor, self.x_cursor) == right_pos):
                    if self.player_points == self.level - 1:
                        self.x_cursor = 2
                        self.y_cursor = 2
                        ledmat.clear()
                        led_green.value(1)
                        time.sleep(0.5)
                        led_green.value(0)
                        self.increase_level()
                        self.player_points = 0

                        self.state = 'SHOWING_SEQUENCE'
                    else:
                        ledmat.clear()
                        led_blue.value(1)
                        time.sleep(0.5)
                        led_blue.value(0)

                        self.player_points += 1
                else:
                    send_death_message()
                    led_red.value(1)
                    time.sleep(0.5)
                    led_red.value(0)
                    ledmat.clear()

                    self.level = 0
                    self.sequence = list()
                    
                    self.x_cursor = 2
                    self.y_cursor = 2

                    self.player_points = 0

                    self.state = 'IDLE'

                    self.increase_level()



    def walk_cursor(self, direction):
        if direction == 'right':
            if self.x_cursor < 4:
                self.x_cursor += 1

        elif direction == 'left':
            if self.x_cursor > 0:
                self.x_cursor -= 1

        elif direction == 'up':
            if self.y_cursor > 0:
                self.y_cursor -= 1

        elif direction == 'down':
            if self.y_cursor < 4:
                self.y_cursor += 1

