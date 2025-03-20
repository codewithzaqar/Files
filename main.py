import sys
from file_manager import FileManager
from config import load_config

def main():
    config = load_config()
    print(f"Welcome to Files v0.09 (Colors: {'on' if config['use_colors'] else 'off'})")
    print("Type 'help' for commands")
    
    file_manager = FileManager(config)
    command_history = []
    aliases = config.get('aliases', {})
    
    while True:
        try:
            command = input("F> ").strip()
            if command:
                if command.endswith('??'):
                    base_cmd = command[:-2].strip()
                    suggestions = file_manager.get_command_suggestions(base_cmd)
                    if suggestions:
                        print("Suggestions:", ", ".join(suggestions))
                    continue
                
                command_history.append(command)
                if len(command_history) > config.get('history_size', 10):
                    command_history.pop(0)
                command = aliases.get(command, command)
            
            if command.lower() == "exit":
                print("Goodbye!")
                break
            elif command.lower() == "help":
                show_help()
            elif command.lower() == "history":
                print("\nCommand History:")
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}. {cmd}")
            else:
                file_manager.execute_command(command)
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
    del <name>    - Delete file
    delmany <name1> <name2> ... - Delete multiple files
    mkdir <name>  - Create directory
    rename <old> <new> - Rename file/directory
    search <term> [-r] - Search for files (optional -r for recursive)
    clear         - Clear the screen
    history       - Show command history
    exit          - Quit the program
    
    Tip: Type '<command>??' for suggestions (simulated tab completion)
    """)

if __name__ == "__main__":
    main()