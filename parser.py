import os
from collections import Counter
from bs4 import BeautifulSoup
import json
import mistune
import multiprocessing as mp
import time

class File_parser():
    __slots__ = ('md_files', 'parsed_res')
    def __init__(self, path='.', ext='.md'):
        self.md_files = [f for f in os.listdir(path) if f.endswith(ext)]
        if not self.md_files:
            print('Тут надо сделать обработку запуска, если нет мд файлов')
            exit(0)
        self.parsed_res = 0

    def file_parse(self):
        with mp.Pool(len(self.md_files)) as p:
            self.parsed_res = p.map(self.parse_func, list(enumerate(self.md_files)))
    @staticmethod
    def parse_func(file):
        file_num = file[0]
        file_name = file[1]
        with open(file_name, 'r'  ,encoding='utf-8') as f:
            parse = BeautifulSoup(mistune.html(f.read()), features='lxml')

        text_list = parse.find_all()[2:]
        # print(text_list)
        parsed_res = {}
        parsed_res['file_id'] = file_num
        parsed_res['title'] = file_name[:-3]
        parsed_res['sections'] = []

        cur_level = 1
        pars_level = parsed_res['sections']
        section_counter = Counter()
        last_with_sel_level = [0] * 6

        last_with_sel_level[cur_level-1] = parsed_res['sections']


        for elem in text_list:
            match elem.name:
                case 'p':
                    pars_level.append({'type':'paragraph', 'text':elem.get_text()})
                case 'ul':
                    pars_level.append({'type':'list', 'content':[]})
                case 'li':
                    pars_level[-1]['content'].append(elem.get_text())
                case 'em':
                    File_parser.append_spec_text(pars_level, 'italicized_text', elem.get_text())
                case 'strong':
                    File_parser.append_spec_text(pars_level, 'bold_text', elem.get_text())
                case 'del':
                    File_parser.append_spec_text(pars_level, 'strikethrough_text', elem.get_text())
                case 'code':
                    File_parser.append_spec_text(pars_level, 'code_text', elem.get_text())
                case _:
                    if elem.name[0] == 'h':
                        new_level = int(elem.name[1])

                        #Блок обрабатывает случаи, когда был переход с пропуском уровня(к примеру 1->4), а также удаляет историю уровней с предыдущих блоков     
                        if new_level <= cur_level:
                            if last_with_sel_level[new_level-1] != 0:
                                pars_level = last_with_sel_level[new_level-1]
                            else:
                                for level in last_with_sel_level[::-1]:
                                    if level != 0:
                                        pars_level = level
                                        break
                            last_with_sel_level = last_with_sel_level[:new_level] + [0] * (6 - new_level)

                        elif new_level > cur_level:
                            last_with_sel_level[cur_level] = pars_level

                        cur_level = new_level
                        section_counter[cur_level] += 1
                        

                        new_section = {}
                        new_section['type'] = 'header'
                        new_section['section_id'] = section_counter[cur_level]
                        new_section['level'] = cur_level
                        new_section['header'] = elem.get_text()
                        new_section['content'] = []
                        pars_level.append(new_section)
                        
                        pars_level = new_section['content']
        return parsed_res

    @staticmethod
    def append_spec_text(pars_level, key, text):
        if key not in pars_level[-1].keys():
            pars_level[-1][key] = []
        pars_level[-1][key].append(text)
if __name__ == '__main__':
    a1 = time.time()
    a = File_parser()
    a.file_parse()
    with open("data.json", "w") as json_file:
        json.dump(a.parsed_res, json_file)
    print(time.time()-a1)
