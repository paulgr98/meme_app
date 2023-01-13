import json
import os
from components import ocr


class MemeManager(object):
    def __init__(self):
        self.memes_file_path = 'memes.json'

    def load_memes(self) -> dict[str, dict[str, list[str]]]:
        # check if memes.json exists
        if not os.path.exists(self.memes_file_path):
            with open(self.memes_file_path, 'w') as f:
                json.dump({}, f)
        # if file exists but doesn't contain json, delete it and create new one with empty dict
        try:
            with open(self.memes_file_path, 'r') as f:
                _ = json.load(f)
        except json.decoder.JSONDecodeError:
            # delete the file
            os.remove(self.memes_file_path)
            # create new file with empty dict
            with open(self.memes_file_path, 'w') as f:
                json.dump({}, f)

        with open(self.memes_file_path, 'r') as f:
            memes = json.load(f)
        return memes

    def save_memes(self, memes: list[str]) -> None:
        meme_content_dir = self.load_memes()
        for meme in memes:
            if meme not in meme_content_dir:
                meme_img = ocr.get_image(meme)
                meme_content_dir[meme] = {'content': ocr.get_text(meme_img)}

        with open(self.memes_file_path, 'w') as f:
            json.dump(meme_content_dir, f, indent=4)

    def find_memes(self, content: str, description: str) -> list[str]:
        memes = self.load_memes()
        results = []
        # if content in not empty, search for memes with that content
        if content.strip() != '':
            for meme, data in memes.items():
                if _check_match_in_content(content, data):
                    results.append(meme)
        # if description is not empty, search for memes with that description
        if description.strip() != '':
            for meme, data in memes.items():
                if _check_match_in_description(description, data):
                    results.append(meme)
        return results


def _check_match_in_content(content: str, data: dir) -> bool:
    for text in data['content']:
        if content.lower() in text.lower():
            return True
    return False


def _check_match_in_description(description: str, data: dir) -> bool:
    for text in data['description']:
        if description.lower() in text.lower():
            return True
    return False
