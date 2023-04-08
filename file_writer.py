import os
import traceback


def write_map(map, filename):
    path = "./maps/"
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + filename + ".png", "wb") as f:
            f.write(map.content)
            # print("png保存成功!!!")
            write_w(filename, path)
    except Exception:
        err = traceback.format_exc()
        print("保存失败T_T\n{}".format(err))


def write_w(picname, path):
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
            # print("w文件保存成功!!!")
    except Exception:
        err = traceback.format_exc()
        print("w文件保存失败T_T\n{}".format(err))
