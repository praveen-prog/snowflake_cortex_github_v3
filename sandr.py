import subprocess
import time

def launch_application():
    return subprocess.Popen(["streamlit", "run", "app.py"])

def application_start_and_stop():
    try:
        print("Stopping application...")
        process = launch_application()
        process.terminate()
        process.wait()
        print("Stopped application. Restarting...")
        time.sleep(5)
        process = launch_application()
        print("Application restarted successfully!")
    except Exception as e:
        print("Error, please check:", e)

application_start_and_stop()
