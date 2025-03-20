import sys
from file_manager import FileManager

def main():
    print("Welcome to Files v0.02")
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
    dir           - List directory contents with details
    cd <path>     - Change directory
    pwd           - Show current path
    info <name>   - Show file/directory info
    clear         - Clear the screen
    exit          - Quit the program
    """)

if __name__ == "__main__":
    main()