import os

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        
        if cmd == "dir":
            self.list_directory()
        elif cmd == "cd" and len(parts) > 1:
            self.change_directory(" ".join(parts[1:]))
        elif cmd == "pwd":
            print(self.current_path)
        else:
            print("Unknown command. Type 'help' for available commands")

    def list_directory(self):
        try:
            items = os.listdir(self.current_path)
            for item in items:
                full_path = os.path.join(self.current_path, item)
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                print(f"{item_type:<6} {item}")
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