import os
import re
import threading
import parallel as pl
from PyPDF2.pdf import PdfFileReader
from . import PATH, store_data

ID_PATTERN = re.compile(r'201\d[12E]\d{10}')
FILE_NAME = os.path.join(PATH, 'src', 'AllStudentNameList.txt')
LOCK = threading.Lock()
PDF_BASE_PATH = os.path.join(PATH, 'src', 'pdf')
TEMP_FILE_PATH = os.path.join(PATH, 'src', 'pdf_temp')
NAME_LIST = set()


def read_pdf_page(pdf, page_num, file_name):
    page = pdf.getPage(page_num)
    content = page.extractText()
    name_list = set(re.findall(ID_PATTERN, content))
    out_file_name = os.path.join(
        TEMP_FILE_PATH, '%s.%s.txt' % (file_name, page_num))
    store_data(out_file_name, name_list)


def get_name_list_para(file_name):
    print(file_name)
    pdf_path = os.path.join(PDF_BASE_PATH, file_name)
    pdf = PdfFileReader(pdf_path)
    req_list = [(read_pdf_page, (pdf, page_num, file_name))
                for page_num in range(pdf.getNumPages())]
    pl.run_process_pool(req_list, is_lock=True, limit_num=16)


def main():
    global NAME_LIST

    file_list = os.listdir(PDF_BASE_PATH)
    for file_name in file_list:
        get_name_list_para(file_name)

    temp_file_list = os.listdir(TEMP_FILE_PATH)
    for temp_file_name in temp_file_list:
        temp_file_path = os.path.join(TEMP_FILE_PATH, temp_file_name)
        with open(temp_file_path, 'r') as temp_file:
            NAME_LIST |= set(temp_file.read().split('\n'))
        os.remove(temp_file_path)

    NAME_LIST.remove('')
    store_data(FILE_NAME, NAME_LIST)


# def time_it(num=5):
#     '测试程序用时'
#     import timeit
#     print(timeit.timeit('main()', 'from __main__ import main', number=num) / num)


if __name__ == '__main__':
    # time_it(1)
    num = 1
    import timeit
    print(timeit.timeit('main()', 'from __main__ import main', number=num) / num)
