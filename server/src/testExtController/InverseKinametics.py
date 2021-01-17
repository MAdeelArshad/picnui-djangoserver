from ikpy import link
from ikpy import chain
import numpy as np

print(link)

# a = np.array([0.0, 0.61, 0.0])
# a.shape = (3,1)
# print(a)

# b = np.array([-0.577, -0.577, -0.577])
# b.shape = (3,1)
# print(b)

# t = [0 .61 0]
#
# r = [-0.577 -0.577 -0.577]
# 1.6563 rad





def getJointsPosition(r, waypoints):
    shoulderPanLink= ''
    shoulderLink= ''
    elbowLink= ''
    wrist1_Link= ''
    wrist2_Link= ''
    wrist3_Link = ''
    for item in r:
        # print(item['ORIGIN_XYZ'])
        # print(type(item['ORIGIN_XYZ']))
        # print(item)


        if(item['LINK'] == "base_link"):
            shoulderPanLink = link.URDFLink('shoulder_pan', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                            np.array(item['AXIS_XYZ']))
            print("TRUE1")

        elif(item['LINK'] == "shoulder_link"):
            shoulderLink = link.URDFLink('shoulder_lift', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                         np.array(item['AXIS_XYZ']))
            print("TRUE2")


        elif (item['LINK'] == "forearm_link"):
            elbowLink = link.URDFLink('elbow', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                      np.array(item['AXIS_XYZ']))
            print("TRUE3")


        elif (item['LINK'] == "wrist_1_link"):
            wrist1_Link = link.URDFLink('wrist1', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                        np.array(item['AXIS_XYZ']))
            print("TRUE4")


        elif (item['LINK'] == "wrist_2_link"):
            wrist2_Link = link.URDFLink('wrist2', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                        np.array(item['AXIS_XYZ']))
            print("TRUE5")


        elif (item['LINK'] == "wrist_3_link"):
            wrist3_Link = link.URDFLink('wrist3', np.array(item['ORIGIN_XYZ']), np.array(item['ORIGIN_RPY']),
                                        np.array(item['AXIS_XYZ']))
            print("TRUE6")



    LinksList = [shoulderPanLink, shoulderLink, elbowLink, wrist1_Link, wrist2_Link, wrist3_Link]
    LinkActiveMask = [True, True, True, True, True, True]

    print(didLinksInitialized(LinksList))
    if(didLinksInitialized(LinksList)):
        UR10_Chain = chain.Chain(LinksList, LinkActiveMask, 'UR10e Chain')
        res = [np.array([-0.65, -1.6, 0, -0.228571428571, 0, 0])] #go to reset pos first and then go to given points
        #
        for p in waypoints:
            res.append(UR10_Chain.inverse_kinematics(p, [-4.2146848e-08, 0, 0], "X"))
        return res






# print('Target Position of Joint Returned From Inverse Kinametics: ', getJointsPosition())


def didLinksInitialized(Links):
    check = 0
    for l in Links:
        if(l != ''):
            check += 1

    if check == 6:
        return True
    else:
        return False