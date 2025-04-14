from random import randint
import time

from machine import Pin, ADC
import peripherals.led_matrix as ledmat
import peripherals.oled as oled
import peripherals.joystick as joystick
import peripherals.buzzer as buzzer

button_white = Pin(5, Pin.IN, Pin.PULL_UP)
button_blue = Pin(6, Pin.IN, Pin.PULL_UP)

led_red = Pin(12, Pin.OUT) #vermelho
led_green = Pin(11, Pin.OUT) # verde
led_blue = Pin(13, Pin.OUT) # azul




music = buzzer.Music()

class Game:
    def __init__(self, speed=1):
        self.max_level = 5
        self.level = 0
        self.speed = speed
        self.sequence = list()
        
        self.x_cursor = 2
        self.y_cursor = 2

        self.player_points = 0

        self.state = 'IDLE'

        self.increase_level()


    def restart(self):
        self.level = 0
        self.sequence = list()
        
        self.x_cursor = 2
        self.y_cursor = 2

        self.player_points = 0

        self.state = 'IDLE'

        self.increase_level()

    def run(self):
        print(f"Speed: {self.speed}, Level: {self.level}")
        print(f"Current Sequence: {self.sequence}")
        sequence_index = 0

        while True:
            self.get_user_input()

    def increase_level(self):
        if(self.level >= self.max_level):
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
            self.send_start_message()
            dir = joystick.direction()
            if button_blue.value() == 0:
                self.state = 'SHOWING_SEQUENCE'
                music.play_ini()

            if dir != 'none':
                if dir == 'up' and self.max_level < 25:
                    self.max_level += 1
                    self.send_start_message()
                    time.sleep(0.2)
                elif dir == 'down' and self.max_level > 1:
                    self.max_level -= 1
                    self.send_start_message()
                    time.sleep(0.2)

        elif self.state == 'SHOWING_SEQUENCE':
            for led_index in self.sequence:
                ledmat.blink_single_index(led_index)

            self.state = 'PLAYER_MOVE'
            ledmat.write(self.y_cursor, self.x_cursor)

        elif self.state == 'PLAYER_MOVE':
            ledmat.write(self.y_cursor, self.x_cursor, 5, 5, 40)
            self.show_current_status()
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
                        self.player_points = 0
                        if self.level < self.max_level:
                            ledmat.clear()
                            led_green.value(1)
                            music.play_super_yeah()
                            led_green.value(0)
                            self.increase_level()

                            self.state = 'SHOWING_SEQUENCE'
                        else:
                            self.send_victory_message()
                            ledmat.clear()
                            led_green.value(1)
                            music.play_victory()
                            led_green.value(0)

                            self.restart()
                    else:
                        ledmat.clear()
                        led_blue.value(1)
                        music.play_yeah()
                        time.sleep(0.5)
                        led_blue.value(0)

                        self.player_points += 1

                else:
                    self.send_death_message()
                    music.play_dumb()
                    led_red.value(1)
                    time.sleep(0.5)
                    led_red.value(0)
                    ledmat.clear()

                    self.restart()



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


    def send_start_message(self):
        oled.display.fill(0)
        oled.display.text("Pressione", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("qualquer botao", 0, 10) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("para iniciar.", 0, 20) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("Escolha o nivel", 0, 40) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text(f"maximo: {self.max_level}", 0, 50) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.show()


    def show_current_status(self):
        oled.display.fill(0)
        oled.display.text(f"Nivel maximo: {self.max_level}", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text(f"Nivel: {self.level}", 0, 10) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.show()


    def send_death_message(self):
        oled.display.fill(0)
        oled.display.text("Voce perdeu...", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("Pressione o", 0, 10) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("botao para jogar", 0, 20) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.text("novamente", 0, 30) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.show()

    def send_victory_message(self):
        oled.display.fill(0)
        oled.display.text("Voce ganhou!", 0, 0) # Segundo, escreve "Ola, Mundo!" no centro do display.
        oled.display.show()

