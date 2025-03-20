import os
import datetime
from utils import format_size

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()

    def execute_command(self, command):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        
        if cmd == "dir":
            self.list_directory()
        elif cmd == "cd" and len(parts) > 1:
            self.change_directory(parts[1])
        elif cmd == "pwd":
            print(self.current_path)
        elif cmd == "info" and len(parts) > 1:
            self.show_info(parts[1])
        elif cmd == "clear":
            from utils import clear_screen
            clear_screen()
        else:
            print("Unknown command. Type 'help' for available commands")

    def list_directory(self):
        try:
            items = os.listdir(self.current_path)
            if not items:
                print("Directory is empty")
                return
                
            print(f"\nDirectory: {self.current_path}")
            print(f"{'Type':<6} {'Size':>10} {'Modified':>20} {'Name'}")
            print("-" * 60)
            
            for item in items:
                full_path = os.path.join(self.current_path, item)
                stats = os.stat(full_path)
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                size = format_size(stats.st_size)
                mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                print(f"{item_type:<6} {size:>10} {mod_time:>20} {item}")
            print(f"\n{len(items)} item(s)")
        except Exception as e:
            print(f"Error listing directory: {str(e)}")

    def change_directory(self, path):
        try:
            if path == "..":
                new_path = os.path.dirname(self.current_path)
            else:
                new_path = os.path.abspath(os.path.join(self.current_path, path))
            
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_path = new_path
                print(f"Changed to: {self.current_path}")
            else:
                print("Invalid directory")
        except Exception as e:
            print(f"Error changing directory: {str(e)}")

    def show_info(self, name):
        try:
            full_path = os.path.join(self.current_path, name)
            if not os.path.exists(full_path):
                print("Item not found")
                return
                
            stats = os.stat(full_path)
            item_type = "Directory" if os.path.isdir(full_path) else "File"
            
            print(f"\nInfo for: {name}")
            print(f"Type: {item_type}")
            print(f"Size: {format_size(stats.st_size)}")
            print(f"Created: {datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Modified: {datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Path: {full_path}")
        except Exception as e:
            print(f"Error getting info: {str(e)}")