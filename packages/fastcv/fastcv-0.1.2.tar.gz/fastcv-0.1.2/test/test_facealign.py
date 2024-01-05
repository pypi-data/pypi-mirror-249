
import random
import cv2
import numpy as np
from tqdm import tqdm
import fastcv
from fastcv import VideoLoader, VideoDumper, draw_text, resize, view, cast, info
from fastcv import face, timer
from fastcv import FFmpegVideoLoader, FFmpegVideoDumper

import PIL
from PIL import Image
from PIL import ImageDraw



def stable_videos():
    # loader = FFmpegVideoLoader("../../002_dataset/lip_jiaqi/11/train_source.mp4")
    loader = VideoLoader("../../002_dataset/lip_jiaqi/11/train_source.mp4")
    # bboxs [ (center_x, center_y, width, height) ]
    bboxs = []
    for idx, im in tqdm(enumerate(loader)):
        im_pil = cast(im, "pil")
        with timer():
            im_align, lm_align, transform_paras = face.detect_and_align(im, rotate=False)
            bboxs.append(transform_paras[0])
            # (x0, y0), _, (x1, y1), _ = transform_paras[0]
            # bboxs.append(((x0+x1)/2, (y0+y1)/2, x1-x0, y1-y0))
        if idx == 100000:
            break
    # smooth bboxs
    bboxs = face.smooth_bbox(bboxs, 13)
    loader = VideoLoader("../../002_dataset/lip_jiaqi/11/train_source.mp4")
    dumper = VideoDumper("../../002_dataset/lip_jiaqi/11/train_source_crop512.mp4", fps=25)
    for idx, im in tqdm(enumerate(loader)):
        # cromp image
        center_x, center_y, width, height = bboxs[idx]
        im = im[int(center_y-height/2):int(center_y+height/2), int(center_x-width/2):int(center_x+width/2)]
        im = resize(im, 512)
        dumper.write(im)
        if idx == 100000:
            break
    return

def test_videos():
    loader = fastcv.open("../../002_dataset/lip_jiaqi/6/train_source.mp4", "opencv")
    target_dir = "../../002_dataset/lip_jiaqi/raw_images/6/"
    buffer_imgs = []
    buffer_idxs = []

    def handel(imgs, names, prev_box=[]):
        def set_prev_box(transform_paras_src):
            transform_paras_src = np.array(transform_paras_src)
            x0 = np.min(transform_paras_src[:, 0], 0)
            y0 = np.min(transform_paras_src[:, 1], 0)
            x1 = np.max(transform_paras_src[:, 0], 0)
            y1 = np.max(transform_paras_src[:, 1], 0)
            w, h = x1 - x0, y1 - y0
            x0 = round(max(x0 - w, 0))
            y0 = round(max(y0 - h, 0))
            x1 = round(x1 + w)
            y1 = round(y1 + h)
            prev_box.clear()
            prev_box.extend([x0, y0, x1, y1])

        if not prev_box:
            print("Init prev_box")
            paras = face.detect_and_align(imgs[0], output_size=(512, 512))
            if paras is None:
                paras = face.detect_and_align(imgs[0], output_size=(512, 512), detector="sfd")
            set_prev_box(paras[2][0])

        paras = face.detect_and_align(imgs, output_size=(512, 512), rotate=True, prev_box=prev_box)
            
        for idx, (im_align, lm_align, transform_paras) in zip(names, paras):
            fastcv.save(im_align, f"./{target_dir}/{idx}.webp", quality=80)
            np.save(f"./{target_dir}/{idx}.npy", lm_align.round().astype(np.int16))
        else:
            print(im_align.shape)
            fastcv.view(im_align)
            set_prev_box(transform_paras[0])

        pass
    for idx, im in tqdm(enumerate(loader)):
        buffer_imgs.append(im)
        buffer_idxs.append(idx)
        if len(buffer_imgs) == 4:
            handel(buffer_imgs, buffer_idxs)
            buffer_imgs = []
            buffer_idxs = []
    else:
        handel(buffer_imgs, buffer_idxs)
        pass

        # continue
        
        # fastcv.save(im_align, f"./{target_dir}/{idx}.webp", quality=80)
        # np.save(f"./{target_dir}/{idx}.npy", lm_align.round().astype(np.int16))
        # continue
        # #  print(im_align)
        # view(im_align)
        # im_align_back, mask = face.align_back(im_align, im_pil.size, transform_paras)
        # im_pil.paste(cast(im_align_back, "pil"), cast(mask, "pil"))
        # view(mask)
        # view(im_align_back)
        # view(im_pil)
        # break
        # # print(quad)
        # # ImageDraw.Draw(im_pil).polygon(quad, outline=(255, 0, 0), width=20)
        # for i, p in enumerate(lm_align):
            # ImageDraw.Draw(im_align).arc((p[0]-5, p[1]-5, p[0]+5, p[1]+5), 0, 360, fill=(255, 0, 0))
            # ImageDraw.Draw(im_align).text((p[0], p[1]), str(i))

        # # draw landmarks on image with number
        # # for i, point in enumerate(preds[0]):
            # # ImageDraw.Draw(im_pil).text((point[0], point[1]), str(i))
            # # ImageDraw.Draw(im_pil).point((point[0], point[1]), fill=(255, 0, 0))
                

        # view(im_align)
        # # print(info(im_align), info(im_align_back), info(im_pil))
        # im_pil.paste(im_align_back, mask=Image.fromarray(mask))
        # view(im_align_back)
        # view(im_pil)
        # # break

