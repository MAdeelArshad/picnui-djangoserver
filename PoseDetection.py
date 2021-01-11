import sys
import time

import cv2 as cv
import freenect
import numpy as np

import tf_pose.common as common


def get_camera_image():
    cam = cv.VideoCapture(0)
    ret_val, image = cam.read()
    return image


class PoseEstimation(object):

    def __init__(self, args):
        self.args = args

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

        humans = self.args["estimator"].inference(image, resize_to_default=(
                    self.args["width"] > 0 and self.args["height"] > 0),
                                                  upsample_size=float(4))

        for human in humans:
            pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
            pose_2d_mpiis.append(
                [(int(y * height + 0.5), int(x * width + 0.5)) for x, y in pose_2d_mpii]
            )
            visibilities.append(visibility)

        pose_2d_mpiis = np.array(pose_2d_mpiis)
        visibilities = np.array(visibilities)
        transformed_pose2d, weights = self.args["pose"].transform_joints(pose_2d_mpiis, visibilities)
        pose_3d = self.args["pose"].compute_3d(transformed_pose2d, weights)
        keypoints = pose_3d[0].transpose()
        keypoints = keypoints

        return keypoints[13]

    """
    return 3d keypoints

    """

    def getKeypoints(self, option=None, url=None):
        self.option = option
        self.url = url
        image = self.get_frame()
        try:
            keypoints = self.mesh(image)
        except AssertionError:
            print("body not in image")
            return Exception("body not in image")

        else:
            return keypoints
