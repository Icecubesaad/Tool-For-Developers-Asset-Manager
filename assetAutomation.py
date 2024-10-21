from shutil import move
import os
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import pyperclip
from tkinter import Tk, filedialog

# files path
source_dir = str(Path.home() / "Downloads")
global CURRENT_DIR
# File types
image_extensions = [
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".png",
    ".gif",
    ".webp",
    ".tiff",
    ".tif",
    ".psd",
    ".raw",
    ".arw",
    ".cr2",
    ".nrw",
    ".k25",
    ".bmp",
    ".dib",
    ".heif",
    ".heic",
    ".ind",
    ".indd",
    ".indt",
    ".jp2",
    ".j2k",
    ".jpf",
    ".jpf",
    ".jpx",
    ".jpm",
    ".mj2",
    ".svg",
    ".svgz",
    ".ai",
    ".eps",
    ".ico",
]
# ? supported Video types
video_extensions = [
    ".webm",
    ".mpg",
    ".mp2",
    ".mpeg",
    ".mpe",
    ".mpv",
    ".ogg",
    ".mp4",
    ".mp4v",
    ".m4v",
    ".avi",
    ".wmv",
    ".mov",
    ".qt",
    ".flv",
    ".swf",
    ".avchd",
]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [
    ".doc",
    ".docx",
    ".odt",
    ".pdf",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
]

def get_project_directory():
    root = Tk()
    root.withdraw()  # Hide the unnecessary root window
    project_dir = filedialog.askdirectory(title="Select the project directory")
    if project_dir:
        print(f"Selected project directory: {project_dir}")
        return project_dir
    else:
        print("No directory selected. Exiting.")
        exit()

def set_path_for_framework(choice: int):
    global dest_dir_image, dest_dir_audio, dest_dir_video, dest_dir_documents
    is_in_root = False
    global storing_dir
    if choice == 1 or choice == 2 or choice == 5:
        storing_dir = "public"
    elif choice == 3:
        storing_dir = "src/assets"
    elif choice == 4:
        storing_dir = "static"
    # Define folder map for different frameworks
    folder_map = {
        1: f"{storing_dir}",
        2: f"client/{storing_dir}",  # Client
        3: f"frontend/{storing_dir}",  # Frontend
        4: f"website/{storing_dir}",  # Website
    }
    for key, path in folder_map.items():
            print(path)
            framework_dir = os.path.join(CURRENT_DIR,path)
            print(framework_dir)
            if os.path.isdir(framework_dir):
                print("Found the directory")
                is_in_root = True
                dest_dir_image = os.path.join(framework_dir, "images")
                dest_dir_audio = os.path.join(framework_dir, "audios")
                dest_dir_video = os.path.join(framework_dir, "videos")
                dest_dir_documents = os.path.join(framework_dir, "documents")
                break
            else:
                continue
    if not is_in_root:
        print("Cannot find the working directory. Try to select the root of your project")


def is_file_in_use(file_path):
    try:
        with open(file_path, "rb") as f:
            f.seek(0, os.SEEK_END)  
            return False  
    except IOError:
        return True


def move_file(dest, entry, name):
    if not os.path.exists(dest):
        os.makedirs(dest)
        logging.info(f"Created destination directory: {dest}")

    while is_file_in_use(entry):
        logging.info(f"Waiting for file {name} to finish downloading...")
        time.sleep(1)  

    unique_name = make_unique(dest, name)
    
    logging.info(f"Moving file {name} to {dest}")
    try:
        move(entry, os.path.join(dest, unique_name))
    except Exception as e:
        logging.error(f"Error moving file {name}: {e}")
    path_to_copy = ""
    if user_choice == 1 or user_choice == 2:
        path_to_copy = f"images/{unique_name}"
    elif user_choice == 3:
        path_to_copy = f"assets/images/{unique_name}"
    elif user_choice == 4:
        path_to_copy = '{% static "images/' + unique_name + '" %}'
    pyperclip.copy(path_to_copy)


def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return 
        entry = event.src_path
        name = os.path.basename(entry)
        if entry and os.path.isfile(entry):
            self.check_image_files(entry, name)
            self.check_audio_files(entry, name)
            self.check_video_files(entry, name)
            self.check_document_files(entry, name)

    def check_image_files(self, entry, name):
        if any(name.endswith(ext) for ext in image_extensions):
            move_file(dest_dir_image, entry, name)

    def check_audio_files(self, entry, name):
        if any(name.endswith(ext) for ext in audio_extensions):
            move_file(dest_dir_audio, entry, name)

    def check_video_files(self, entry, name):
        if any(name.endswith(ext) for ext in video_extensions):
            move_file(dest_dir_video, entry, name)

    def check_document_files(self, entry, name):
        if any(name.endswith(ext) for ext in document_extensions):
            move_file(dest_dir_documents, entry, name)


# Main script execution
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    print("Select your project directory\n")
    CURRENT_DIR = get_project_directory()
    print("Choose a framework you are working on right now\n")
    print(
        "press 1 for React.js\npress 2 for Next.js\npress 3 for Angular.js\npress 4 for Django\npress 5 for Laravel\npress 6 for exit"
    )
    user_choice_raw = input("Enter your choice: ")
    user_choice = int(user_choice_raw)
    if user_choice == 6:
        print("Terminating the process")
        exit()
    set_path_for_framework(user_choice)
    # Observe the source directory for new files being added
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()

    try:
        logging.info("Waiting for new files to be added...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
