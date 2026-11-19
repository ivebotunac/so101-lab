# Reads every joint and moves nothing: the first test after calibration.
from so101.simple import JOINTS, read_angle, read_temperature

for joint in JOINTS:
    print(f"{joint:14} {read_angle(joint):7.1f}   {read_temperature(joint)} °C")
