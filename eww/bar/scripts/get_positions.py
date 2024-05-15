import subprocess
import argparse


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract resolution details.")
    parser.add_argument('--width', action='store_true', help="Extract the width of the resolution")
    parser.add_argument('--height', action='store_true', help="Extract the height of the resolution")
    parser.add_argument('--full', action='store_true', help="Extract the full resolution")

    args = parser.parse_args()


    # Define the shell command with properly escaped backslashes
    command = "hyprctl monitors | grep -oP '\\d+x\\d+(?=@)' | head -n 1"
    # Execute the command using subprocess.Popen
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    output = stdout.strip()
    x_res = output.split('x')[0]
    y_res = output.split('x')[-1]
    # Print the output of the command
    print(output)

    print(x_res, y_res)

    # Get the first resolution
    resolution = get_resolution(output)

    if args.width:
        print("function here")
    elif args.height:
        print("function here")
    elif args.full:
        print("function here")
    else:
        print("Please provide a valid flag: --width, --height, or --full")

if __name__ == "__main__":
    main()
