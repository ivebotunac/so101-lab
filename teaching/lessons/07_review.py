# Lecture 7, review: one program with everything from lectures 1 to 6.
# The arm is driven from the keyboard: a command is typed, a function carries it out.
from so101.simple import highest_angle, home, lowest_angle, move, read_angle, read_temperature


def choose_speed(distance):
    """Short motions are slow, long ones fast."""
    if distance < 20:
        return 20
    elif distance < 50:
        return 45
    return 90


def move_checked(joint, angle):
    """Move the joint when the angle is allowed. Return True if it moved."""
    if not lowest_angle(joint) <= angle <= highest_angle(joint):
        print(f"{joint} goes from {lowest_angle(joint)}° to {highest_angle(joint)}°.")
        return False
    distance = abs(angle - read_angle(joint))
    move(joint, angle, choose_speed(distance))
    return True


def wave(times=3):
    for i in range(times):
        move("wrist_roll", 40, speed=90)
        move("wrist_roll", -40, speed=90)
    move("wrist_roll", 0)


def nod(times=1):
    for i in range(times):
        move("wrist_flex", 25, speed=90)
        move("wrist_flex", 0, speed=90)


def greatest_common_divisor(a, b):
    """Euclid's algorithm from lecture 2, written with a loop."""
    while b != 0:
        rest = a % b
        a = b
        b = rest
    return a


def sweep(joint, step):
    """Walk the joint through its range in steps. Return the number of stops."""
    stops = 0
    angle = int(lowest_angle(joint) / 2)
    while angle <= highest_angle(joint) / 2:
        move(joint, angle)
        stops += 1
        angle += step
    move(joint, 0)
    return stops


def print_joint(joint):
    print(f"{joint:14} {read_angle(joint):6.1f}°  {read_temperature(joint)} °C")


def print_status():
    print("Joint            Angle  Temperature")
    print_joint("shoulder_pan")
    print_joint("elbow_flex")
    print_joint("wrist_roll")


home()
commands = 0

while True:
    command = input("Command (wave, nod, turn, sweep, divisor, status, quit): ")

    if command == "quit":
        break
    if command == "":
        continue
    commands += 1

    if command == "wave":
        wave()
    elif command == "nod":
        nod(times=2)
    elif command == "turn":
        angle = float(input("Angle of the base: "))
        if move_checked("shoulder_pan", angle):
            print("The base is at", read_angle("shoulder_pan"))
    elif command == "sweep":
        step = int(input("Step in degrees (10 to 40): "))
        if step < 10 or step > 40:
            print("The step has to be from 10 to 40.")
        else:
            print("Stops:", sweep("shoulder_pan", step))
    elif command == "divisor":
        a = int(input("First number: "))
        b = int(input("Second number: "))
        divisor = greatest_common_divisor(a, b)
        print(f"The greatest common divisor of {a} and {b} is {divisor}.")
        # The arm nods the answer, but never more than six times.
        if divisor <= 6:
            nod(times=divisor)
    elif command == "status":
        print_status()
    else:
        print("Unknown command.")
        commands -= 1

print(f"{commands} commands carried out. The arm goes home.")
home()

# Try it:
# 1. Before running: how many stops does sweep("shoulder_pan", 20) make?
# 2. Add the command "shake" with its own function that turns the base left and right.
# 3. Count how many commands were unknown and print that number at the end.
# 4. An empty line is skipped with continue. What would break do there?
