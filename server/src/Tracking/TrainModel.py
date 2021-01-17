from numpy.distutils.fcompiler import str2bool
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from lifting.utils.prob_model import Prob3dPose


def train_model():
    args = {}
    w, h = model_wh('0x0')
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h),
                            trt_bool=str2bool("False"))
    else:
        e = TfPoseEstimator(get_graph_path("cmu"), target_size=(432, 368),
                            trt_bool=str2bool("False"))
    poseLifting = Prob3dPose('lifting/prob_model/prob_model_params.mat')
    args = {
        "width": w,
        "height": h,
        "estimator": e,
        "pose": poseLifting
    }
    return args