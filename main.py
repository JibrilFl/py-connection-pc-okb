import dearpygui.dearpygui as dpg
import pyperclip
import subprocess
import Data
from addFont import font

font(dpg)

with dpg.value_registry():
    dpg.add_int_value(tag="building_id")
    dpg.add_int_value(tag="room_id")
    dpg.add_int_value(tag="computer_id")
    dpg.add_string_value(default_value='All', tag="floor_current")
    dpg.add_string_value(tag="input_post")
    dpg.add_string_value(tag="building_post")

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [41, 19, 46])
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [41, 19, 46])
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [47, 57, 55])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [222, 0, 78])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, [222, 0, 78])
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [50, 20, 80])
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [220, 85, 132])
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, [41, 19, 46])
        dpg.add_theme_color(dpg.mvThemeCol_Border, [41, 19, 46])

with dpg.theme() as table_header_color_text:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])

with dpg.theme() as table_column_color_text:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [41, 19, 46])


with dpg.theme() as modal_title:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [248, 135, 255])

with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [50, 20, 80])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [222, 0, 78])

with dpg.theme() as current_item:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [248, 135, 255])

with dpg.theme() as current_floor_item:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [248, 135, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [248, 135, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 11, 7)

with dpg.theme() as table_btn:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [41, 19, 46])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [134, 0, 41])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [222, 0, 78])

with dpg.theme() as floor_padding:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 11, 7)

def copyIp(sender, app_data, user_data):
    pyperclip.copy(str(user_data))
    pyperclip.paste()
    subprocess.run([f"_internal/vncviewer/vncviewer.exe ", f"{str(user_data)}", "/password", "qwert1"])
    # _internal /
def onFloor(sender, app_data, user_data):
    if dpg.get_value('floor_current') == str(user_data):
        return

    dpg.delete_item('floor_list', children_only=True)
    dpg.delete_item('info_window', children_only=True)
    dpg.set_value("floor_current", str(user_data))
    with Data.Database() as bd:
        sql = f"SELECT * FROM Rooms WHERE Id_Buildings={dpg.get_value('building_id')}"
        if dpg.get_value("floor_current") != 'All':
            sql += f" AND Floor={user_data}"
        room = bd.query(sql)
        floors = bd.query(f'SELECT DISTINCT Floor FROM Rooms WHERE Id_Buildings={dpg.get_value("building_id")} ORDER BY Floor')
        floors.append(['All'])

    generationFloors(floors)
    generationRooms(room)

def generationBuildings():
    dpg.delete_item('buildings', children_only=True)

    with Data.Database() as bd:
        arr = bd.query('SELECT * FROM Buildings')

    for i in range(len(arr)):
        if arr[i][0] == dpg.get_value('building_id'):
            dpg.set_value('building_post', f'{arr[i][2].encode("cp1251").decode("iso8859-1")}')

            with dpg.group(parent='buildings'):
                dpg.add_separator()
                dpg.add_button(label=f'{arr[i][1]}', tag='current_item_building', width=180)
                dpg.add_input_text(default_value=f"{arr[i][2]}", height=50, width=175, multiline=True, source="building_post")
                dpg.add_button(label='Изменить', callback=postBuilding, user_data=[arr[i][0], 'Buildings', 'Location'], tag='edit')
                dpg.add_separator()
                dpg.bind_item_theme('current_item_building', current_item)
                dpg.bind_item_theme('edit', item_theme)
        else:
            dpg.add_button(label=arr[i][1], callback=add_rooms, user_data=arr[i][0], parent='buildings', width=180)
