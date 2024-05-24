import subprocess
import select
import json


def run_rfid_script():
    try:
        # Start rfid_with_check.py as a separate process
        process = subprocess.Popen(["python3", "-u", "rfid_with_check.py"], stdout=subprocess.PIPE, text=True)

        # Use a while loop to continuously read and print the output
        while True:
            # Use select to wait for data to become available or for the process to end
            reads = [process.stdout.fileno()]
            ret = select.select(reads, [], [])

            for fd in ret[0]:
                if fd == process.stdout.fileno():
                    line = process.stdout.readline()
                    if line == '' and process.poll() is not None:
                        break
                    if line != '':
                        print(line.strip())

        if process.returncode == 0:
            # If the return code is 0, a valid user has badged in
            print("Valid user detected.")
            return True
        else:
            # Print a message if no valid user was detected
            print("No valid user detected.")
            return False
    except subprocess.CalledProcessError as e:
        # Handle errors that occur during the subprocess call
        print(f"Error occurred: {e}")
        return False

# Function to run the gate opening script
def open_gate():
    try:
        # Run open_gate.py
        subprocess.run(["python3", "open_gate.py"], check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors that occur during the subprocess call
        print(f"Error occurred while opening gate: {e}")

if __name__ == "__main__":
    # Run the RFID script and check if a valid user was detected
    user_info = run_rfid_script()
    if user_info:
        # Print the valid user's name
        print(f"Valid user detected: {user_info['name']}")
        # Run the gate opening script
        open_gate()

