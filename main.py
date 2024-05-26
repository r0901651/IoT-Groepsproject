import subprocess
import select
import json

def run_rfid_script():
    loadcell_process = None  # Keep track of the loadcell.py process

    try:
        while True:
            # Start the RFID script subprocess
            process = subprocess.Popen(["python3", "-u", "rfid_with_check.py"], stdout=subprocess.PIPE, text=True)

            # Use a while loop to continuously read and print the output
            while True:
                # Use select to wait for data to become available or for the process to end
                reads = [process.stdout.fileno()]
                ret = select.select(reads, [], [])

                for fd in ret[0]:
                    if fd == process.stdout.fileno():
                        # Read a line from the subprocess stdout
                        line = process.stdout.readline()
                        # Check if the subprocess has ended and no more output is available
                        if line == '' and process.poll() is not None:
                            break
                        # Process the output line if it's not empty
                        if line != '':
                            print(line.strip())
                            # Check if the output is a JSON string (indicating a successful enter scan)
                            try:
                                json.loads(line)
                                # Execute open-close_gate.py subprocess if JSON is successfully loaded
                                subprocess.run(["python3", "open-close_gate.py"])
                                # Start loadcell.py subprocess after the gate has opened
                                loadcell_process = subprocess.Popen(["python3", "loadcell.py"])
                            except json.JSONDecodeError:
                                # Check if the output is a string indicating the user has left (indicating a successful leave scan)
                                if "has left" in line:
                                    # Execute open-close_gate.py subprocess
                                    subprocess.run(["python3", "open-close_gate.py"])
                                    if loadcell_process is not None:  # If loadcell.py is running
                                        # Terminate loadcell.py subprocess
                                        loadcell_process.terminate()
                                        loadcell_process = None  # Reset the loadcell_process variable

                # Check if the RFID script subprocess has ended
                if process.poll() is not None:
                    break  # Break the inner loop to restart the RFID script

    except subprocess.CalledProcessError as e:
        # Handle errors that occur during the subprocess call
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Run the RFID script
    run_rfid_script()