def merge_face():
    f1 = random.choice(list(range(1100)))
    f2 = random.choice(list(range(1100)))
    d = "../../002_dataset/lip_jiaqi/raw_images/11"
    print(f1, f2)

    face0 = fastcv.open(f"./{d}/{f1}.webp")
    lm0 = np.load(f"./{d}/{f1}.npy")
    center_mouth_p = np.mean(lm0[48:68], 0)
    print(center_mouth_p)
    # fastcv.view(face0)
    #  lm0 = fastcv.face.detect(face0)
    mouth0 = face.get_mask_from_lm(lm0, region="mouth", size=(512, 512))
    # fastcv.view(fastcv.blend(face0, mouth0))

    face100 = fastcv.open(f"./{d}/{f2}.webp")
    lm100 = np.load(f"./{d}/{f2}.npy")
    center_mouth_p = np.mean(lm100[48:68], 0)
    print(center_mouth_p)
    mouth100 = face.get_mask_from_lm(lm100, region="mouth", size=(512, 512))
    # fastcv.view(face100)

    # fastcv.view(fastcv.blend(face100, mouth100))
    mask = np.max(np.array([mouth0, mouth100]), 0)
    # fastcv.view(fastcv.blend(face100, mask))
    

    # img = fastcv.draw.seamless_clone(face100, face0, mask)
    # fastcv.view(img)
    # img = fastcv.draw.seamless_clone(face0, face100, mask)
    # fastcv.view(img)
    #  erode_mask = cv2.erode(mask, np.ones((15, 15), dtype=np.uint8), iterations=1)
    mask = cv2.dilate(mask, np.ones((15, 15), dtype=np.uint8), iterations=1)
    mask = cv2.dilate(mask, np.ones((15, 15), dtype=np.uint8), iterations=1)
    # fastcv.view(fastcv.blend(face100, erode_mask))
    img0 = fastcv.draw.seamless_clone(face100, face0, mask)
    img1 = fastcv.draw.seamless_clone(face0, face100, mask)
    fastcv.view([face0, face100, img0, img1])
    return

    face1 = fastcv.open("./testfaces/12.jpg")
    lm1 = np.load("./testfaces/12.npy")
    fastcv.view(face1)

    face101 = fastcv.open("./testfaces/42.jpg")
    lm101 = np.load("./testfaces/42.npy")
    fastcv.view(face101)
    pass

if __name__=='__main__':
    test_videos()
    # merge_face()
