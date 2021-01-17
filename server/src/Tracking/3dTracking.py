import sys
import time
import argparse

import cv2 as cv
import freenect
import numpy as np
import tf_pose.common as common
from numpy.distutils.fcompiler import str2bool
from pyqtgraph import glColor
from pyqtgraph import QtGui, QtCore

from pyqtgraph.opengl import GLViewWidget, GLGridItem, GLScatterPlotItem, GLLinePlotItem
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from lifting.utils.prob_model import Prob3dPose


class PoseEstimation(object):
    @staticmethod
    def getframe(option):
        image = None
        ret_val = 0
        camera = 0
        if option == "camera":
            cam = cv.VideoCapture(camera)
            ret_val, image = cam.read()
        elif option == "kinect":
            image, ret_val = freenect.sync_get_video()
            image = cv.cvtColor(image,  cv.COLOR_RGB2BGR)
        elif option.__contains__("/"):
            image = cv.imread(option)
        elif option == "camera_image":
            print("after waiting")
            time.sleep(5)
            print("before waiting")
            cam = cv.VideoCapture(camera)
            ret_val, image = cam.read()
        return image, ret_val

    # creating window inilatizing graph objects
    def __init__(self, args, option='camera'):
        self.args = args
        self.fpsTime=0
        self.option = option
        self.app = QtGui.QApplication(sys.argv)
        self.window = GLViewWidget()
        self.window.setGeometry(0, 150, 1920, 1080)
        self.window.setCameraPosition(distance=50, elevation=8)
        self.window.setWindowTitle("3D Pose Estimation")
        self.window.show()
        gx = GLGridItem()
        gy = GLGridItem()
        gz = GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gy.rotate(90, 1, 0, 0)
        gx.translate(-10, 0, 0)
        gy.translate(0, -10, 0)
        gz.translate(0, 0, -10)
        self.window.addItem(gx)
        self.window.addItem(gy)
        self.window.addItem(gz)
        self.lines = {}
        keypoints = []
        self.connection = [
            [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6],
            [0, 7], [7, 8], [8, 9], [9, 10], [8, 11], [11, 12],
            [12, 13], [8, 14], [14, 15], [15, 16]
        ]
        self.w, self.h = model_wh(self.args.resize)

        if self.w > 0 and self.h > 0:
            self.e = TfPoseEstimator(get_graph_path(self.args.model), target_size=(self.w, self.h),
                                     trt_bool=str2bool(self.args.tensorrt))
        else:
            self.e = TfPoseEstimator(get_graph_path(self.args.model), target_size=(432, 368),
                                     trt_bool=str2bool(self.args.tensorrt))

        print(self.args.option)
        image, ret_val = PoseEstimation.getframe(self.args.option)

        self.poseLifting = Prob3dPose('lifting/prob_model/prob_model_params.mat')
        try:

            keypoints = self.mesh(image)
        except AssertionError:
            print("body not in image")
            keypoints = np.zeros((17, 3))
        except Exception:
            print("General exception")
            keypoints = np.zeros((17, 3))

        # self.lines = {}
        # self.connection = [
        #     [13, 16]
        # ]
        # p = []
        # p.append(keypoints[13])
        # p.append(keypoints[16])
        # p = np.array(p)
        finally:
            self.points = GLScatterPlotItem(
                pos=np.array(np.array(keypoints)),
                color=glColor((12, 255, 0)),
                size=15,
            )
            self.window.addItem(self.points)
            for n, pts in enumerate(self.connection):
                self.lines[n] = GLLinePlotItem(
                    pos=np.array([keypoints[p] for p in pts]),
                    color=glColor((0, 0, 255)),
                    width=3,
                    antialias=True
                )
                self.window.addItem(self.lines[n])

    def mesh(self, image):
        # image_h, image_w = image.shape[:2]

        width = 640
        height = 480
        pose_2d_mpiis = []
        visibilities = []

        humans = self.e.inference(image, resize_to_default=(self.w > 0 and self.h > 0),
                                  upsample_size=self.args.resize_out_ratio)
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - self.fpsTime)),
                    (10, 10), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv.imshow('tf-pose-estimation result', image)
        self.fpsTime= time.time()

        # image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        # cv2.putText(image,
        #             "FPS: %f" % (1.0 / (time.time() - terrain.fps_time)),
        #             (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #             (0, 255, 0), 2)
        # cv2.imshow('tf-pose-estimation result', image)
        # terrain.fps_time = time.time()
        # cv2.waitKey(1)

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
        return keypoints

    """
    return 3d keypoints

    """

    def update(self):
        """ tf.constant([123]) + tf.constant([321])
                update the mesh and shift the noise each time
                """
        # ret_val, image = terrain.get_video()
        # ret_val, image = self.cam.read()
        if cv.waitKey(1) & 0xFF == 27:
            cv.destroyAllWindows()
            sys.exit()

        keypoints = []
        image, ret_val = PoseEstimation.getframe(self.args.option)
        try:
            keypoints = self.mesh(image)
        except AssertionError:
            print("body not in image")
            keypoints = np.zeros((17, 3))
        except Exception:
            print("General exception")
            keypoints = np.zeros((17, 3))
        finally:
            self.points.setData(pos=np.array(keypoints))
            for n, pts in enumerate(self.connection):
                self.lines[n].setData(
                    pos=np.array([keypoints[p] for p in pts])
                )

    """
        update graph all graph objects
    """

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def animation(self, frametime=10):
        """u
        calls the update method to run in a loop
        """
        if not (self.option.__contains__("/") or self.option == "camera_image"):
            timer = QtCore.QTimer()
            timer.timeout.connect(self.update)
            timer.start(frametime)
        self.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='cmu',
                        help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--option', type=str, default="camera", help="Camera / Kinect / image_path / camera_image")
    parser.add_argument('--tensorrt', type=str, default="False",
                        help='for tensorrt process.')
    args = parser.parse_args()
    pose = PoseEstimation(args, option=args.option)
    pose.animation()
