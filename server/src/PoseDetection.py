import time

import cv2 as cv
import freenect
import numpy as np

import tf_pose.common as common
from numpy.distutils.fcompiler import str2bool
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from server.lifting.utils.prob_model import Prob3dPose


class PoseEstimation(object):

    def __init__(self, args, option=None, url=None):
        self.args = args
        self.option = option
        self.url = url
        self.w, self.h = model_wh(self.args.resize)
        if self.w > 0 and self.h > 0:
            self.e = TfPoseEstimator(get_graph_path(self.args.model), target_size=(self.w, self.h),
                                     trt_bool=str2bool(self.args.tensorrt))
        else:
            self.e = TfPoseEstimator(get_graph_path(self.args.model), target_size=(432, 368),
                                     trt_bool=str2bool(self.args.tensorrt))

        self.poseLifting = Prob3dPose('lifting/prob_model/prob_model_params.mat')

    def get_frame(self):
        image = None
        camera = 0
        # live stream ko abhi dekhna hai nechey
        if self.options == "kinect image":
            print("after waiting")
            time.sleep(5)
            print("before waiting")
            image, ret_val = freenect.sync_get_video()
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        elif self.options == "camera image":
            print("after waiting")
            time.sleep(5)
            print("before waiting")
            cam = cv.VideoCapture(camera)
            ret_val, image = cam.read()
        elif self.options == "static image":
            imagepath = "server/images" + self.options
            image = cv.imread(imagepath)
        return image

    def mesh(self, image):
        # image_h, image_w = image.shape[:2]
        width = 640
        height = 480
        pose_2d_mpiis = []
        visibilities = []

        humans = self.e.inference(image, resize_to_default=(self.w > 0 and self.h > 0),
                                  upsample_size=self.args.resize_out_ratio)

        for human in humans:
            pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
            pose_2d_mpiis.append(
                [(int(y * height + 0.5), int(x * width + 0.5)) for x, y in pose_2d_mpii]
            )
            visibilities.append(visibility)

        pose_2d_mpiis = np.array(pose_2d_mpiis)
        visibilities = np.array(visibilities)
        transformed_pose2d, weights = self.poseLifting.transform_joints(pose_2d_mpiis, visibilities)
        pose_3d = self.poseLifting.compute_3d(transformed_pose2d, weights)

        keypoints = pose_3d[0].transpose()
        keypoints = keypoints / 100
        print(" \n")

        print(keypoints)
        return keypoints[13]

    """
    return 3d keypoints
    
    """

    def getKeypoints(self):
        image = self.get_frame()
        try:
            keypoints = self.mesh(image)
        except AssertionError:
            print("body not in image")
            return Exception("body not in image")
        except Exception:
            print("General exception")
            return Exception("General exception")
        else:
            return keypoints
            pass
