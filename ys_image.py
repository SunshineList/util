# -- coding: utf-8 --

import os
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo, showerror
from PIL import Image
from PIL.ImageFile import ImageFile


class ImageCompress(object):
    def __init__(self):
        self.file_list = []
        self.frameT = Tk()
        # self.frameT.configure(background='lightgray')
        self.frameT.geometry("500x350+400+200")
        self.frameT.minsize(560, 350)  # 最小尺寸
        self.frameT.maxsize(560, 350)  # 最大尺寸
        self.frameT.title("v1.0 作者:Tuple 图片压缩(支持 jpg png jpeg)")
        self.v = StringVar()
        self.file_size = IntVar(value=200)
        self.frame = Frame(self.frameT)
        self.frame2 = Frame(self.frameT)
        self.frame1 = Frame(self.frameT)
        self.frame3 = Frame(self.frameT)
        self.text = Text(self.frame3, width=100, height=20, font=("宋体", 14, "bold"))  # , state='disabled')

    def gui_arrang(self):
        self.frame.pack(padx=10, pady=10)
        self.frame2.pack(padx=10, pady=10)
        self.frame1.pack(padx=10, pady=10)
        self.frame3.pack(padx=10, pady=10)
        self.text.pack(fill=Y, padx=10)

    def get_size(self, file):
        # 获取文件大小:KB
        size = os.path.getsize(file)
        return int(size / 1024)

    def get_outfile(self, infile, outfile=None):
        """
        输出文件形式 不改变原文件名
        :param infile:
        :type infile:
        :param outfile:
        :type outfile:
        :return:
        :rtype:
        """
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self, outfile, mb=280, quality=85, k=0.9):
        """不改变图片尺寸压缩到指定大小
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """

        o_size = os.path.getsize(outfile) // 1024
        print(o_size, mb)
        if o_size <= mb:
            return outfile

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        while o_size > mb:
            im = Image.open(outfile)
            x, y = im.size
            out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
            try:
                out.save(outfile, quality=quality)
            except Exception as e:
                break
            o_size = os.path.getsize(outfile) // 1024
        return outfile

    def compress_one_image(self):
        self.file_list.clear()  # 必须清除 不然压缩的时候会有问题
        if self.file_size.get() <= 0:
            showerror("失败", "压缩比太小不推荐!! 本工具无法继续")
        else:
            try:
                self.compress_image(self.v.get(), mb=self.file_size.get())
            except Exception as e:
                showerror("失败", "压缩失败 错误原因: %s" % e)
            else:
                self.text.insert(INSERT, self.v.get() + "压缩成功\n")
                # self.text.config(state='disabled')
                showinfo("成功", "压缩成功")

    def batch_compress_image(self):
        if not self.file_list:
            showerror("失败", "文件夹是空文件夹  请重新选择文件夹")
        if self.file_size.get() <= 0:
            showerror("失败", "压缩比太小不推荐!! 本工具无法继续")
        else:
            try:
                for index, file in enumerate(self.file_list):
                    print(file)
                    self.compress_image(file, mb=self.file_size.get())
                    self.text.insert(INSERT, str(file).replace("\\", "/") + "压缩成功\n\n")
            except Exception as e:
                showerror("失败", "压缩失败 错误原因: %s" % e)
            else:
                self.file_list.clear()
                # self.text.config(state='disabled')
                showinfo("成功", "文件压缩成功 请注意查看!!!")

    def choice_file(self):
        """
        选择文件
        :return:
        :rtype:
        """
        file_name = askopenfilename()
        if not file_name:
            showerror("错误", "请选择正确的文件")
        else:
            if file_name.split('.')[1] not in ('jpg', 'png', 'jpeg'):
                showerror("错误", "文件格式错误")
            else:
                if file_name:
                    self.v.set(file_name)
                self.text.delete(1.0, "end")

    def open_dir_files(self):
        """
        选择文件夹
        :return:
        :rtype:
        """
        for dirpath, dirs, files in os.walk(askdirectory()):
            for file in files:
                if file.split('.')[1] not in ('jpg', 'png', 'jpeg'):
                    self.file_list.clear()
                    showerror("错误", str(file) + "格式错误")
                else:
                    self.file_list.append(os.path.join(dirpath, file))
            self.v.set(dirpath)
            self.text.delete(1.0, "end")

    def set_size(self):
        """
        显示压缩大小
        :return:
        :rtype:
        """
        self.file_size.set(self.file_size.get())

    def run_compress(self):
        if self.file_list:
            self.batch_compress_image()
        else:
            self.compress_one_image()

    def create_window(self):
        Entry(self.frame, width=50, textvariable=self.v).pack(fill=X, side=LEFT)
        Button(self.frame, width=20, text='选择文件', font=("宋体", 14, "bold"), command=self.choice_file).pack(fill=X, padx=10)
        Button(self.frame, width=20, text='选择文件夹', font=("宋体", 14, "bold"), command=self.open_dir_files).pack(fill=Y, padx=10)
        Entry(self.frame2, width=40, textvariable=self.file_size).pack(fill=X, side=LEFT)
        Button(self.frame2, width=30, text='确定压缩大小(kb)', font=("宋体", 14, "bold"), command=self.set_size).pack(fill=X, padx=10)
        Button(self.frame1, width=10, text='压缩', font=("宋体", 14, "bold"), command=self.run_compress).pack(fill=X, side=LEFT)
        Button(self.frame1, width=10, text='退出', font=("宋体", 14, "bold"), command=self.frameT.quit).pack(fill=Y, padx=10)
        self.frame1.mainloop()


if __name__ == "__main__":
    window = ImageCompress()
    window.gui_arrang()
    window.create_window()
