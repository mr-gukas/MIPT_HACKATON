from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
import json

# Загружаем данные из JSON файла
with open('example.json', encoding="UTF-8") as json_file:
    data = json.load(json_file)

# Создаем сеть графа
net = Network(notebook=True, 
              directed=True,
              cdn_resources='in_line',
              select_menu=True)

# Добавляем узлы в граф
colors = ['#93e1d8', '#83c5be', '#edf6f9'] 
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

def hide_1_level_node(node_name, hide):
    net.get_node(node_name)["hidden"] = hide
    children = net.get_adj_list()[node_name]
    for node_ch in children:
        net.get_node(node_ch)["hidden"] = hide

def click_button(name):
    st.session_state[name] = not st.session_state[name]

# Настройка кнопок для управления узлами
names = net.get_nodes()
for name in names[1:6]:  # Пример: берем только первые 5 узлов
    if name not in st.session_state:
        st.session_state[name] = False

    # Создаем кнопку для каждого узла
    st.button(name, on_click=click_button, args=[name])
    hide_1_level_node(name, st.session_state[name])

# net.repulsion(node_distance=0, central_gravity=1, spring_length= 0, spring_strength=0)
# net.show_buttons(filter_=['physics']) 
# net.toggle_drag_nodes(False)
# net.set_edge_smooth('horizontal')

if 'Physics on/off' not in st.session_state:
    st.session_state['Physics on/off'] = True

st.button('Physics on/off', on_click=click_button, args=['Physics on/off'])
print(st.session_state['Physics on/off'])
net.toggle_physics(st.session_state['Physics on/off'])


# net.set_options('''
#     {
#         "nodes": {
#             "font": {
#                 "face": "Arial",
#                 "size": 18
#             }
#         }
#     }
# ''')

# Заголовок для приложения
st.title("Graph Visualization")

# Генерация HTML для отображения графа
components.html(net.generate_html(), height=800, width=800)
