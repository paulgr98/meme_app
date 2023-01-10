from components import ocr
from components import toml_w
from components import meme_manager
import tomllib as tml
import PySimpleGUI as sg
import os


def main() -> None:
    init_config()
    window = init_gui()
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED | 'exit':
                break
            case 'find':
                print('find')
            case 'add_folder':
                on_add_folder_click()
            case 'add_meme':
                on_add_meme_click()
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
                [sg.Button('Edit Meme Folder', key='add_folder', size=(20, 1))],
                [sg.Button('Add Meme(s)', key='add_meme', size=(20, 1))],
                [sg.Button('Exit', key='exit', size=(20, 1))]
            ],
            justification='center')],
    ]

    return sg.Window('Meme App', layout, size=(400, 300))


def on_add_folder_click() -> None:
    add_folder_layout = [
        [sg.Column(
            [
                [sg.Text('')],  # spacer
                [sg.Text('Your Meme Folder:')],
                [sg.InputText(key='meme_folder', size=(30, 1)), sg.FolderBrowse('Browse', key='browse', size=(10, 1))],
                [sg.Button('Save', key='save', size=(10, 1))]
            ],
            justification='center')],
    ]
    add_folder_window = sg.Window('Edit Meme Folder', add_folder_layout, size=(400, 300))

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


def on_add_meme_click() -> None:
    add_meme_layout = [
        [sg.Column(
            [
                [sg.Text('')],  # spacer
                [sg.Text('Update whole meme folder: '), sg.Button('Update', key='update', size=(10, 1))],
                [sg.Text('OR')],
                [sg.Text('Add single meme:')],
                [sg.FileBrowse('Browse', key='browse', size=(10, 1), file_types=(("Image", "*.png *.jpg"),)),
                 sg.Button('Add', key='add', size=(10, 1))],
                [sg.Text('')],  # spacer
                [sg.Text('', key='result', size=(30, 1))]
            ],
            justification='center')],
    ]
    add_meme_window = sg.Window('Add Meme(s)', add_meme_layout, size=(400, 300))
    add_meme_window.finalize()

    manager = meme_manager.MemeManager()

    while True:
        add_meme_event, add_meme_values = add_meme_window.read()
        match add_meme_event:
            case 'add':
                meme_path = add_meme_values['browse']
                meme_name = meme_path.split('/')[-1]
                add_meme_window['result'].update(f'{meme_name} added')
                break
            case 'update':
                config = load_config()
                meme_folder = config['app']['meme_dir']
                memes = load_memes(meme_folder)
                manager.save_memes(memes)
                add_meme_window['result'].update(f'{len(memes)} memes added')
                break
            case sg.WIN_CLOSED:
                add_meme_window.close()
                break


def load_memes(path: str) -> list[str]:
    # save full path to all .png and .jpg files in path
    memes = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                memes.append(f'{root}/{file}')
    return memes


def save_config(config: dict) -> None:
    with open('config.toml', 'wb') as f:
        data = toml_w.dumps(config)
        f.write(data.encode('utf-8'))


if __name__ == '__main__':
    main()
