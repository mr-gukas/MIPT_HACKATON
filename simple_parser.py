import os
from bs4 import BeautifulSoup
import markdown

class File_parser():
    __slots__ = ('md_files', 'parsed_res', 'markdown_parse')
    def __init__(self, path='./files', ext='.md'):
        self.md_files = [path + '/' + f for f in os.listdir(path) if f.endswith(ext)]
        if not self.md_files:
            print('Тут надо сделать обработку запуска, если нет мд файлов')
            exit(0)
        self.parsed_res = [0] * len(self.md_files)
        self.markdown_parse = markdown.Markdown()

    def parse_func(self):
        for file_ind, file_name in enumerate(self.md_files):
            with open(file_name, 'r'  ,encoding='utf-8') as f:
                parse = BeautifulSoup(self.markdown_parse.convert(f.read()), features='lxml')

            text_list = parse.find_all('p')

            self.parsed_res[file_ind] = {}
            for ind, paragraph in enumerate(text_list):
                self.parsed_res[file_ind][ind+1] = paragraph.text
            self.markdown_parse.reset()
