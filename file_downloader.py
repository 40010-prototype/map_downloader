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
        # print("下载成功!!!")

        return response
    except Exception:
        err = traceback.format_exc()
        print("下载失败T_T\n{}".format(err))
