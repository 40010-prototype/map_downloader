import os
import traceback

import requests


def no_same_element_list(list):
    temp = []
    for item in list:
        if item not in temp:
            temp.append(item)
    return temp


def cal_col_and_row(x, y, scale):
    col = int((x + 20037507) / (40075014 / 2 ** scale))
    row = int((20037507 - y) / (40075014 / 2 ** scale))
    return col, row


def download_map(url, scale, row, col, headers):
    try:
        z = scale
        y = row
        x = col
        url = url.format(z=z, y=y, x=x)
        response = requests.get(url, headers=headers)
        print("下载成功!!!")

        return response
    except Exception:
        err = traceback.format_exc()
        print("下载失败T_T\n{}".format(err))


def save_map(pic, path, filename):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + filename + ".png", "wb") as f:
            f.write(pic.content)
            print("png保存成功!!!")
            create_w(filename, path)
    except Exception:
        err = traceback.format_exc()
        print("保存失败T_T\n{}".format(err))


def create_w(picname, path):
    scale = int(picname[6:].split("_row=")[0])
    row = int(picname[6:].split("_row=")[1].split("_col=")[0])
    col = int(picname[6:].split("_row=")[1].split("_col=")[1])
    step = int(40075014 / 2 ** scale)
    x_resolution = step / 256
    y_resolution = step / 256
    LU_y = 20037507 - (step * row)
    LU_x = (step * col) - 20037507
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + picname + ".pngw", "w") as f:
            f.write("{}\n0\n0\n-{}\n{}\n{}".format(x_resolution, y_resolution, LU_x, LU_y))
            print("w文件保存成功!!!")
    except Exception:
        err = traceback.format_exc()
        print("w文件保存失败T_T\n{}".format(err))


def main():
    url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44 "
    }
    path = "./maps/"
    scale = 15
    maps_index = []
    count = 0
    step = int(40075014 / 2 ** scale)
    for x in range(13518000, 13521001, step):
        for y in range(3636000, 3638101, step):
            col, row = cal_col_and_row(x, y, scale)
            maps_index.append([col, row])
            count += 1
    maps_index = no_same_element_list(maps_index)
    for indexs in maps_index:
        pic = download_map(url, 15, indexs[1], indexs[0], HEADERS)
        picname = "scale={}_row={}_col={}".format(scale, indexs[1], indexs[0])
        save_map(pic, path, picname)


if __name__ == main():
    main()
