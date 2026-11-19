# Conditions: the program asks for an angle and decides whether the elbow may go there.
from so101.simple import highest_angle, home, lowest_angle, move, read_temperature

home()

lowest = lowest_angle("elbow_flex")
highest = highest_angle("elbow_flex")
angle = float(input(f"Elbow angle ({lowest} to {highest}): "))

temperature = read_temperature("elbow_flex")
if temperature > 55:
    print("The motor is hot, the arm stays where it is.")
elif angle < lowest:
    print("Too low, the elbow goes to its lowest angle.")
    move("elbow_flex", lowest)
elif angle > highest:
    print("Too high, the elbow goes to its highest angle.")
    move("elbow_flex", highest)
else:
    print("Within limits.")
    move("elbow_flex", angle)

# Two conditions joined with and: the gripper opens only for a raised elbow.
if angle > 0 and angle <= highest:
    print("The elbow is raised, the gripper opens.")
    move("gripper", 90)
else:
    print("The gripper stays closed.")
