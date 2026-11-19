# The arm wakes up, greets by name and bows.
from gestures import bow, sleep, wake_up, wave

name = input("What is your name? ")

wake_up()
print(f"Hello, {name}!")

# One wave per letter of a short name, never more than five.
times = len(name)
if times > 5:
    times = 5
if times < 1:
    times = 1
wave(times=times)

print("Nice to meet you.")
bow()
sleep()
