import cv2
import os
import time
import numpy as np
from PIL import Image


def corp_margin(img):
    img2 = img.sum(axis=2)
    (row, col) = img2.shape
    row_top = 0
    row_down = 0
    col_top = 0
    col_down = 0
    for r in range(1, row, 10):
        if img2.sum(axis=1)[r] < 765*col:
            row_top = r
            break
    for r in range(row-1, 0, -10):
        if img2.sum(axis=1)[r] < 765*col:
            row_down = r
            break
    for c in range(0, col, 10):
        if img2.sum(axis=0)[c] < 765*row:
            col_top = c
            break
    for c in range(col-1, 0, -10):
        if img2.sum(axis=0)[c] < 765*row:
            col_down = c
            break
    new_img = img[row_top:row_down+1, col_top:col_down+1, 0:3]
    return new_img


# def no_white_bg(img):
#     threshold = 100
#     dist = 5
#     img = Image.fromarray(cv2.cvtColor(
#         img, cv2.COLOR_BGR2RGB)).convert('RGBA')  # 增加Alpha通道
#     arr = np.array(np.asarray(img))  # 获取图像数据，使用了numpy
#     r, g, b, a = np.rollaxis(arr, axis=-1)
#     mask = ((r > threshold)
#             & (g > threshold)
#             & (b > threshold)
#             & (np.abs(r-g) < dist)  # 将接近白色背景的也替换掉
#             & (np.abs(r-b) < dist)
#             & (np.abs(g-b) < dist)
#             )
#     arr[mask, 3] = 0
#     img = Image.fromarray(arr, mode='RGBA')  # 转换为图像格式
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     return img

def remove_white_bg(img):
    # (1) Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY_INV)
    # (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
    print(morphed.shape)
    w, h, c = img.shape
    img = np.transpose(img, [2, 0, 1])
    z = np.ones([1, w, h]).astype(img.dtype)*255
    img = np.vstack((img, z))
    img = np.transpose(img, [1, 2, 0])
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    stencil = np.zeros([w, h, 4]).astype(img.dtype)
    color = [255, 255, 255, 255]
    cv2.fillPoly(stencil, cnts, color)
    result = cv2.bitwise_and(img, img, mask=morphed)
    result = cv2.bitwise_and(result, stencil)
    # result = CropImage(result, result.shape[0], result.shape[1])[0]
    return result


dir = "font"
dir_res = "font_trans"
imgList = os.listdir(dir)
# 按照数字进行排序后按顺序读取文件夹下的图片
# imgList.sort(key=lambda x: int(x.replace("frame", "").split('.')[0]))
print(imgList)
for count in range(0, len(imgList)):
    st = time.time()
    im_name = imgList[count]
    if (im_name == ".DS_Store"):
        continue
    im_path = os.path.join(dir, im_name)
    print("now proccessing:" + im_name)
    im = cv2.imread(im_path)
    img_re = corp_margin(im)
    # img_re = remove_white_bg(img_re)
    res_path = os.path.join(dir_res, im_name)
    cv2.imwrite(res_path, img_re)
    ed = time.time()
    print(str(round(ed-st, 2))+' seconds download finish:', im_name)
