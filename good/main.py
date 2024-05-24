import subprocess
import select
import json

def run_rfid_script():
    try:
        while True:
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
                            # Check if the output is a JSON string (indicating a successful enter scan)
                            try:
                                json.loads(line)
                                subprocess.run(["python3", "open_gate.py"])
                            except json.JSONDecodeError:
                                # Check if the output is a string saying the user has left (indicating a successful leave scan)
                                if "has left" in line:
                                    subprocess.run(["python3", "open_gate.py"])

                if process.poll() is not None:  # process has ended
                    break  # Break the inner loop to restart the script

    except subprocess.CalledProcessError as e:
        # Handle errors that occur during the subprocess call
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Run the RFID script
    run_rfid_script()