import os
import shutil
import datetime
from utils import format_size, color_text, COLOR

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
        elif cmd == "copy" and len(parts) > 1:
            self.copy_file(parts[1])
        elif cmd == "del" and len(parts) > 1:
            self.delete_file(parts[1])
        elif cmd == "search" and len(parts) > 1:
            self.search_files(parts[1])
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
            print(f"{color_text('Type', COLOR.CYAN):<6} {color_text('Size', COLOR.CYAN):>10} {color_text('Modified', COLOR.CYAN):>20} {color_text('Name', COLOR.CYAN)}")
            print(color_text("-" * 60, COLOR.GRAY))
            
            for item in items:
                full_path = os.path.join(self.current_path, item)
                stats = os.stat(full_path)
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                color = COLOR.BLUE if item_type == "DIR" else COLOR.GREEN
                size = format_size(stats.st_size)
                mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                print(f"{color_text(item_type, color):<6} {size:>10} {mod_time:>20} {color_text(item, color)}")
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
            
            print(f"\nInfo for: {color_text(name, COLOR.YELLOW)}")
            print(f"Type: {item_type}")
            print(f"Size: {format_size(stats.st_size)}")
            print(f"Created: {datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Modified: {datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Path: {full_path}")
        except Exception as e:
            print(f"Error getting info: {str(e)}")

    def copy_file(self, args):
        try:
            src, dst = args.split(maxsplit=1)
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"Copied {src} to {dst}")
            else:
                print("Source file not found")
        except Exception as e:
            print(f"Error copying file: {str(e)}")

    def delete_file(self, name):
        try:
            full_path = os.path.join(self.current_path, name)
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    print("Cannot delete directories with 'del' command")
                else:
                    os.remove(full_path)
                    print(f"Deleted {name}")
            else:
                print("File not found")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")

    def search_files(self, term):
        try:
            print(f"\nSearching for '{term}'...")
            found = False
            for item in os.listdir(self.current_path):
                if term.lower() in item.lower():
                    full_path = os.path.join(self.current_path, item)
                    item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                    print(f"{item_type:<6} {item}")
                    found = True
            if not found:
                print("No matches found")
        except Exception as e:
            print(f"Error searching: {str(e)}")