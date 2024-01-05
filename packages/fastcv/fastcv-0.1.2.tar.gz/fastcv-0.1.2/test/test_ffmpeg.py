#!/usr/bin/env python
# encoding: utf-8

import cv2

from tqdm import tqdm
from fastcv import VideoLoader, VideoDumper, draw_text, resize
from fastcv import FFmpegVideoLoader, FFmpegVideoDumper


def test_videos():
    loader = FFmpegVideoLoader("../../002_dataset/lip_jiaqi/test_reference/中文.avi")
    for i, im in enumerate(tqdm(loader)):
        print(i, im.shape, im.dtype)
        break

if __name__=='__main__':
    test_videos()
