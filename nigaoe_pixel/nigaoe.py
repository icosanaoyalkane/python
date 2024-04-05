# -*- coding: utf-8 -*- #
#https://qiita.com/wataoka/items/261fc12c956a517049d8
import sys
import emoji
import numpy as np
from PIL import Image


def draw(path: str, col: int = 50) -> None:
    print('.draw')
    tsuki_matrixs = load_tsuki_matrixs()
    img = preprocess(path, col)

    tsuki_list = []
    for i in range(int(np.shape(img)[0]/4)):
        for j in range(int(np.shape(img)[1]/4)):
            row = 4*i
            col = 4*j
            max = -10000
            max_tk = 0
            for n, tk in enumerate(tsuki_matrixs):
                hadamard = np.multiply(img[row:row+4, col:col+4], tk)
                if max < hadamard.sum():
                    max_index = n
                    max = hadamard.sum()
            tsuki_list.append(index2tsuki(max_index))
        tsuki_list.append('\n')

    for i in tsuki_list:
        sys.stdout.write(i)


def load_tsuki_matrixs():

    black = np.matrix([[-1, -1, -1, -1],
                        [-1, -1, -1, -1],
                        [-1, -1, -1, -1],
                        [-1, -1, -1, -1]])

    white = np.matrix([[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]])

    return [black, white]


def index2tsuki(index):
    """
    indexから絵文字対応する絵文字を返す関数
    Args:
        index
    Return:
        絵文字
    """
    if index==0:
        return emoji.emojize(':black_circle:')

    else:
        return emoji.emojize(':white_circle:')


def preprocess(path, col):
    """
    画像の前処理。グレスケール、画質下げ、その他前処理。
    Args:
        path: 画像のパス
        col: 月の列の数
    Return:
        img: 前処理が完了したnumpyの行列
    """
    img = Image.open(path)
    img = img.convert('L')

    width = col*4
    height = int(width*(img.height/img.width))
    height -= height%4

    img = img.resize((width, height))
    img = np.matrix(img)
    img = (img/128.) - 1.

    return img
