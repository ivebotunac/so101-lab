# The base turns to a secret angle. Guess it by looking at the arm.
import random

from gestures import celebrate, shake
from so101.simple import home, move

home()
secret = random.randint(-6, 6) * 10          # a multiple of 10 from -60 to 60
move("shoulder_pan", secret)
print("The base turned to an angle from -60° to 60°, a multiple of 10. Zero was straight ahead.")

tries = 0
while True:
    guess = int(input("Your guess: "))
    tries += 1
    if guess == secret:
        break

    shake(times=1)
    move("shoulder_pan", secret)
    difference = abs(guess - secret)
    if difference <= 10:
        print("Very close.")
    elif difference <= 30:
        print("Getting there.")
    else:
        print("Far off.")
    if guess < secret:
        print("Try a higher angle.")
    else:
        print("Try a lower angle.")

print(f"Correct, {secret}°, in {tries} tries.")
celebrate()
