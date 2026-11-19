# Loops: the same motion repeated, with while, for, range() and break.
from so101.simple import highest_angle, home, move, read_angle

home()

# while: the elbow rises by 15° until it reaches 45°.
angle = 0
while angle <= 45:
    move("elbow_flex", angle)
    print("Elbow at", read_angle("elbow_flex"))
    angle += 15

# for and range(): the base turns to five angles, from -40° to 40°.
for angle in range(-40, 41, 20):
    move("shoulder_pan", angle)

# for: the wrist rolls left and right three times.
for i in range(3):
    move("wrist_roll", 40, speed=90)
    move("wrist_roll", -40, speed=90)

# break: the wrist bends in steps of 30° and stops before the joint's limit.
limit = highest_angle("wrist_flex")
for angle in range(0, 181, 30):
    if angle > limit:
        print("Limit!")
        break
    move("wrist_flex", angle)

home()