def generationRooms(arr):
    if len(arr) == 0:
        dpg.add_text('Кабинеты еще не добавлены', parent='info_window', tag='no_room')
        dpg.bind_item_theme('no_room', modal_title)
        return

    with dpg.table(parent='info_window', row_background=True, tag='room_table'):

        dpg.add_table_column(width_fixed=True, label='Кабинет', tag='room_name')
        dpg.add_table_column(label='Комментарий', tag='room_comment')
        dpg.add_table_column(width_fixed=True, label='---', tag='room3')

        dpg.bind_item_theme('room_table', table_header_color_text)
        dpg.bind_item_theme('room_name', table_column_color_text)
        dpg.bind_item_theme('room_comment', table_column_color_text)
        dpg.bind_item_theme('room3', table_column_color_text)

        for i in range(len(arr)):
            with dpg.table_row():
                for j in range(3):
                    if j == 0:
                        dpg.add_button(label=arr[i][2], tag=arr[i][0], callback=add_computers, user_data=arr[i][0])
                        dpg.bind_item_theme(arr[i][0], table_btn)
                    elif j == 1:
                        if len(arr[i][4]) >= 60:
                            dpg.add_text(f"{arr[i][4][slice(0, 57)]}...")
                        else:
                            dpg.add_text(arr[i][4])
                    else:
                        dpg.add_button(label='Редакторивать', tag=f'{arr[i][0]}-editRoom', callback=openModal, user_data=[arr[i][0], arr[i][2], arr[i][4], 'Rooms', 'Comments'])
                        dpg.bind_item_theme(f'{arr[i][0]}-editRoom', item_theme)


def postBuilding(sender, app_data, user_data):
    with Data.Database() as bd:
        bd.execute(f"UPDATE {user_data[1]} SET {user_data[2]}='{dpg.get_value('building_post').encode('iso8859-1').decode('cp1251')}' WHERE Id={str(user_data[0])}")

    generationBuildings()

def generationFloors(arr):
    with dpg.table(header_row=False, parent='floor_list', resizable=False, no_host_extendX=True, no_pad_innerX=True):
        for f in range(len(arr)):
            dpg.add_table_column(width_fixed=True)

        with dpg.table_row():
            for k in range(len(arr)):
                if dpg.get_value('floor_current') == str(arr[k][0]):
                    dpg.add_button(label=f'{arr[k][0]}', tag='active_floor', callback=onFloor, user_data=arr[k][0])
                    dpg.bind_item_theme('active_floor', current_floor_item)
                else:
                    dpg.add_button(label=f'{arr[k][0]}', tag=f'{arr[k][0]}-{dpg.get_value("building_id")}', callback=onFloor, user_data=arr[k][0])
                    dpg.bind_item_theme(f'{arr[k][0]}-{dpg.get_value("building_id")}', floor_padding)

def generationComputers(arr):
    if len(arr) == 0:
        dpg.add_text('Компьютеров еще нет в базе', parent='info_window', tag='no_computer')
        dpg.bind_item_theme('no_computer', modal_title)
        return

    with dpg.table(parent='info_window', row_background=True, tag='computer_table'):

        dpg.add_table_column(label='ОС', width_fixed=True, tag='OC')
        dpg.add_table_column(label='Комментарий', tag="Comments-comp")
        dpg.add_table_column(label='IP', width_fixed=True, tag='IP')
        dpg.add_table_column(label='---', width_fixed=True, tag='comp4')
        dpg.add_table_column(label='---', width_fixed=True, tag='comp5')

        dpg.bind_item_theme('computer_table', table_header_color_text)
        dpg.bind_item_theme('OC', table_column_color_text)
        dpg.bind_item_theme('Comments-comp', table_column_color_text)
        dpg.bind_item_theme('IP', table_column_color_text)
        dpg.bind_item_theme('comp4', table_column_color_text)
        dpg.bind_item_theme('comp5', table_column_color_text)

        for i in range(len(arr)):
            with dpg.table_row():
                for j in range(5):
                    if j == 0:
                        dpg.add_text(f'{arr[i][3]}')
                    elif j == 1:
                        dpg.add_text(arr[i][4])
                    elif j == 2:
                        dpg.add_text(arr[i][1])
                    elif j == 3:
                        dpg.add_button(label='Подключиться', callback=copyIp, user_data=arr[i][1], tag=f'{arr[i][0]}-connectComputer')
                        dpg.bind_item_theme(f'{arr[i][0]}-connectComputer', table_btn)
                    else:
                        dpg.add_button(label='Редакторивать', tag=f'{arr[i][0]}-editComputer', callback=openModal, user_data=[arr[i][0], arr[i][1], arr[i][4], 'Computers', 'Comments'])
                        dpg.bind_item_theme(f'{arr[i][0]}-editComputer', item_theme)
