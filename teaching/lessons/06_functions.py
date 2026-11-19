# Lecture 6, functions: def, parameters, return, default arguments and local variables.
import random

from so101.simple import highest_angle, home, lowest_angle, move, read_angle


# A definition moves nothing; the body runs only when the function is called.
def wave(times=3, width=40):
    """Roll the wrist left and right."""
    for i in range(times):
        move("wrist_roll", width, speed=90)
        move("wrist_roll", -width, speed=90)
    move("wrist_roll", 0)


# A function that returns a value: the call becomes that value.
def clamp_angle(angle, lowest=-45, highest=45):
    """Return the angle, or the nearest limit when it is outside."""
    if angle < lowest:
        return lowest
    if angle > highest:
        return highest
    return angle


# A function that returns True or False stands where a condition is expected.
def is_within_limits(joint, angle):
    return lowest_angle(joint) <= angle <= highest_angle(joint)


# A function that calls other functions: the program is split into small parts.
def move_safely(joint, angle):
    """Move the joint if the angle is allowed, and report what happened."""
    if is_within_limits(joint, angle):
        move(joint, angle)
        return "moved"
    return "refused"


# return inside a loop ends the function at the first hit.
def first_angle_beyond(joint, step):
    for angle in range(0, 361, step):
        if not is_within_limits(joint, angle):
            return angle


home()

wave()                              # default arguments: 3 times, 40° wide
wave(times=2, width=20)             # the same function, a shy wave

print(clamp_angle(120), clamp_angle(-120), clamp_angle(120, highest=60))
move("elbow_flex", clamp_angle(120))

print("Elbow to 30°:", move_safely("elbow_flex", 30))
print("Elbow to 500°:", move_safely("elbow_flex", 500))
print("First angle the elbow refuses, in steps of 25°:", first_angle_beyond("elbow_flex", 25))

# A local variable lives only during the call.
def half_way(joint):
    middle = read_angle(joint) / 2
    return middle

move("elbow_flex", half_way("elbow_flex"))
# print(middle) here would raise NameError: the name exists only inside half_way().

# A function from a module: random.randint() picks where the base turns.
surprise = random.randint(-4, 4) * 10
print("The base turns to", surprise)
move("shoulder_pan", surprise)

home()

# Try it:
# 1. Write nod(times=2) that bends wrist_flex down and back, and call it twice.
# 2. wave() prints nothing and returns nothing. What does print(wave(times=1)) show?
# 3. Write a function that returns how many degrees a joint has left to its highest angle.
