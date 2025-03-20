import os
import shutil
import datetime
from utils import format_size, color_text, COLOR

class FileManager:
    def __init__(self, config):
        self.current_path = os.getcwd()
        self.config = config

    def execute_command(self, command):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        
        if cmd == "dir":
            self.list_directory(parts[1] if len(parts) > 1 else "")
        elif cmd == "cd" and len(parts) > 1:
            self.change_directory(parts[1])
        elif cmd == "pwd":
            print(self.current_path)
        elif cmd == "info" and len(parts) > 1:
            self.show_info(parts[1])
        elif cmd == "copy" and len(parts) > 1:
            self.copy_item(parts[1])
        elif cmd == "del" and len(parts) > 1:
            self.delete_file(parts[1])
        elif cmd == "delmany" and len(parts) > 1:
            self.delete_multiple(parts[1])
        elif cmd == "mkdir" and len(parts) > 1:
            self.make_directory(parts[1])
        elif cmd == "rename" and len(parts) > 1:
            self.rename_item(parts[1])
        elif cmd == "search" and len(parts) > 1:
            self.search_files(parts[1])
        elif cmd == "clear":
            from utils import clear_screen
            clear_screen()
        else:
            print("Unknown command. Type 'help' for available commands")

    def list_directory(self, args):
        try:
            sort_key = None
            if args.startswith("sort:"):
                sort_type = args.split("sort:")[1].lower()
                sort_key = "size" if sort_type == "size" else "name" if sort_type == "name" else None

            items = os.listdir(self.current_path)
            if not items:
                print("Directory is empty")
                return
                
            print(f"\nDirectory: {self.current_path}")
            headers = f"{'Type':<6} {'Size':>10} {'Modified':>20} {'Name'}"
            print(color_text(headers, COLOR.CYAN) if self.config['use_colors'] else headers)
            print(color_text("-" * 60, COLOR.GRAY) if self.config['use_colors'] else "-" * 60)
            
            item_list = []
            for item in items:
                full_path = os.path.join(self.current_path, item)
                stats = os.stat(full_path)
                item_list.append((item, full_path, stats))

            if sort_key == "size":
                item_list.sort(key=lambda x: x[2].st_size, reverse=True)
            elif sort_key == "name":
                item_list.sort(key=lambda x: x[0].lower())

            for item, full_path, stats in item_list:
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                color = COLOR.BLUE if item_type == "DIR" else COLOR.GREEN
                size = format_size(stats.st_size)
                mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                line = f"{item_type:<6} {size:>10} {mod_time:>20} {item}"
                print(color_text(line, color) if self.config['use_colors'] else line)
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
            color = COLOR.YELLOW if self.config['use_colors'] else None
            
            print(f"\nInfo for: {color_text(name, color) if color else name}")
            print(f"Type: {item_type}")
            print(f"Size: {format_size(stats.st_size)}")
            print(f"Created: {datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Modified: {datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Path: {full_path}")
        except Exception as e:
            print(f"Error getting info: {str(e)}")

    def copy_item(self, args):
        try:
            src, dst = args.split(maxsplit=1)
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            if os.path.exists(src_path):
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    print(f"Copied directory {src} to {dst}")
                else:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied file {src} to {dst}")
            else:
                print("Source item not found")
        except Exception as e:
            print(f"Error copying item: {str(e)}")

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

    def delete_multiple(self, args):
        try:
            names = args.split()
            deleted = 0
            for name in names:
                full_path = os.path.join(self.current_path, name)
                if os.path.exists(full_path) and not os.path.isdir(full_path):
                    os.remove(full_path)
                    print(f"Deleted {name}")
                    deleted += 1
                else:
                    print(f"Skipped {name} - not found or is a directory")
            print(f"Deleted {deleted} file(s)")
        except Exception as e:
            print(f"Error deleting files: {str(e)}")

    def make_directory(self, name):
        try:
            full_path = os.path.join(self.current_path, name)
            if not os.path.exists(full_path):
                os.mkdir(full_path)
                print(f"Created directory: {name}")
            else:
                print("Directory already exists")
        except Exception as e:
            print(f"Error creating directory: {str(e)}")

    def rename_item(self, args):
        try:
            old_name, new_name = args.split(maxsplit=1)
            old_path = os.path.join(self.current_path, old_name)
            new_path = os.path.join(self.current_path, new_name)
            if os.path.exists(old_path):
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed {old_name} to {new_name}")
                else:
                    print("Destination name already exists")
            else:
                print("Source item not found")
        except Exception as e:
            print(f"Error renaming: {str(e)}")

    def search_files(self, args):
        try:
            parts = args.split()
            term = parts[0]
            recursive = "-r" in parts[1:] if len(parts) > 1 else False
            
            print(f"\nSearching for '{term}' {'recursively' if recursive else 'in current directory'}...")
            found = False
            
            if recursive:
                for root, dirs, files in os.walk(self.current_path):
                    for item in dirs + files:
                        if term.lower() in item.lower():
                            full_path = os.path.join(root, item)
                            item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                            rel_path = os.path.relpath(full_path, self.current_path)
                            print(f"{item_type:<6} {rel_path}")
                            found = True
            else:
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