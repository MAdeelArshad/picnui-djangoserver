import sys
import threading
import time
import _thread
import cv2 as cv
import freenect
import numpy as np
from PIL import Image,ImageShow

import tf_pose.common as common
from tf_pose.estimator import TfPoseEstimator


def get_camera_image():
    cam = cv.VideoCapture(0)
    ret_val, image = cam.read()
    return image


class PoseEstimation(object):

    def __init__(self, args):
        self.args = args
        self.window_counter = 0

    def get_frame(self):

        image = None
        if self.option == "kinect image":
            print("after waiting")
            time.sleep(5)
            print("before waiting")
            image, ret_val = freenect.sync_get_video()
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        elif self.option == "camera image":
            print("after waiting")
            time.sleep(5)
            print("before waiting")
            image = get_camera_image()
        elif self.option == "static image":
            imagepath = "server/images" + self.url
            image = cv.imread(imagepath)
        return image

    def mesh(self, image):
        width = 640
        height = 480
        pose_2d_mpiis = []
        visibilities = []

        # Re-samples the images and perform estimation
        humans = self.args["estimator"].inference(image, resize_to_default=(
                self.args["width"] > 0 and self.args["height"] > 0),
                                                  upsample_size=float(4))
        # creates the body structure containing body points
        structure = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        for human in humans:
            pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
            pose_2d_mpiis.append(
                [(int(y * height + 0.5), int(x * width + 0.5)) for x, y in pose_2d_mpii]
            )
            # Contains the body points. If empty then body not found error encounter
            visibilities.append(visibility)

        # Generate 2D points
        pose_2d_mpiis = np.array(pose_2d_mpiis)
        visibilities = np.array(visibilities)
        # Generate 3D points of 17 joints of body
        transformed_pose2d, weights = self.args["pose"].transform_joints(pose_2d_mpiis, visibilities)
        # pose_3d contains an matrix of size 17(body points)*3(x,y,z)
        pose_3d = self.args["pose"].compute_3d(transformed_pose2d, weights)
        # Take Transpose of the matrix and return a matrix of size 3*17
        keypoints = pose_3d[0].transpose()
        # chaning the color scheme of the image from RGB to BGR
        output=Image.fromarray(cv.cvtColor(structure, cv.COLOR_RGB2BGR))
        # Displaying Image on the frontend
        ImageShow.show(output,title=self.url)

        # window_name = "image " + str(self.window_counter)
        # structure=ResizeWithAspectRatio(image=structure,height=786)
        #
        # cv.imshow(window_name, structure)
        # cv.waitKey(10)
        # thread = myThread(self.window_counter, name=window_name)
        # thread.start()
        # _thread.start_new_thread(create_window(),window_name)

        # keypoints = keypoints

        """
        return 3d keypoints

        """

        return keypoints[13]


    def getKeypoints(self, option=None, url=None, ):
        self.option = option
        self.url = url
        image = self.get_frame()
        self.window_counter = self.window_counter+1
        print(self.window_counter)
        try:
            keypoints = self.mesh(image)
        except AssertionError:
            print("body not in image")
            return Exception("body not in image")

        else:
            return keypoints

# class myThread (threading.Thread):
#    def __init__(self, threadID, name):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#    def run(self):
#       print ("Starting " +str(self.threadID) )
#       create_window(window_name=self.name)
#       print ("Exiting " + self.window_name)

# def create_window(window_name):
#     print("inilize thread "+str(window_name)
#     while True:
#         if cv.waitKey(1) & 0xFF == 27:
#             cv.destroyAllWindows()
#             cv.waitKey(10)
#             break
#     pass
# def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
#     dim = None
#     (h, w) = image.shape[:2]
#
#     if width is None and height is None:
#         return image
#     if width is None:
#         r = height / float(h)
#         dim = (int(w * r), height)
#     else:
#         r = width / float(w)
#         dim = (width, int(h * r))
#
#     return cv.resize(image, dim, interpolation=inter)
