# Lecture 2, algorithms: every program is built from a sequence, a decision and a repetition.
from so101.simple import home, move, read_angle, read_temperature

home()

# Sequence: the same steps in another order give another result.
move("elbow_flex", 30)
difference = 30 - read_angle("elbow_flex")     # read after the motion: close to 0
print("Read after the motion:", difference)

home()
before = read_angle("elbow_flex")              # read too early, before the motion
move("elbow_flex", 30)
print("Read before the motion:", 30 - before)

# Decision: one reading, two paths.
temperature = read_temperature("elbow_flex")
limit = 40
if temperature > limit:
    print(temperature, "°C: the arm rests")
else:
    print(temperature, "°C: the arm may work")

# Repetition: the same step again and again until the condition stops holding.
angle = 30
while angle > 0:
    angle = angle - 10
    move("elbow_flex", angle)
    print("Elbow lowered to", angle)

# Try it:
# 1. Draw the flowchart of the last loop before running it. How many times does it repeat?
# 2. Change the step from 10 to 15. Where does the elbow stop now?
# 3. Change the step to 0. What happens, and why? (Ctrl+C stops the program.)
