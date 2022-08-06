# encoding:utf-8
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
from mutagen.m4a import M4A
import mutagen
import eyed3
import time
import os
import difflib


def get_mp3(mp3path):
    mp3_list = []
    for dirs, dirnames, files in os.walk(mp3path):
        for file in files:
            if file.endswith('.mp3'):
                mp3_list.append(dirs+'/'+file)
    return mp3_list


# def SetMp3Info(mp3file, info):
#     songFile = ID3(mp3file, translate=False)
#     # songFile = mutagen.File(mp3file)
#     # songFile = M4A(mp3file)
#     print(songFile)
#     songFile['APIC'] = APIC(  # 插入封面
#         encoding=3,
#         mime='image/jpeg',
#         type=3,
#         desc=u'Cover',
#         data=info['picData']
#     )
#     songFile.save()


def SetMp3Info(mp3file, info):
    songFile = eyed3.load(mp3file)
    songFile.tag.images.set(
        type_=3, img_data=info['picData'], mime_type='image/jpeg')  # 封面
    songFile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')


if __name__ == '__main__':

    img_dir = "font_trans"
    music_dir = "deemo_trans"
    # music_dir = "/Users/loujieming/Music/deemo"

    imgList = os.listdir(img_dir)
    # 按照数字进行排序后按顺序读取文件夹下的图片
    # imgList.sort(key=lambda x: int(x.replace("frame", "").split('.')[0]))
    # print(imgList)
    imgList2 = []
    for img in imgList:
        imgList2.append(img.casefold())
    imgList = imgList2

    musicList = os.listdir(music_dir)
    # print(musicList)
    musicList2 = []
    for music in musicList:
        musicList2.append(music.casefold())
    musicList = musicList2

    mp3_list = get_mp3(music_dir)
    # print(mp3_list)

    # for music in mp3_list:
    for count in range(1, len(musicList)):
        st = time.time()
        music_name = musicList[count]
        if (music_name == ".DS_Store" or not music_name.endswith(".mp3")):
            continue
        music_path = os.path.join(music_dir, music_name)

        print("now proccessing:" + music_name)

        pic_name = difflib.get_close_matches(
            music_name, imgList, 1, cutoff=0.1)[0]
        print("find pic name:" + pic_name)
        pic_dir = os.path.join(img_dir, pic_name)

        with open(pic_dir, 'rb') as f:
            picData = f.read()
        info = {
            'picData': picData,
        }
        SetMp3Info(music_path, info)

        ed = time.time()
        print(str(round(ed-st, 2))+' seconds download finish:', music_name)
