from components import ocr
import tomllib as tml


def main():
    init_config()


def init_config():
    with open('config.toml', 'rb') as f:
        config = tml.load(f)
    ocr.set_tesseract_path(config['tesseract']['install_path'])


if __name__ == '__main__':
    main()
