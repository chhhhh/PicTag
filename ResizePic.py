from PIL import Image
import os
from multiprocessing import Process, Queue


class ResizePic:
    """
    多进程处理图片格式
    """

    def __init__(self, re_addr: str, width: int, height: int, rs_addr: str, p_type: str) -> None:
        self.re_addr = re_addr
        self.width = width
        self.height = height
        self.rs_addr = rs_addr
        self.p_type = p_type

    def _get_picture(self) -> list:
        """
        获取图片文件集
        :return:
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(file_path, self.re_addr)
        pictures = os.listdir(base_path)
        return pictures

    def _resize(self, curr_list, i) -> None:
        """
        处理图片
        :return:
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        re_list = os.path.join(file_path, self.re_addr)
        print("进程" + str(i+1) + ": ", end="")
        print(curr_list)
        for picture in curr_list:
            try:
                addr = os.path.join(re_list, picture)
                resize_addr = os.path.join(self.rs_addr, picture)
                print(addr)
                img = Image.open(addr)
                img = img.resize((self.width, self.height))
                img.save(resize_addr)
            except FileNotFoundError:
                print("文件名更改失败或不存在该名称！")
            except LookupError:
                print('指定了未知的编码!')
            except UnicodeDecodeError:
                print('读取文件时解码错误!')

    def multiproc_resize(self, n: int) -> None:
        """
        多进程处理机制
        :param n: 单个进程任务数
        :return:
        """
        pictures = self._get_picture()
        print(pictures)
        processes = []
        index = 0
        l = int(len(pictures) / n) + 1
        print(len(pictures))
        last = len(pictures) % n
        for i in range(l):
            if i == l:
                p = Process(target=self._resize, args=(pictures[index:index + last], i))
            else:
                p = Process(target=self._resize, args=(pictures[index:index+n], i))
            index += n
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        print("执行完成")


if __name__ == '__main__':
    result = "/Users/chenhao/PycharmProjects/PicTag/result"
    resize = "/Users/chenhao/PycharmProjects/PicTag/resize"
    p_type = 'JPG'
    rp = ResizePic(re_addr=result, width=345, height=200, rs_addr=resize, p_type=p_type)
    rp.multipro_resize(10)
