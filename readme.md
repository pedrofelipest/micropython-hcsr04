hcsr04


Para receber o valor da distância em cm ou mm defina os pinos trigger e echo.
O valor retornado é do tipo float

```python
h = HCSR04(trigger_pin=16, echo_pin=0)u = HSCR04()

print(h.distance_mm())
print(h.distance_cm())
```
