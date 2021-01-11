from lxml import html, etree
from lxml.etree import tostring






# root = etree.Element("robot")
# print(root.tag)
# print(len(root))



# for child in root:
#     print(child.tag)
#     if (child.tag == 'link'):
#         links.append(child)
#     if(child.tag == 'joint'):
#         joints.append(child)
#     pass
#
#
# print("Links Array Length: " , len(links))
# print("Joints Array Length: " , len(joints))

# -------------------

# links = root.xpath("//robot[@name='UR10e']/link/@name")
# joints = root.xpath("//robot[@name='UR10e']/joint/@name")
# print(len(links))
# print(len(joints))

# o1 = root.xpath("//robot[@name='UR10e']/link[@name='base_link']/visual/origin/@xyz")
# origin_xyz1 = root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@xyz".format(links[0]))
# origin_rpy1 = root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@rpy".format(links[0]))
# axis_xyz1 = root.xpath("//robot[@name='UR10e']/joint[@name='{}']//axis/@xyz".format(joints[0]))
#
# print(links.index('upper_arm_link'))

# print(links)
# print(joints)
# print(origin_xyz1[0])
# print(origin_rpy1[0])
# print(axis_xyz1[0])


def lxml_to_stringArr(a):
    newlist = [str(s) for s in a]
    newStr = ""
    for i in newlist:
        newStr += i
    strArr = newStr.split(" ")
    for i in range(0, len(strArr)):
        strArr[i] = float(strArr[i])

    # print(strArr)
    return strArr

def InitializeLinks(xml):

    root = etree.fromstring(xml)
    etree.tostring(root)
    links = []
    joints = []
    links = root.xpath("//robot[@name='UR10e']/link/@name")
    joints = root.xpath("//robot[@name='UR10e']/joint/@name")
    result = []
    del (links[links.index('upper_arm_link')])
    for i in range(6):
        # print("--------------{}--------------".format(i))
        # print(root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@xyz".format(links[i]))[0])
        # print(root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@rpy".format(links[i]))[0])
        # print(root.xpath("//robot[@name='UR10e']/joint[@name='{}']//axis/@xyz".format(joints[i]))[0])
        # print(links[i])
        # print(joints[i])

        # a = root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@xyz".format(links[i]))[0]
        # print(a)
        # print(type(a))
        # print(lxml_to_stringArr(a))
        # print(type(lxml_to_stringArr(a)))


        # print("----------------------------")
        result.append({
            'LINK': links[i],
            'JOINT': joints[i],
            'ORIGIN_XYZ': lxml_to_stringArr(root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@xyz".format(links[i]))[0]),
            'ORIGIN_RPY': lxml_to_stringArr(root.xpath("//robot[@name='UR10e']/link[@name='{}']/visual/origin/@rpy".format(links[i]))[0]),
            'AXIS_XYZ': lxml_to_stringArr(root.xpath("//robot[@name='UR10e']/joint[@name='{}']//axis/@xyz".format(joints[i]))[0])
        })

    # for r in result:
    #     print(r)
    return result

f = open("New URDF.xml", "r")
tree = f.read()
# print(tree)
InitializeLinks(tree)