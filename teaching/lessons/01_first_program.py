# Lecture 1, the first program: statements run one after another, from the top down.
from so101.simple import home, move, read_temperature

print("The arm wakes up.")
home()

# Three statements, three motions, in the order they are written.
move("wrist_roll", 40)
move("wrist_roll", -40)
move("wrist_roll", 0)

# A reading from the motor is a value like any other.
temperature = read_temperature("wrist_roll")   # °C
limit = 65.0                                   # °C, the arm refuses to move above it

print("Motor temperature:", temperature, "°C")
print("The motor is below the limit:", temperature < limit)

# Try it:
# 1. Swap the first two move() lines. What changes in the motion?
# 2. Write "wrist_rol" instead of "wrist_roll" and read the error message.
# 3. Add a line that turns the base: move("shoulder_pan", 30).
