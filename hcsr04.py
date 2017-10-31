import machine, time
from machine import Pin

__version__ = '0.1.0'
__author__ = 'Pedro Felipe Teixeira'

class HCSR04:
    """
    Use o sensor ultra-sônico HC-SR04.
    O alcance do sensor está entre 2cm e 4m.
    Os tempos limite recebidos ouvindo o pino de eco são convertidos para OSError ('Fora do alcance')
    """
    # echo_timeout_us baseia-se no limite (400 cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: pino de saída para enviar pulsos
        echo_pin: pino para medir a distância. O pino deve ser protegido com resistência de 1k
        echo_timeout_us: Tempo limite em microssegundos para ouvir o pino de eco.
        Por padrão é baseado no limite limite do sensor (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # inicializa trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # inicializa echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Envie o pulso para disparar e ouvir no pino de eco.
        Usamos o método `machine.time_pulse_us ()` para obter os microssegundos até o eco ser recebido.
        """
        self.trigger.value(0) # estabiliza o sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # envia um pulso de10us.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # Para calcular a distância, obtemos o tempo de pulso e dividimos por 2
         # (o pulso anda a distância duas vezes) e por volta de 29,1
         # a velocidade do som no ar (343,2 m / s), que é equivalente a
         # 0.34320 mm / us que é 1mm cada 2.91us
         # Pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Obtenha a distância em centímetros com operações de ponto flutuante.
        Retorna um float
        """
        pulse_time = self._send_pulse_and_wait()

        # Para calcular a distância, obtemos o tempo de pulso e dividimos por 2
        # (o pulso anda a distância duas vezes) e por volta de 29,1
        # a velocidade do som no ar (343,2 m / s), que é equivalente a
        # 0.034320 cm / us que é 1cm cada 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms
