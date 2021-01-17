"""Maintainence controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
sholder_lift_motor = robot.getDevice("shoulder_lift_joint")
sholder_lift_motor.setVelocity(2.0)
elbow_lift_motor = robot.getDevice("elbow_joint")
elbow_lift_motor.setVelocity(2.0)
shoulder_pan_motor = robot.getDevice("shoulder_pan_joint")
shoulder_pan_motor.setVelocity(2.0)
wrist1_motor = robot.getDevice("wrist_1_joint")
wrist1_motor.setVelocity(2.0)
wrist2_motor = robot.getDevice("wrist_2_joint")
wrist2_motor.setVelocity(2.0)
wrist3_motor = robot.getDevice("wrist_3_joint")
wrist3_motor.setVelocity(2.0)

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    shoulder_pan_motor.setPosition(-0.57)
    sholder_lift_motor.setPosition(-1.6)
    elbow_lift_motor.setPosition(0)
    wrist1_motor.setPosition(-1.6)
    wrist2_motor.setPosition(0)
    wrist3_motor.setPosition(0)
    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
