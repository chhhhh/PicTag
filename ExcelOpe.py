import os
import shutil
import xlrd


class ExcelOpe:
    """
    读取操作Excel表中的数据并实现图片的重命名。
    """

    def __init__(self, xl_addr: str, p_addr: str, re_addr: str) -> None:
        """
        初始化
        :param xl_addr: Excel编号表的地址
        :param p_addr: 待命名图片地址
        :param re_addr: 结果地址
        """
        self.re_addr = re_addr
        self.p_addr = p_addr
        self.xl_addr = xl_addr

    def _init_read(self) -> list:
        """
        读取Excel列表
        :return:
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(file_path, self.xl_addr)
        book = xlrd.open_workbook(base_path)
        sheet1 = book.sheets()[0]
        n_rows = sheet1.nrows
        print('表格总行数', n_rows)
        n_cols = sheet1.ncols
        print('表格总列数', n_cols)
        nums = sheet1.col_values(0)
        print(nums)
        return nums

    def _del_dir(self) -> None:
        """
        清空结果文件夹
        :return:
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        re_dir = os.path.join(file_path, self.re_addr)
        shutil.rmtree(re_dir)
        os.mkdir(re_dir)

    def batch_rename(self) -> None:
        """
        批量重命名文件名
        :return:
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        base_files = os.path.join(file_path, self.p_addr)
        files = os.listdir(base_files)

        result_list = os.path.join(file_path, self.re_addr)

        files.sort(key=lambda x: int(x.split('.')[0]))
        print(files)
        # 清空原目录
        self._del_dir()
        # 获取Excel列表
        num = [int(n) for n in self._init_read()]
        # 批处理重命名图片
        for i, file in enumerate(files):
            if file.endswith('.jpg'):
                src = os.path.join(base_files, file)
                dst = os.path.join(result_list, str(num[i]) + '.jpg')
                try:
                    os.rename(src, dst)
                    print('文件重命名 %s to %s' % (src, dst))
                except FileNotFoundError:
                    print("文件名更改失败或不存在该名称！")
                except LookupError:
                    print('指定了未知的编码!')
                except UnicodeDecodeError:
                    print('读取文件时解码错误!')


if __name__ == '__main__':
    xl = "/Users/chenhao/PycharmProjects/PicTag/table1.xlsx"
    p = "/Users/chenhao/PycharmProjects/PicTag/pictures"
    re = "/Users/chenhao/PycharmProjects/PicTag/result"
    op = ExcelOpe(xl_addr=xl, p_addr=p, re_addr=re)
    op.batch_rename()
