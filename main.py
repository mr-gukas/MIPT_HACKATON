from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
import os
import time
import json
# import model


# Имена загруженных файлов
uploaded_file_names = []

# Цвета узлов графа
colors = ['#93e1d8', '#83c5be', '#edf6f9'] 
# TODO: Можно добавить вмджет для выбор цветов


def disappearing_message(mess, sec=2):
    with st.spinner(mess):
        time.sleep(sec)



def uploader():
    uploaded_files = st.file_uploader(label="Upload .md files, limited to 200MB",
                                  type=['md'],
                                  accept_multiple_files=True,
                                  help="Choose and upload .md files")

    # Сохраняем файлы
    if uploaded_files is not None:
        for file in uploaded_files:
            if file.name not in uploaded_file_names:
                uploaded_file_names.append(file.name)
                with open(os.path.join("cache", file.name),"wb") as f: 
                    f.write(file.getbuffer())

def settings(net):
    with st.sidebar:
        st.title('Settings')
        net.toggle_physics(st.toggle("Physics on/off"))
        for i, color in enumerate(colors):       
            color = st.color_picker("Pick A Color", color)
            colors[i] = color
            st.write("The current color is", color)

def main():

    # Загрузчик файлов пользователя
    uploader()

    # Код Жени
    # model.generate_json_output()

    # Загружаем данные обработанные моделью из JSON файла
    with open('example.json', encoding="UTF-8") as json_file:
        data = json.load(json_file)

    # Создаем сеть графа
    net = Network(notebook=True, 
                directed=True,
                cdn_resources='in_line',
                select_menu=True)

   
    settings(net)
    # TODO: Добавить выбор большей функциональности и вынести их в виджеты
    for elem in data:
        net.add_node(elem["data"],
                    level=elem["level"], 
                    title=elem["data"], 
                    shape='box',
                    mass=(elem["level"] + 1), 
                    color=colors[elem["level"]]) # title позволяет отображать текст при наведении

    # Добавляем рёбра между узлами
    for elem in data:
        if elem["prev_num"] is None:
            continue
        for prev_node in data:
            if prev_node["num"] == elem["prev_num"] and elem["level"] - 1 == prev_node["level"]:
                net.add_edge(prev_node["data"], elem["data"])

    def click_button(name):
        st.session_state[name] = not st.session_state[name]

    # if 'Physics on/off' not in st.session_state:
    #     st.session_state['Physics on/off'] = True

    # st.button('Physics on/off', on_click=click_button, args=['Physics on/off'])
    # print(st.session_state['Physics on/off'])
    # net.toggle_physics(st.session_state['Physics on/off'])

    
    
    # Заголовок для приложения
    st.title("Mind map")

    # Генерация HTML для отображения графа
    components.html(net.generate_html(notebook=True), height=600, width=800)


    if 'balloons' not in st.session_state:
        st.session_state['balloons'] = False

    if st.button('BaLlOoNs', on_click=click_button, args=['balloons']):
        st.balloons()



if __name__ == "__main__":
    main()