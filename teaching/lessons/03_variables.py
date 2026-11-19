# Lecture 3, variables, types, operators, input and output.
from so101.simple import home, move, read_angle

home()

# Assignment: the expression on the right is computed once, then the name gets the value.
target = 20                  # int
double = target * 2
target = 30                  # double stays 40, it was computed before this line
print(target, double)
move("elbow_flex", double)

# Types: what the program holds decides what it can do with it.
angle = read_angle("elbow_flex")       # float, the motor never lands exactly
reached = abs(double - angle) < 3      # bool
joint = "elbow_flex"                   # str
print(type(double), type(angle), type(reached), type(joint))
print(f"{joint}: target {double}°, reached {angle}°, close enough: {reached}")

# Swapping two values needs a helper variable.
left = -30
right = 30
helper = left
left = right
right = helper
move("shoulder_pan", left)             # goes to 30 first
move("shoulder_pan", right)
move("shoulder_pan", 0)

# input() always returns text; int() gives it a numeric meaning.
typed = input("Turn the wrist by how many degrees in total (for example 400)? ")
total = int(typed)
quarter_turns = total // 90            # integer division
rest = total % 90                      # remainder
print(f"{total}° is {quarter_turns} quarter turns and {rest}° more.")

# Whole quarter turns are skipped: the wrist only shows the remainder.
move("wrist_roll", rest)
move("wrist_roll", 0)

home()

# Try it:
# 1. What does print(typed * 2) show, and what print(total * 2)? Why?
# 2. Compute and print how many degrees are left until the next quarter turn.
# 3. Type 12.5 at the question. Read the error and fix the program with float().
