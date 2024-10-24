import sys
from parser import parse

def main():
    if len(sys.argv) != 2:
        print("Usage: python app.py <path_to_json_file>")
        sys.exit(1)  

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r') as file:
            json_content = file.read().strip()
        
        parse(json_content)
        print("Valid JSON")
        sys.exit(0)  

    except FileNotFoundError:
        print("Error: The file does not exist.")
        sys.exit(1)  
    except ValueError as e:
        print("Invalid JSON:", e)
        sys.exit(1) 
    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)  

if __name__ == "__main__":
    main()