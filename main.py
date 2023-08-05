import PySimpleGUI as sg

sg.theme('Default 1')
def run_program_1():
    import vk

def run_program_2():
    import twitter

layout = [
    [sg.Text("Добро пожаловать в программу для сравнения и анализа аудиторий социальных сетей!")],
    [sg.Text("Выберите программу для запуска:")],
    [sg.Button("Запустить программу для ВКонтакте", size=(40, 1))],
    [sg.Button("Запустить программу для Twitter", size=(40, 1))],
    [sg.Button("Выход", size=(10, 1), button_color=("white", "firebrick3"), pad=((450, 0), (10, 10)))]
]

window = sg.Window("Сравнение и анализ аудитории социальных сетей", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Выход":
        break
    elif event == "Запустить программу для ВКонтакте":
        window.close()
        run_program_1()
    elif event == "Запустить программу для Twitter":
        window.close()
        run_program_2()
window.close()
