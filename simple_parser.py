import os
from bs4 import BeautifulSoup
import json
import markdown
import multiprocessing as mp

class File_parser():
    __slots__ = ('md_files', 'parsed_res')
    def __init__(self, path='./files', ext='.md'):
        self.md_files = [path + '/' + f for f in os.listdir(path) if f.endswith(ext)]
        if not self.md_files:
            print('Тут надо сделать обработку запуска, если нет мд файлов')
            exit(0)
        self.parsed_res = 0

    def file_parse(self):
        with mp.Pool(len(self.md_files)) as p:
            self.parsed_res = p.map(self.parse_func, self.md_files)
    @staticmethod
    def parse_func(file_name):
        with open(file_name, 'r'  ,encoding='utf-8') as f:
            parse = BeautifulSoup(markdown.markdown(f.read()), features='lxml')

        text_list = parse.find_all('p')
        parsed_res = {}
        for ind, paragraph in enumerate(text_list):
            parsed_res[ind+1] = paragraph.text
        
        return parsed_res
        
if __name__ == '__main__':
    a = File_parser()
    a.file_parse()
    with open("data.json", "w") as json_file:
        json.dump(a.parsed_res, json_file)
