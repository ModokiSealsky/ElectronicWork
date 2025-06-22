from machine import PWM, Pin
from pico.StepMoter28BYJ48 import StepMoter28BYJ48
import utime

mt = StepMoter28BYJ48(10, 11, 12, 13)
print("正転")
mt.step(2000)
utime.sleep_ms(100)
print("逆転")
mt.step(-2000)
utime.sleep_ms(100)
print("終了")
