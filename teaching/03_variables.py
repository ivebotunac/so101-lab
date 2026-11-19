# Variables and types: a reading is stored, used in an expression and printed.
from so101.simple import home, move, read_angle, read_temperature

home()

target = 30                              # int, degrees
move("elbow_flex", target)

angle = read_angle("elbow_flex")         # float, what the motor reports
error = target - angle
temperature = read_temperature("elbow_flex")

print(f"Target: {target}°, reached: {angle}°, error: {error:.1f}°")
print(f"Motor temperature: {temperature} °C")
print("The target is an", type(target), "and the reading is a", type(angle))

home()
