"""
📂 Watcher Script for File-Based Interactions

Usage:
1. Run this script with `python watch_to_process.py`
2. Drop any `.txt`, `.jpg`, or `.mp3` file into the `to_process/` folder
3. The script will automatically detect the file, classify it using `InputClassifier`,
   and move it into the appropriate subfolder inside `interactions/`:
     - text → interactions/text/
     - audio → interactions/audio/
     - img → interactions/img/

Dependencies:
- Requires `watchdog` library (`pip install watchdog`)
- Logs are saved to `logs/watcher.log`
"""

import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from automation_research_ai_project.input_files.FileInputClassifier import FileInputClassifier

# === 🔧 Logging Configuration ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/watcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# TODO: 🔁 Implement log rotation using logging.handlers.RotatingFileHandler
# TODO: 🧾 Optionally separate error logs into logs/watcher_errors.log
# TODO: 📧 Send email/Slack/notification if a critical error is logged

WATCH_DIR = os.getenv("WATCH_DIR", "to_process")

class InputFolderWatcher(FileSystemEventHandler):
    def __init__(self, classifier: FileInputClassifier):
        self.classifier = classifier

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        logging.info(f"📥 New file detected: {file_path}")

        # Wait briefly to ensure file is fully written
        time.sleep(1)

        try:
            result_path = self.classifier.classify_and_store(file_path)
            logging.info(f"✅ File moved to: {result_path}")
        except Exception as e:
            logging.error(f"❌ Error processing file {file_path}: {e}")
            # TODO: Trigger email/Slack alert here if severity is high

if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)
    classifier = FileInputClassifier()
    event_handler = InputFolderWatcher(classifier)

    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()

    logging.info("👀 Watcher started. Monitoring 'to_process/' for new files.")
    print("👀 Watching 'to_process/' for new files. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("🛑 Watcher manually stopped.")
        print("\n🛑 Watcher stopped.")
    observer.join()
