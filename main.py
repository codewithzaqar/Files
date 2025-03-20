import sys
from file_manager import FileManager

def main():
    print("Welcome to Files v0.04")
    print("Type 'help' for commands")

    file_manager = FileManager()

    while True:
        try:
            command = input("FE> ").strip()
            if command.lower() == "exit":
                print("Goodbye!")
                break
            elif command.lower() == "help":
                show_help()
            else:
                file_manager.execute_command(command)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {str(e)}")

def show_help():
    print("""
    Available commands:
    dir [sort:size|name] - List directory contents (optional sorting)
    cd <path>     - Change directory
    pwd           - Show current path
    info <name>   - Show file/directory info
    copy <src> <dst> - Copy file
    del <name>    - Delete file
    mkdir <name>  - Create directory
    search <term> [-r] - Search for files (optional -r for recursive)
    clear         - Clear the screen
    exit          - Quit the program
    """)

if __name__ == "__main__":
    main()