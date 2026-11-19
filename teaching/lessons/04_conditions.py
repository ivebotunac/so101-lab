# Lecture 4, conditions: if, elif, else, logical operators and nested conditions.
from so101.simple import highest_angle, home, lowest_angle, move, read_angle, read_temperature

home()

lowest = lowest_angle("shoulder_pan")
highest = highest_angle("shoulder_pan")
angle = float(input(f"Turn the base to which angle ({lowest} to {highest})? "))

# A chain of elif: exactly one branch runs, the first whose condition holds.
distance = abs(angle - read_angle("shoulder_pan"))
if distance < 20:
    speed = 20
elif distance < 50:
    speed = 45
else:
    speed = 90
print(f"The base travels {distance:.1f}°, so the speed is {speed}°/s.")

# A nested condition: first whether the motion is allowed at all, then where to.
temperature = read_temperature("shoulder_pan")
if temperature < 55:
    if lowest <= angle <= highest:
        move("shoulder_pan", angle, speed)
        print("Done.")
    elif angle < lowest:
        print("Too far to one side, the base stops at its limit.")
        move("shoulder_pan", lowest, speed)
    else:
        print("Too far to the other side, the base stops at its limit.")
        move("shoulder_pan", highest, speed)
else:
    print("The motor is hot, the base stays where it is.")

# and, or, not: several conditions in one.
position = read_angle("shoulder_pan")
turned = position < -10 or position > 10
if turned and not temperature > 40:
    print("The base is turned and the motor is cool: the gripper opens.")
    move("gripper", 90)
else:
    print("The gripper stays closed.")

home()

# Try it:
# 1. Which three angles test all three branches of the speed chain?
# 2. Put the condition distance < 50 first in the chain. Which branch can never run now?
# 3. Rewrite lowest <= angle <= highest with the operator and.
