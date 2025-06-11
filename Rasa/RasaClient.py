import requests
import subprocess
import os
import time
import sys

class RasaClient:
    def __init__(self, endpoint="http://localhost:5005/webhooks/rest/webhook"):
        self.endpoint = endpoint
        self.rasa_process = None
        self.action_process = None

    def send_message(self, message, sender="user"):
        payload = {
            "sender": sender,
            "message": message
        }
        try:
            print(f"Sending message: {payload}")
            response = requests.post(self.endpoint, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"Server response: {data}")
            return [msg.get("text", "") for msg in data if "text" in msg]
        except requests.RequestException as e:
            print(f"Rasa connection error: {e}")
            return ["Sorry, I couldn't reach the server."]

    def start_rasa_servers(self):
        try:
            # Use the current Python executable
            conda_env_path = r"C:\\Users\TOLGA\anaconda3\AnacondaProjects\envs\installingrasa"
            python_executable = os.path.join(conda_env_path, "python.exe")
            print(f"Using Python path: {python_executable}")

            # Verify Python path
            if not os.path.exists(python_executable):
                raise FileNotFoundError(f"Python executable not found at {python_executable}")

            # Rasa project directory
            rasa_project_dir = r"C:\Users\TOLGA\Desktop\NLP-ChatBot\Rasa"
            if not os.path.exists(rasa_project_dir):
                raise FileNotFoundError(f"Rasa project directory not found at {rasa_project_dir}")

            # Start Rasa server
            rasa_cmd = [python_executable, "-m", "rasa", "run", "--enable-api", "--cors", "*"]
            self.rasa_process = subprocess.Popen(
                rasa_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=rasa_project_dir
            )
            print("Rasa server is starting...")
            time.sleep(15)

            # Start Action server
            action_cmd = [python_executable, "-m", "rasa", "run", "actions", "--port", "5057"]
            self.action_process = subprocess.Popen(
                action_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=rasa_project_dir
            )
            print("Action server is starting...")
            time.sleep(15)

            # Check process status
            try:
                stdout, stderr = self.rasa_process.communicate(timeout=1)
                if stderr:
                    raise RuntimeError(f"Rasa server error: {stderr}")
            except subprocess.TimeoutExpired:
                print("Rasa server is running.")
            try:
                stdout, stderr = self.action_process.communicate(timeout=1)
                if stderr:
                    raise RuntimeError(f"Action server error: {stderr}")
            except subprocess.TimeoutExpired:
                print("Action server is running.")

        except Exception as e:
            print(f"Error starting Rasa server: {str(e)}")
            self.stop_rasa_servers()
            raise

    def stop_rasa_servers(self):
        if self.rasa_process and self.rasa_process.poll() is None:
            self.rasa_process.terminate()
            print("Rasa server stopped.")
        if self.action_process and self.action_process.poll() is None:
            self.action_process.terminate()
            print("Action server stopped.")

    def start_chat(self):
        """Run an interactive chat session with the Rasa bot."""
        print("Start chatting with the bot! Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Ending chat session.")
                break
            responses = self.send_message(user_input)
            for response in responses:
                print(f"Bot: {response}")

if __name__ == "__main__":
    cli = RasaClient()
    try:
        cli.start_rasa_servers()
        cli.start_chat()
    except KeyboardInterrupt:
        print("\nChat interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cli.stop_rasa_servers()

