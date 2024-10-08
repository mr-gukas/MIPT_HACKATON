import os
import markdown
from collections import Counter
from bs4 import BeautifulSoup
import json
import mistune


class File_parser():
    def __init__(self, path='.', ext='.md'):
        self.md_files = [f for f in os.listdir(path) if f.endswith(ext)]
        if not self.md_files:
            print('Тут надо сделать обработку запуска, если нет мд файлов')
            exit(0)

        self.markdown_file = markdown.Markdown(extensions=['toc'])
        
        self.parsed_res = [0] * len(self.md_files)

    def parse_func(self):
        for file_num, file_name in enumerate(self.md_files):
            with open(file_name, 'r'  ,encoding='utf-8') as f:
                parse = BeautifulSoup(mistune.html(f.read()), features='lxml')
                # parse = BeautifulSoup(self.markdown_file.convert(f.read()), features='lxml')

            text_list = parse.find_all()[2:]
            # print(text_list)
            # return
            self.parsed_res[file_num] = {}
            self.parsed_res[file_num]['file_id'] = file_num
            self.parsed_res[file_num]['title'] = file_name[:-3]
            self.parsed_res[file_num]['sections'] = []

            cur_level = 1
            pars_level = self.parsed_res[file_num]['sections']
            section_counter = Counter()
            last_with_selected_level = {}

            last_with_selected_level[0] = self.parsed_res[file_num]['sections']


            for elem in text_list:
                # print(text_list)
                match elem.name:
                    case 'p':
                        pars_level.append({'type':'paragraph', 'text':elem.get_text()})
                    case 'ul':
                        pars_level.append({'type':'list', 'content':[]})
                    case 'li':
                        pars_level[-1]['content'].append(elem.get_text())
                    case 'em':
                        if 'italicized text' not in pars_level[-1].keys():
                            pars_level[-1]['italicized text'] = []
                        pars_level[-1]['italicized text'].append(elem.get_text())
                    case 'strong':
                        if 'bold text' not in pars_level[-1].keys():
                            pars_level[-1]['bold text'] = []
                        pars_level[-1]['bold text'].append(elem.get_text())
                    case _:
                        if elem.name[0] == 'h':
                            new_level = int(elem.name[1])

                            if new_level < cur_level:
                                pars_level = last_with_selected_level[new_level]
                            elif new_level >= cur_level:
                                last_with_selected_level[cur_level] = pars_level

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
            self.markdown_file.reset()

a = File_parser()
a.parse_func()
import pprint

pprint.pprint(json.loads(json.dumps(a.parsed_res), ))
# with open('lermontov.md', 'w') as f:
#     f.write(json.dumps(a.parsed_res))

# Добавить обработку кода, зачёркнутых строчек