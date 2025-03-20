import sys
from file_manager import FileManager

def main():
    print("Welcome to Files v0.01")
    print("Type 'help' for commands")

    file_manager = FileManager()

    while True:
        try:
            command = input("FE> ").strip().lower()
            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
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
    dir - List current directory contents
    cd <path> - Change directory
    pwd - Show current path
    exit - Quit the program
    """)

if __name__ == "__main__":
    main()