"""
This module implements GradCAM module for YOLOv5 in order to see where the model is attenting to.
"""

import argparse

import os
import sys
from pathlib import Path

from utils.general import print_args
from PIL import Image

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def run(
    weights=ROOT / 'yolov5s.pt',  # model path or triton URL
    source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
    data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
    imgsz=(640, 640),  # inference size (height, width)
    iou_thres=0.45,  # NMS IOU threshold
    device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    # model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)  # local model
    raw_image=Image.Image.resize(Image.open(source),(640,384))
    results = model([raw_image])
    # Results
    results.print()


def parseopt():
    parser=argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt

def main(opt):
    # we should check if `grad-cam` is installed
    run(**vars(opt))

if __name__ == '__main__':
    opt = parseopt()
    main(opt)