def add_rooms(sender, app_data, user_data):
    dpg.delete_item('info_window', children_only=True)
    dpg.delete_item('btn_back', children_only=True)
    dpg.delete_item('floor_list', children_only=True)
    dpg.set_value('building_id', user_data)

    with Data.Database() as bd:
        sql = f"SELECT * FROM Rooms WHERE Id_Buildings={user_data}"
        if dpg.get_value("floor_current") != 'All':
            sql += f" AND Floor={dpg.get_value('floor_current')}"

        room = bd.query(sql)
        floors = bd.query(f'SELECT DISTINCT Floor FROM Rooms WHERE Id_Buildings={user_data} ORDER BY Floor')
        floors.append(['All'])
        generationFloors(floors)

    generationRooms(room)
    generationBuildings()

def add_computers(sender, app_data, user_data):
    dpg.delete_item('info_window', children_only=True)
    dpg.delete_item('floor_list', children_only=True)
    dpg.set_value('room_id', user_data)
    dpg.add_button(label='Назад', callback=back_room, parent='btn_back')

    with Data.Database() as bd:
        computers = bd.query(f"SELECT * FROM Computers WHERE idRoom={user_data}")

    generationComputers(computers)

def postData(sender, app_data, user_data):
    dpg.configure_item("modal_id", show=False)
    dpg.delete_item('modal_id', children_only=True)

    if user_data == None:
        return

    dpg.delete_item('info_window', children_only=True)
    with Data.Database() as bd:
        bd.execute(f"UPDATE {user_data[1]} SET {user_data[2]}='{dpg.get_value('input_post').encode('iso8859-1').decode('cp1251')}' WHERE Id={str(user_data[0])}")

        if user_data[1] == 'Rooms':
            room = bd.query(f"SELECT * FROM Rooms WHERE Id_Buildings={dpg.get_value('building_id')}")
            generationRooms(room)
        elif user_data[1] == 'Computers':
            computers = bd.query(f"SELECT * FROM Computers WHERE idRoom={dpg.get_value('room_id')}")
            generationComputers(computers)

def openModal(sender, app_data, user_data):

    dpg.add_text(f"{user_data[1]}", parent="modal_id", tag='m_title')
    dpg.add_separator(parent="modal_id")
    dpg.set_value('input_post', f'{user_data[2].encode("cp1251").decode("iso8859-1")}')
    dpg.add_input_text(default_value=f"{user_data[2]}", height=50, width=480, parent="modal_id", multiline=True, source="input_post")
    with dpg.group(horizontal=True, parent="modal_id"):
        dpg.add_button(label="Подтвердить", width=105, callback=postData, user_data=[user_data[0], user_data[3], user_data[4]], tag="save")
        dpg.add_button(label="Закрыть", width=80, callback=postData)
    dpg.configure_item("modal_id", show=True)
    dpg.bind_item_theme('m_title', modal_title)
    dpg.bind_item_theme('save', item_theme)

with dpg.window(modal=True, show=False, pos=(340, 200), width=500, height=130, tag="modal_id", no_title_bar=True, no_resize=True):
    pass


def back_room():
    dpg.delete_item('info_window', children_only=True)
    dpg.delete_item('btn_back', children_only=True)

    with Data.Database() as bd:
        room = bd.query(f"SELECT * FROM Rooms WHERE Id_Buildings={dpg.get_value('building_id')}")
        floors = bd.query(f"SELECT DISTINCT Floor FROM Rooms WHERE Id_Buildings={dpg.get_value('building_id')} ORDER BY Floor")
        floors.append(['All'])

    generationFloors(floors)
    generationRooms(room)



with dpg.window(label="Example Window", pos=(0, 0), width=200, height=600, no_title_bar=True, no_move=True, no_resize=True, tag='buildings'):
    pass

with dpg.window(label="Example Window", width=730, height=100, pos=(205, 0), no_title_bar=True, no_move=True, no_resize=True):
    with dpg.child_window(height=25, pos=(5, 15), border=False, tag="btn_back"):
        pass
    with dpg.child_window(height=40, pos=(5, 45), border=False, tag="floor_list"):
        pass


with dpg.window(label="Example Window", pos=(205, 105), width=730, height=495, no_title_bar=True, no_move=True, no_resize=True, tag="info_window"):
    pass

dpg.create_viewport(title='Kompudahteri OKB2', width=935, height=600, resizable=False, small_icon='_internal/vncviewer/hospital.ico')
# //_internal

dpg.bind_theme(global_theme)
generationBuildings()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_con