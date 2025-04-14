import time
from machine import Pin, PWM

class Music:
    def __init__(self, pin=21):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty_u16(0)
        self.REST = 0  # silêncio

    def _play(self, melody, durations):
        for note, duration in zip(melody, durations):
            if note != self.REST:
                self.buzzer.freq(note)
                self.buzzer.duty_u16(700)
            else:
                self.buzzer.duty_u16(0)
            time.sleep(duration / 1000)
            self.buzzer.duty_u16(0)
            time.sleep(0.05)

    def play_ini(self):
        # Notas necessárias
        E6  = 1319
        E7  = 2637
        C7  = 2093
        G6  = 1568
        G7  = 3136
        A6  = 1760
        B6  = 1976
        AS6 = 1865

        melody = [
            E7, E7, self.REST, E7,
            self.REST, C7, E7,
            G7, self.REST, G6,
            self.REST, C7, G6,
            self.REST, E6, self.REST, A6, B6,
            AS6, A6
        ]

        durations = [
            125, 125, 125, 125,
            125, 125, 125,
            125, 125, 125,
            125, 125, 125,
            125, 125, 125, 125, 125,
            125, 125
        ]

        self._play(melody, durations)

    def play_yeah(self):
            # Notas da melodia (em Hz)
        D5 = 587
        C5 = 523
        A4 = 440
        G4 = 392

        melody = [D5, C5, A4, G4]
        durations = [250, 250, 250, 250]  # Cada nota dura um quarto de segundo

        self._play(melody, durations)

    def play_victory(self):
        G  = 392
        A5 = 880
        E5 = 659
        C5 = 523
        B4 = 494
        F5 = 698

        melody = [
            A5, A5, A5,
            F5, C5, A5,
            F5, C5, A5,
            E5, E5, E5,
            F5, C5, G, B4,
            C5
        ]

        durations = [
            350, 350, 350,
            250, 1000, 350,
            250, 1000, 350,
            350, 350, 350,
            250, 1000, 250, 1000,
            1000
        ]

        self._play(melody, durations)

    def play_super_yeah(self):
        C5 = 523
        E5 = 659
        G5 = 784
        C6 = 1047

        melody = [
            C5, E5, G5, C6,
            self.REST, G5, C6
        ]
        durations = [
            200, 200, 200, 400,
            200, 200, 600
        ]

        self._play(melody, durations)
    
    def play_dumb(self):
    
        melody = [500, 1000, 1500, 2000]
    
        durations = [50, 50, 50, 50] 

        self._play(melody, durations)
