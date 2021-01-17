"""UR10eController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from hmac import new

from dask.array import round
from fire.decorators_test import double
from gevent.select import poll
from numpy import double
from sympy import floor

from controller import Robot
from xml_scrap import InitializeLinks
from InverseKinametics import getJointsPosition
import time
import socket, pickle

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 4096

# create the Robot instance.
robot = Robot()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
scale=1.5

# initializing motors
sholder_lift_motor = robot.getDevice("shoulder_lift_joint")
sholder_lift_motor.setVelocity(1.0)
elbow_lift_motor = robot.getDevice("elbow_joint")
elbow_lift_motor.setVelocity(1.0)
shoulder_pan_motor = robot.getDevice("shoulder_pan_joint")
shoulder_pan_motor.setVelocity(1.0)
wrist1_motor = robot.getDevice("wrist_1_joint")
wrist1_motor.setVelocity(1.0)
wrist2_motor = robot.getDevice("wrist_2_joint")
wrist2_motor.setVelocity(1.0)
wrist3_motor = robot.getDevice("wrist_3_joint")
wrist3_motor.setVelocity(1.0)

# initializing motors Sensors
sholder_pan_motor_sensor = robot.getDevice("shoulder_pan_joint_sensor")
sholder_pan_motor_sensor.enable(timestep)
sholder_lift_motor_sensor = robot.getDevice("shoulder_lift_joint_sensor")
sholder_lift_motor_sensor.enable(timestep)
elbow_lift_motor_sensor = robot.getDevice("elbow_joint_sensor")
elbow_lift_motor_sensor.enable(timestep)
wrist1_motor_sensor = robot.getDevice("wrist_1_joint_sensor")
wrist1_motor_sensor.enable(timestep)
wrist2_motor_sensor = robot.getDevice("wrist_2_joint_sensor")
wrist2_motor_sensor.enable(timestep)
wrist3_motor_sensor = robot.getDevice("wrist_3_joint_sensor")
wrist3_motor_sensor.enable(timestep)

def Deyploy_Waypoints(waypoints):
    # get Urdf data
    Urdf_data = robot.getUrdf()
    get_robot_state = InitializeLinks(Urdf_data)
    print(get_robot_state)
    joints_pos = getJointsPosition(get_robot_state, waypoints)
    print("------")
    print("Joint Motor Positions: " ,joints_pos)
    print("------")

    c = 0
    pan = 0.0; shoulder = 0.0; elbow = 0.0; wrist1 = 0.0; wrist2 = 0.0; wrist3 = 0.0;

    while robot.step(timestep) != -1:
        # sholder_lift_motor.setPosition(-1.6)
        # elbow_lift_motor.setPosition(0.0)
        break

    # time.sleep(.10)
    previous_pan = 0
    previous_shoulder = 0
    previous_elbow = 0
    previous_wrist3 = 0
    previous_wrist2 = 0
    previous_wrist1 = 0

    for pos in joints_pos:
        print("Inside For")

        if len(pos) == 6:
            shoulder_pan_motor.setPosition(pos[0])
            sholder_lift_motor.setPosition(pos[1])
            elbow_lift_motor.setPosition(pos[2])
            wrist1_motor.setPosition(pos[3])
            wrist2_motor.setPosition(pos[4])
            wrist3_motor.setPosition(pos[5])

        # print("Sensor Type: ", sholder_lift_motor_sensor.getType())
        # print("Sensor Value: ", sholder_lift_motor_sensor.getValue())
        # print("Motor Value: ", sholder_lift_motor.getTargetPosition())
        # print(round(sholder_lift_motor_sensor.getValue(), 3))
        # print(round(pos[1], 3))
        # print("Target Position: ", pos[1])

        # print("Diff: ", sholder_lift_motor.getTargetPosition() + (pos[1]))

        # start = time.time()


        new_pan = sholder_pan_motor_sensor.getValue()
        new_shoulder = sholder_lift_motor_sensor.getValue()
        new_elbow = elbow_lift_motor_sensor.getValue()
        new_wrist1 = wrist1_motor_sensor.getValue()
        new_wrist2 = wrist2_motor_sensor.getValue()
        new_wrist3 = wrist3_motor_sensor.getValue()

        while robot.step(timestep) != -1:
            print("=======================")
            # print("Motor Sensor Value: ", sholder_pan_motor_sensor.getValue())
            # print("Target Position: ", pos[0])
            # print("Motor Sensor Value: ", sholder_lift_motor_sensor.getValue())
            # print("Target Position: ", pos[1])
            # print("Motor Sensor Value: ", elbow_lift_motor_sensor.getValue())
            # print("Target Position: ", pos[2])
            # print("Motor Sensor Value: ", wrist1_motor_sensor.getValue())
            # print("Target Position: ", pos[3])
            # print("Motor Sensor Value: ", wrist2_motor_sensor.getValue())
            # print("Target Position: ", pos[4])
            # print("Motor Sensor Value: ", wrist3_motor_sensor.getValue())
            # print("Target Position: ", pos[5])
            # print(type(wrist3_motor_sensor.getValue()))
            # print(type(float(pos[5])))
            # print(type(pos[5]))
            print("=======================")
            if new_pan==previous_pan and new_shoulder == previous_shoulder and new_elbow == previous_elbow and new_wrist1==previous_wrist1 and new_wrist2==previous_wrist2 and new_wrist3==previous_wrist3:
                print ("in stopping infinte loop")
                time.sleep(1)
                break
            else :
                previous_pan = new_pan
                previous_shoulder = new_shoulder
                previous_elbow = new_elbow
                previous_wrist3 = new_wrist3
                previous_wrist2 = new_wrist2
                previous_wrist1 = new_wrist1

                new_pan = sholder_pan_motor_sensor.getValue()
                new_shoulder = sholder_lift_motor_sensor.getValue()
                new_elbow = elbow_lift_motor_sensor.getValue()
                new_wrist1 = wrist1_motor_sensor.getValue()
                new_wrist2 = wrist2_motor_sensor.getValue()
                new_wrist3 = wrist3_motor_sensor.getValue()
                time.sleep(1/1000)



# Enter here exit cleanup code.




        # shoulder_pan_motor.setPosition(1.65630989e-03)
        # sholder_lift_motor.setPosition(4.72708062e-02)
        # elbow_lift_motor.setPosition(-1.61715921e+00)
        #
        # wrist1_motor.setPosition(-1.57082494e+00)
        # wrist2_motor.setPosition(1.08601505e-05)
        # wrist3_motor.setPosition(0.00000000e+00)




try:

    s.bind(('', port))
    print("socket binded to %s" % (port))

    port = 4096
    s.listen(5)

    while True:

        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)


        res = c.recv(4096)
        data_arr = pickle.loads(res)



        print("Points received from frontend: " , data_arr)

        Deyploy_Waypoints(data_arr)




except Exception as e:
    print(str(e))
finally:
    # close the connection
    s.close()


# Deyploy_Waypoints([[-1,-1,-1],[-1,2,-2],[1,0,1]])