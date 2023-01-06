from components import ocr
from components import toml_w
import tomllib as tml
import PySimpleGUI as sg


def main() -> None:
    init_config()
    window = init_gui()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'exit':
            break
        elif event == 'find':
            print('find')
        elif event == 'add_folder':
            on_add_folder_click()
    window.close()


def init_config() -> None:
    try:
        config = load_config()
        ocr.set_tesseract_path(config['tesseract']['install_path'])
    except FileNotFoundError:
        print('config.toml not found')


def load_config() -> dict:
    with open('config.toml', 'rb') as f:
        config = tml.load(f)
    return config


def init_gui() -> sg.Window:
    sg.theme('DarkAmber')
    layout = [
        [sg.Column(
            [
                [sg.Text('')],  # spacer
                [sg.Button('Find Meme!', key='find', size=(20, 1))],
                [sg.Button('Add Meme Folder', key='add_folder', size=(20, 1))],
                [sg.Button('Exit', key='exit', size=(20, 1))]
            ],
            justification='center')],
    ]

    return sg.Window('Meme App', layout, size=(400, 300))


def on_add_folder_click() -> None:
    add_folder_layout = [
        [sg.Text('Your Meme Folder:')],
        [sg.InputText(key='meme_folder', size=(30, 1)), sg.FolderBrowse('Browse', key='browse', size=(10, 1))],
        [sg.Button('Save', key='save', size=(10, 1))]
    ]
    add_folder_window = sg.Window('Add Meme Folder', add_folder_layout, size=(400, 300))

    # read meme folder location from config
    config = load_config()

    meme_folder = config['app']['meme_dir']
    add_folder_window.finalize()
    add_folder_window['meme_folder'].update(meme_folder)
    add_folder_window.refresh()

    while True:
        add_folder_event, add_folder_values = add_folder_window.read()
        match add_folder_event:
            case 'save':
                config['app']['meme_dir'] = add_folder_values['meme_folder']
                save_config(config)
                break
            case sg.WIN_CLOSED:
                add_folder_window.close()
                break
    add_folder_window.close()


def save_config(config: dict) -> None:
    with open('config.toml', 'wb') as f:
        data = toml_w.dumps(config)
        f.write(data.encode('utf-8'))


if __name__ == '__main__':
    main()
