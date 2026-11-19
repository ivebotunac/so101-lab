# The first motion: one joint, a small angle, slowly, and back.
from so101.simple import move, read_angle

start = read_angle("wrist_roll")
print("The wrist is at", start)

move("wrist_roll", start + 15, speed=20)
print("The wrist is at", read_angle("wrist_roll"))

move("wrist_roll", start, speed=20)
print("The wrist is back at", read_angle("wrist_roll"))
