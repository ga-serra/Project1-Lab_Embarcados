from random import randint
import time

from machine import Pin, ADC, SoftI2C
import ssd1306
import peripherals.led_matrix as ledmat
import peripherals.joystick as joystick
import peripherals.buzzer as buzzer

button_white = Pin(5, Pin.IN, Pin.PULL_UP)
button_blue = Pin(6, Pin.IN, Pin.PULL_UP)

led_red = Pin(13, Pin.OUT) # azul
led_green = Pin(11, Pin.OUT) # verde
led_blue = Pin(12, Pin.OUT) #vermelho

music = buzzer.Music()

i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

class Game:
    # @brief Construtor do jogo
    #
    # @member max_level, level: int Nível máximo e atual. O jogador deve atingir o nível máximo para ganhar
    # @member led_time: int O tempo em segundos pelo qual cada LED ficará aceso
    # @member x_cursor, y_cursor: int
    # @member player_points: int O número de acêrtos do jogador na sequência atual
    # @member state: string O estado do jogo. Pode assumir os seguintes valores:
    #         -> 'IDLE': Quando o jogador ainda não iniciou o jogo, ou após perder
    #         -> 'SHOWING_SEQUENCE': Quando a sequência de LEDs está sendo mostrada
    #         -> 'PLAYER_MOVE': Quando é a vez do jogador
    def __init__(self, led_time=1):
        self.max_level = 5
        self.level = 0
        self.led_time = led_time
        self.sequence = list()
        
        self.x_cursor = 2
        self.y_cursor = 2

        self.player_points = 0

        self.state = 'IDLE'

        self.increase_level()


    # @brief Muda as variáveis para seus valores iniciais. O parâmetro `loss` pode ser usado
    # para indicar se o reinício está sendo feito após o jogador perder
    #
    # @param loss: bool Verdadeiro para fazer o estado do jogo mudar para 'LOSS'
    def restart(self, loss=False):
        self.level = 0
        self.sequence = list()
        
        self.x_cursor = 2
        self.y_cursor = 2

        self.player_points = 0

        if loss:
            self.state = 'LOSS'
        else:
            self.state = 'IDLE'

        self.increase_level()


    # @brief Roda o loop do jogo, lidando com o input do usuário e então atualizando
    # seu estado visual a cada ciclo
    def run(self):
        while True:
            self.handle_input()
            self.update()


    # @brief Atualiza a matriz de LEDs e o OLED de acordo com o estado do jogo,
    # dando feedback visual para o jogador
    def update(self):
        if self.state == 'IDLE':
            self.oled_send_start_message()

        elif self.state == 'PLAYER_MOVE':
            self.show_player_cursor()
            self.oled_show_current_status()

        elif self.state == 'LOSS':
            self.oled_send_loss_message()


    # @brief Recebe input do usuário e toma ação apropriada de acordo com o estado atual
    def handle_input(self):
        if self.state == 'IDLE' or self.state == 'LOSS':
            if button_blue.value() == 0:
                self.initialize_game_sequence()

            dir = joystick.direction()
            self.change_level_from_joystick(dir)

        elif self.state == 'SHOWING_SEQUENCE':
            self.play_led_sequence()

        elif self.state == 'PLAYER_MOVE':
            dir = joystick.direction()
            self.walk_cursor(dir)
            
            if button_blue.value() == 0:
                if(self.player_hit_correctly()):
                    # Os pontos do jogador aumentam até que ele chegue ao final
                    # da sequência, e então ele completa a fase.
                    if self.reached_end_of_sequence():
                        self.player_completes_level()
                    else:
                        self.player_increase_points()
                else:
                    self.player_loses() # O jogador perde se errar uma única vez


    # @brief Incrementa o nível do jogo, mas não permite que ultrapasse o nível 
    # máximo, e nem 25 (número máximo de LEDs na matriz)
    def increase_level(self):
        if(self.level >= self.max_level or self.level >= 25):
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


    def initialize_game_sequence(self):
        self.state = 'SHOWING_SEQUENCE'
        music.play_ini()


    # @brief Aumenta o nível máximo se o jogador mover o joystick para cima, e 
    # abaixa se ele o mover para baixo
    def change_level_from_joystick(self, dir):
        if dir != 'none':
            if dir == 'up' and self.max_level < 25:
                self.max_level += 1
                time.sleep(0.2)
            elif dir == 'down' and self.max_level > 1:
                self.max_level -= 1
                time.sleep(0.2)


    def play_led_sequence(self):
        for led_index in self.sequence:
            ledmat.blink_single_index(led_index, self.led_time)

        self.state = 'PLAYER_MOVE'


    def show_player_cursor(self):
        ledmat.write(self.y_cursor, self.x_cursor, 5, 5, 40)


    # @brief Move o cursor na direção do joystick e espera 0.2 segundos para evitar
    # dificuldade de controle do cursor
    def walk_cursor(self, direction):
        if direction == 'none':
            return

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

        ledmat.clear()
        time.sleep(0.2)


    # @brief O jogador acerta se a posição do cursor (com ínices x e y), ao ser
    # convertida para um único índice, corresponder ao valor da sequência
    def player_hit_correctly(self):
        right_pos = self.sequence[self.player_points]
        return ledmat.single_index(self.y_cursor, self.x_cursor) == right_pos


    def reached_end_of_sequence(self):
        return self.player_points == self.level - 1


    def center_cursor(self):
        self.x_cursor = 2
        self.y_cursor = 2


    # @brief Aumenta a pontuação do jogador, acendendo o LED azul e tocando uma
    # música
    def player_increase_points(self):
        ledmat.clear()
        led_blue.value(1)
        music.play_yeah()
        time.sleep(0.5)
        led_blue.value(0)

        self.player_points += 1


    # @brief Aumenta a nível caso o jogador não tenha atingido o último nível. 
    # Se o jogador atingiu o último nível, dá a vitória ao jogador
    def player_completes_level(self):
        self.center_cursor()
        self.player_points = 0
        if self.level < self.max_level:
            self.player_goes_to_next_level()
        else:
            self.player_victory()


    # @brief Aumenta o nível, acendendo o LED verde e tocando uma música
    def player_goes_to_next_level(self):
        ledmat.clear()
        led_green.value(1)
        music.play_super_yeah()
        led_green.value(0)
        self.increase_level()

        self.state = 'SHOWING_SEQUENCE'


    # @brief Reinicia o jogo trocando o estado para 'LOSS', ascendendo o LED
    # vermelho e tocando uma música
    def player_loses(self):
        self.oled_send_death_message()
        led_red.value(1)
        music.play_dumb()
        led_red.value(0)
        ledmat.clear()

        self.restart(loss=True)


    # @brief Dá a vitória ao jogador e reinicia o jogo, acendendo o LED verde e 
    # tocando uma música
    def player_victory(self):
        self.oled_send_victory_message()
        ledmat.clear()
        led_green.value(1)
        music.play_victory()
        led_green.value(0)

        self.restart()


    def oled_send_start_message(self):
        oled.fill(0)
        oled.text("Pressione", 0, 0)
        oled.text("qualquer botao", 0, 10)
        oled.text("para iniciar.", 0, 20)
        oled.text("Escolha o nivel", 0, 40)
        oled.text(f"maximo: {self.max_level}", 0, 50)
        oled.show()


    def oled_show_current_status(self):
        oled.fill(0)
        oled.text(f"Nivel maximo: {self.max_level}", 0, 0)
        oled.text(f"Nivel: {self.level}", 0, 10)
        oled.show()


    def oled_send_death_message(self):
        oled.fill(0)
        oled.text("Voce perdeu...", 0, 0)
        oled.show()


    def oled_send_loss_message(self):
        oled.fill(0)
        oled.text("Voce perdeu...", 0, 0)
        oled.text("Pressione o", 0, 10)
        oled.text("botao para jogar", 0, 20)
        oled.text("novamente", 0, 30)
        oled.text(f"Nivel maximo: {self.max_level}", 0, 50)
        oled.show()

    def oled_send_victory_message(self):
        oled.fill(0)
        oled.text("Voce ganhou!", 0, 0)
        oled.show()

