import os
import shutil

class FileInputClassifier:
    def __init__(self, base_folder=None):
        if base_folder is None:
            base_folder = os.path.abspath(os.path.dirname(__file__))

        self.paths = {
            "text": os.path.join(base_folder, "text"),
            "audio": os.path.join(base_folder, "audio"),
            "img": os.path.join(base_folder, "img"),
        }
        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

    def classify_and_store(self, file_path: str):
        ext = file_path.lower().split('.')[-1]

        if ext in ["txt", "md"]:
            target = self.paths["text"]
        elif ext in ["mp3", "wav", "ogg", "m4a"]:
            target = self.paths["audio"]
        elif ext in ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]:
            target = self.paths["img"]
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        filename = os.path.basename(file_path)
        dest_path = os.path.join(target, filename)
        shutil.move(file_path, dest_path)
        print(f"📂 {filename} → {target}")
        return dest_path
