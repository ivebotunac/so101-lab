# Lecture 5, loops: while, for, range(), break, continue and nested loops.
from so101.simple import highest_angle, home, move, read_angle

home()

# while: the elbow rises by 15° for as long as the condition holds.
angle = 0
while angle <= 45:
    move("elbow_flex", angle)
    print("Elbow at", read_angle("elbow_flex"))
    angle += 15
print("After the loop the variable is", angle)

# for and range(start, stop, step): the stop value itself is never reached.
for angle in range(-40, 41, 20):
    move("shoulder_pan", angle)

# A negative step counts down.
for second in range(3, 0, -1):
    print(second)
    move("gripper", 60, speed=90)
    move("gripper", 10, speed=90)

# An accumulator: three readings, one average.
total = 0
for reading in range(3):
    total += read_angle("shoulder_pan")
print(f"Average angle of the base: {total / 3:.1f}°")

# continue skips one pass, break ends the whole loop.
limit = highest_angle("shoulder_pan")
for angle in range(0, 181, 30):
    if angle == 30:
        print("30° is skipped")
        continue
    if angle > limit:
        print(f"{angle}° is beyond the limit of {limit}°, the loop ends")
        break
    move("shoulder_pan", angle)
move("shoulder_pan", 0)

# Nested loops: at each of three base angles the wrist nods twice.
for base in range(-30, 31, 30):
    move("shoulder_pan", base)
    for nod in range(2):
        move("wrist_flex", 25, speed=90)
        move("wrist_flex", 0, speed=90)

home()

# Try it:
# 1. How many nods does the nested loop make in total? Count before you run it.
# 2. Change range(-40, 41, 20) to range(-40, 40, 20). Which angle is missing?
# 3. Rewrite the first while loop as a for loop with range().
