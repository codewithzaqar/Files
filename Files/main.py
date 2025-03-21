import sys
from .file_manager import FileManager
from .config import load_config

def run():
    config = load_config()
    print("""
        ____________________            
        ___  ____/__(_)__  /____________
        __  /_   __  /__  /_  _ \_  ___/
        _  __/   _  / _  / /  __/(__  ) 
        /_/      /_/  /_/  \___//____/
                                    v0.11
    """)
    print(f"Welcome to Files (Colors: {'on' if config['use_colors'] else 'off'})")
    print("Type 'help' for commands")
    
    file_manager = FileManager(config)
    command_history = []
    aliases = config.get('aliases', {})
    
    while True:
        try:
            command = input("FE> ").strip()
            if command:
                if command.endswith('?'):
                    base_cmd = command[:-1].strip()
                    suggestions = file_manager.get_command_suggestions(base_cmd, include_files=True)
                    if suggestions:
                        print("Suggestions:", ", ".join(suggestions))
                    continue
                
                command_history.append(command)
                if len(command_history) > config.get('history_size', 10):
                    command_history.pop(0)
                
                if '|' in command:
                    commands = [cmd.strip() for cmd in command.split('|')]
                    output = None
                    for cmd in commands:
                        cmd = aliases.get(cmd, cmd)
                        output = file_manager.execute_command(cmd, output)
                    if output:
                        print(output)
                    continue
                
                command = aliases.get(command, command)
                if command.lower().startswith("interactive"):
                    file_manager.interactive_mode(command[11:].strip() if len(command) > 11 else "")
                else:
                    file_manager.execute_command(command)
            
            if command.lower() == "exit":
                print("Goodbye!")
                break
            elif command.lower() == "help":
                show_help()
            elif command.lower() == "history":
                print("\nCommand History:")
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}. {cmd}")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {str(e)}")

def show_help():
    print("""
    Available commands:
    dir [sort:size|name] [type:file|dir] - List contents (with size/permissions)
    cd <path>     - Change directory
    pwd           - Show current path
    info <name>   - Show file/directory info (with permissions)
    copy <src> <dst> - Copy file or directory (with progress)
    move <src> <dst> - Move file or directory (with progress)
    del <name>    - Delete file or directory
    delmany <name1> <name2> ... - Delete multiple files/directories
    mkdir <name>  - Create directory
    rename <old> <new> - Rename file/directory
    search <term> [-r] [-c] - Search files (optional -r recursive, -c content)
    compress <name> <zipname> - Compress file/directory to zip
    decompress <zipname> <dst> - Decompress zip to directory
    clear         - Clear the screen
    history       - Show command history
    interactive [delmany|copy|move] - Interactive batch mode
    exit          - Quit the program
    
    Tip: Type '<command>?' for enhanced suggestions
    Pipe: Use '|' to chain commands (e.g., 'dir | search test')
    """)

if __name__ == "__main__":
    run()