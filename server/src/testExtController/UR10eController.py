"""UR10eController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
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
    print(joints_pos)
    print("------")

    c = 0

    while robot.step(timestep) != -1:
        break

    for pos in joints_pos:
        print("Inside For")
        print("Sensor Type: ", sholder_pan_motor_sensor.getType())
        print("Sensor Value: ", sholder_pan_motor_sensor.getValue())
        print("Motor Value: ", shoulder_pan_motor.getTargetPosition())

        start = time.time()



        while robot.step(timestep) != -1:

            try:
                if len(pos) == 6:
                    shoulder_pan_motor.setPosition(pos[0])
                    sholder_lift_motor.setPosition(pos[1])
                    elbow_lift_motor.setPosition(pos[2])

                    wrist1_motor.setPosition(pos[3]*10)
                    wrist2_motor.setPosition(pos[4])
                    wrist3_motor.setPosition(pos[5])
                    c = c + 1
                    # print(pos)
                    # time.sleep(.6)


            except Exception as ex:
                print(ex)
            finally:
                end = time.time()
                # print(end - start)
                if (end - start) > 8:
                    break



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



        print(data_arr)

        Deyploy_Waypoints(data_arr)




except Exception as e:
    print(str(e))
finally:
    # close the connection
    s.close()


# Deyploy_Waypoints([[-1,-1,-1],[-1,2,-2],[1,0,1]])