import os
import shutil
import datetime
import time
import stat
from utils import format_size, color_text, COLOR, show_progress

class FileManager:
    def __init__(self, config):
        self.current_path = os.getcwd()
        self.config = config
        self.commands = [
            "dir", "cd", "pwd", "info", "copy", "move", "del", "delmany",
            "mkdir", "rename", "search", "clear", "history", "exit"
        ]

    def execute_command(self, command, piped_input=None):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        
        try:
            if cmd == "dir":
                return self.list_directory(parts[1] if len(parts) > 1 else "", piped_input)
            elif cmd == "cd" and len(parts) > 1:
                self.change_directory(parts[1])
            elif cmd == "pwd":
                print(self.current_path)
                return self.current_path
            elif cmd == "info" and len(parts) > 1:
                self.show_info(parts[1])
            elif cmd == "copy" and len(parts) > 1:
                self.copy_item(parts[1])
            elif cmd == "move" and len(parts) > 1:
                self.move_item(parts[1])
            elif cmd == "del" and len(parts) > 1:
                self.delete_item(parts[1])
            elif cmd == "delmany" and len(parts) > 1:
                self.delete_multiple(parts[1])
            elif cmd == "mkdir" and len(parts) > 1:
                self.make_directory(parts[1])
            elif cmd == "rename" and len(parts) > 1:
                self.rename_item(parts[1])
            elif cmd == "search" and len(parts) > 1:
                return self.search_files(parts[1], piped_input)
            elif cmd == "clear":
                from utils import clear_screen
                clear_screen()
            else:
                print("Unknown command. Type 'help' for available commands")
        except PermissionError:
            print("Permission denied. Try running with elevated privileges.")
        except FileNotFoundError:
            print("File or directory not found.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        return None

    def get_command_suggestions(self, partial):
        return [cmd for cmd in self.commands if cmd.startswith(partial.lower())]

    def get_dir_size(self, path):
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                total += os.path.getsize(os.path.join(dirpath, filename))
        return total

    def get_permissions(self, path):
        st = os.stat(path)
        mode = st.st_mode
        perms = ''
        perms += 'r' if mode & stat.S_IRUSR else '-'
        perms += 'w' if mode & stat.S_IWUSR else '-'
        perms += 'x' if mode & stat.S_IXUSR else '-'
        perms += 'r' if mode & stat.S_IRGRP else '-'
        perms += 'w' if mode & stat.S_IWGRP else '-'
        perms += 'x' if mode & stat.S_IXGRP else '-'
        perms += 'r' if mode & stat.S_IROTH else '-'
        perms += 'w' if mode & stat.S_IWOTH else '-'
        perms += 'x' if mode & stat.S_IXOTH else '-'
        return perms

    def list_directory(self, args, piped_input=None):
        sort_key = None
        type_filter = None
        args_parts = args.split()
        for arg in args_parts:
            if arg.startswith("sort:"):
                sort_type = arg.split("sort:")[1].lower()
                sort_key = "size" if sort_type == "size" else "name" if sort_type == "name" else None
            elif arg.startswith("type:"):
                type_filter = arg.split("type:")[1].lower()
                if type_filter not in ["file", "dir"]:
                    print("Invalid type filter. Use 'file' or 'dir'.")
                    return

        items = os.listdir(self.current_path) if not piped_input else piped_input.splitlines()
        if not items:
            print("Directory is empty")
            return
            
        print(f"\nDirectory: {self.current_path}")
        headers = f"{'Type':<6} {'Size':>10} {'Modified':>20} {'Perms':<10} {'Name'}"
        print(color_text(headers, COLOR.CYAN) if self.config['use_colors'] else headers)
        print(color_text("-" * 70, COLOR.GRAY) if self.config['use_colors'] else "-" * 70)
        
        item_list = []
        for item in items:
            item = item.strip().split()[-1] if piped_input else item  # Extract name from piped input
            full_path = os.path.join(self.current_path, item)
            if not os.path.exists(full_path):
                continue
            stats = os.stat(full_path)
            item_type = "DIR" if os.path.isdir(full_path) else "FILE"
            if type_filter and item_type.lower() != type_filter:
                continue
            size = self.get_dir_size(full_path) if item_type == "DIR" else stats.st_size
            item_list.append((item, full_path, stats, size))

        if sort_key == "size":
            item_list.sort(key=lambda x: x[3], reverse=True)
        elif sort_key == "name":
            item_list.sort(key=lambda x: x[0].lower())

        output = []
        for item, full_path, stats, size in item_list:
            item_type = "DIR" if os.path.isdir(full_path) else "FILE"
            color = COLOR.BLUE if item_type == "DIR" else COLOR.GREEN
            size_str = format_size(size)
            mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            perms = self.get_permissions(full_path)
            line = f"{item_type:<6} {size_str:>10} {mod_time:>20} {perms:<10} {item}"
            print(color_text(line, color) if self.config['use_colors'] else line)
            output.append(line)
        print(f"\n{len(item_list)} item(s)")
        return '\n'.join(output) if output else None

    def change_directory(self, path):
        if path == "..":
            new_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.abspath(os.path.join(self.current_path, path))
        
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.current_path = new_path
            print(f"Changed to: {self.current_path}")
        else:
            print("Invalid directory")

    def show_info(self, name):
        full_path = os.path.join(self.current_path, name)
        if not os.path.exists(full_path):
            print("Item not found")
            return
            
        stats = os.stat(full_path)
        item_type = "Directory" if os.path.isdir(full_path) else "File"
        size = self.get_dir_size(full_path) if item_type == "Directory" else stats.st_size
        color = COLOR.YELLOW if self.config['use_colors'] else None
        
        print(f"\nInfo for: {color_text(name, color) if color else name}")
        print(f"Type: {item_type}")
        print(f"Size: {format_size(size)}")
        print(f"Permissions: {self.get_permissions(full_path)}")
        print(f"Created: {datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Modified: {datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Path: {full_path}")

    def copy_item(self, args):
        src, dst = args.split(maxsplit=1)
        src_path = os.path.join(self.current_path, src)
        dst_path = os.path.join(self.current_path, dst)
        if not os.path.exists(src_path):
            print("Source item not found")
            return

        print(f"Copying {src} to {dst}...")
        start_time = time.time()
        if os.path.isdir(src_path):
            total_size = self.get_dir_size(src_path)
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True, 
                          copy_function=lambda src, dst: show_progress(src, dst, total_size, start_time))
            print(f"\nCopied directory {src} to {dst}")
        else:
            total_size = os.path.getsize(src_path)
            shutil.copy2(src_path, dst_path)
            show_progress(src_path, dst_path, total_size, start_time, final=True)
            print(f"Copied file {src} to {dst}")

    def move_item(self, args):
        src, dst = args.split(maxsplit=1)
        src_path = os.path.join(self.current_path, src)
        dst_path = os.path.join(self.current_path, dst)
        if not os.path.exists(src_path):
            print("Source item not found")
            return

        print(f"Moving {src} to {dst}...")
        start_time = time.time()
        total_size = self.get_dir_size(src_path) if os.path.isdir(src_path) else os.path.getsize(src_path)
        shutil.move(src_path, dst_path)
        show_progress(src_path, dst_path, total_size, start_time, final=True)
        print(f"Moved {src} to {dst}")

    def delete_item(self, name):
        full_path = os.path.join(self.current_path, name)
        if not os.path.exists(full_path):
            print("Item not found")
            return
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f"Deleted directory {name}")
        else:
            os.remove(full_path)
            print(f"Deleted file {name}")

    def delete_multiple(self, args):
        names = args.split()
        deleted = 0
        for name in names:
            full_path = os.path.join(self.current_path, name)
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    print(f"Deleted directory {name}")
                else:
                    os.remove(full_path)
                    print(f"Deleted file {name}")
                deleted += 1
            else:
                print(f"Skipped {name} - not found")
        print(f"Deleted {deleted} item(s)")

    def make_directory(self, name):
        full_path = os.path.join(self.current_path, name)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
            print(f"Created directory: {name}")
        else:
            print("Directory already exists")

    def rename_item(self, args):
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

    def search_files(self, args, piped_input=None):
        parts = args.split()
        term = parts[0]
        recursive = "-r" in parts[1:] if len(parts) > 1 else False
        content_search = "-c" in parts[1:] if len(parts) > 1 else False
        
        print(f"\nSearching for '{term}' {'recursively' if recursive else 'in current directory'} "
              f"{'in content' if content_search else 'by name'}...")
        found = 0
        output = []
        
        if piped_input:
            items = [(line.split()[-1], os.path.join(self.current_path, line.split()[-1])) 
                     for line in piped_input.splitlines() if os.path.exists(os.path.join(self.current_path, line.split()[-1]))]
        else:
            items = [(item, os.path.join(self.current_path, item)) for item in os.listdir(self.current_path)] if not recursive else None

        if recursive:
            for root, dirs, files in os.walk(self.current_path):
                for item in dirs + files:
                    full_path = os.path.join(root, item)
                    if content_search and os.path.isfile(full_path):
                        try:
                            with open(full_path, 'r', errors='ignore') as f:
                                if term.lower() in f.read().lower():
                                    item_type = "FILE"
                                    rel_path = os.path.relpath(full_path, self.current_path)
                                    print(f"{item_type:<6} {rel_path}")
                                    output.append(f"{item_type:<6} {rel_path}")
                                    found += 1
                        except Exception:
                            continue
                    elif term.lower() in item.lower():
                        item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                        rel_path = os.path.relpath(full_path, self.current_path)
                        print(f"{item_type:<6} {rel_path}")
                        output.append(f"{item_type:<6} {rel_path}")
                        found += 1
        else:
            for item, full_path in items or [(item, os.path.join(self.current_path, item)) for item in os.listdir(self.current_path)]:
                if content_search and os.path.isfile(full_path):
                    try:
                        with open(full_path, 'r', errors='ignore') as f:
                            if term.lower() in f.read().lower():
                                item_type = "FILE"
                                print(f"{item_type:<6} {item}")
                                output.append(f"{item_type:<6} {item}")
                                found += 1
                    except Exception:
                        continue
                elif term.lower() in item.lower():
                    item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                    print(f"{item_type:<6} {item}")
                    output.append(f"{item_type:<6} {item}")
                    found += 1
        
        print(f"Found {found} match(es)" if found else "No matches found")
        return '\n'.join(output) if output else None