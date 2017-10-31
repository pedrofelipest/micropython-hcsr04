#Micropython e sensor hcsr04

Com esta classe você poderá utilizar o sensor ultrassônico HCSR-04 nas seguintes funções:
* Receber a distância em cm
* Receber a distância em mm
* Alterar a distância máxima de leitura
* Controlar o erro por leituras fora das distâncias programadas

Para receber o valor da distância em cm ou mm defina os pinos trigger e echo.
O valor retornado é do tipo float

```python
h = HCSR04(trigger_pin=16, echo_pin=0)

print(h.distance_mm())
print(h.distance_cm())
```

O tempo limite padrão é baseado no limite do sensor (4m), mas também podemos definir um tempo limite diferente, passando o novo valor em microssegundos para o construtor.

```python
from hcsr04 import HCSR04
h = HCSR04(trigger_pin=16, echo_pin=0, echo_timeout_us=1000000)

print(h.distance_mm())
```

Quando o tempo limite é excedido enquanto recebe o pino de eco, o erro é convertido em OSError ('Fora do alcance')

```python
from hcsr04 import HCSR04

h = HCSR04(trigger_pin=16, echo_pin=0, echo_timeout_us=10000)

try:
    print('Distância: ', h.distance_cm, ' cm')
except OSError as ex:
    print('ERRO Fora do alcance:', ex)
```
