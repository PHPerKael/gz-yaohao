#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from io import BytesIO
import random
import time
from urllib import parse
import requests
import pytesseract
import cv2
from PIL import Image
from pprint import pprint

class yaohaologin(object):
    """docstring for yaohaologin"""
    def __init__(self, phone, pwd):
        self.phone = phone
        self.pwd = pwd
        self.headers = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        self.cookies = {}
        self.rd = ""
    def login(self):
        captcha = self.getCaptcha()

        url = "https://apply.jtj.gz.gov.cn/apply/user/person/login.html"
        data = {
            "userType": 0,
            "userTypeSelect": 0,
            "personMobile": self.phone,
            "loginType": "mobile",
            "unitLoginTypeSelect": 0,
            "password": self.pwd,
            "validCode": captcha
        }
        response = requests.post(url, data, headers=self.headers, cookies=self.cookies)
        pprint(response.status_code)
        responseUrl = requests.utils.unquote(response.url)
        pprint(responseUrl)

        if responseUrl.find("login.html") == -1:
            parseResult = parse.urlparse(responseUrl)
            paramDict = parse.parse_qs(parseResult.query)
            self.rd = paramDict['rd'][0]
            pprint("rd = " + self.rd)
            return True
        return False


    def getCaptcha(self):
        response = requests.get("https://apply.jtj.gz.gov.cn/apply/validCodeImage.html?ee=2", cookies=self.cookies, headers=self.headers)
        self.cookies = response.cookies
        filename = os.getcwd() + "/runtime/" + str(time.strftime("%Y-%m-%d_%H-%M-%S")) + "-captcha"
        imagename = filename + ".jpg"
        with open(imagename, "wb") as imgfile:
            imgfile.write(response.content)
        # 1. 新图片
        image = Image.open(imagename)
        codeStr = pytesseract.image_to_string(image)
        pprint("raw: " + codeStr.replace("\n", "").replace(" ", ""))

        mainColors = self.mainColorFilter(image)
        # imgSplit = self.imageMainColorSplit(image, mainColors)

        filterImg = self.transToBin(image, mainColors)
        filterImg.save(filename + "-main-color-filter.jpg")
        codeStr = pytesseract.image_to_string(filterImg)
        pprint("main color filter: " + codeStr.replace("\n", "").replace(" ", ""))

        # denoiceImg = self.reduceNoise(filterImg)
        # denoiceImg.save(filename + "-denoice.jpg")
        #
        # codeStr = pytesseract.image_to_string(denoiceImg)
        # pprint("denoice: " + codeStr.replace("![a-z0-9A-Z]", "").replace("\n", ""))
        return codeStr

    def imageToBin(self, image, filename):
        # 这个是二值化阈值
        threshold = 250
        table = []
        for j in range(256):
            if j < threshold:
                table.append(0)
            else:
                table.append(1)
        # 通过表格转换成二进制图片，1的作用是白色，0就是黑色
        imagebbin = image.point(table, "1")
        imagebbin.save(filename + "-handle.jpg")
        return  imagebbin

    def reduceNoise(self, image):
        rows, cols = image.size  # 图片的宽度和高度
        change_pos = []  # 记录噪声点位置

        for i in range(0, rows):
            change_pos.append((i, 0))
            change_pos.append((i, cols - 1))
        for j in range(0, cols):
            change_pos.append((0, j))
            change_pos.append((rows - 1, j))

        # 遍历图片中的每个点，除掉边缘
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # 接壤的像素为黑色的数量<=1, 则判断为噪点
                count = 0
                if image.getpixel((i - 1, j)) == (0, 0, 0):
                    count += 1

                if image.getpixel((i, j - 1)) == (0, 0, 0):
                    count += 1

                if image.getpixel((i + 1, j)) == (0, 0, 0):
                    count += 1

                if image.getpixel((i, j + 1)) == (0, 0, 0):
                    count += 1

                if count <= 1:
                    change_pos.append((i, j))

        # 对相应位置进行像素修改，将噪声处的像素置为1（白色）
        for pos in change_pos:
            image.putpixel(pos, (255, 255, 255))

        return image  # 返回修改后的图片

    def mainColorFilter(self, image):
        dict = {}
        rows, cols = image.size  # 图片的宽度和高度
        for i in range(0, rows):
            for j in range(0, cols):
                pixel = image.getpixel((i, j))
                if pixel != (255, 255, 255):
                    if pixel not in dict:
                        dict[pixel] = 0
                    dict[pixel] += 1
        dict = sorted(dict.items(), key=lambda item:item[1], reverse=True)
        newdict = {}
        lastnum = 0
        for color in dict:
            if lastnum == 0 or color[1] / lastnum > 0.5:
                newdict[color[0]] = color[1]
                lastnum = color[1]
                pass
        return newdict

    def transToBin(self, image, mainColors):
        rows, cols = image.size  # 图片的宽度和高度
        for i in range(0, rows):
            for j in range(0, cols):
                pixel = image.getpixel((i, j))
                if pixel in mainColors:
                    image.putpixel((i, j), (0, 0, 0))
                    pass
                else:
                    image.putpixel((i, j), (255,255,255))
        return image

    def imageMainColorSplit(self, image, mainColors):
        return 1

    def renewal(self):
        renewalUrl = "https://apply.jtj.gz.gov.cn/apply/person/keepUp.do?rd=" + self.rd
        response = requests.get(renewalUrl, cookies=self.cookies, headers=self.headers)
        pprint(response.status_code)
        responseUrl = requests.utils.unquote(response.url)
        pprint(responseUrl)
        if responseUrl.find("已确认延期") >= 0:
            return True
        else:
            return False
