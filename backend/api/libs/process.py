import subprocess
import json

def start_work_manager(model, chat_id, message_id, prompt, params):
    # Prepare parameters as JSON string
    process_params = {
        "model": model,
        "chat_id": chat_id, 
        "message_id": message_id,
        "prompt": prompt,
        "params": params
    }
    
    # Convert to JSON string
    json_params = json.dumps(process_params)
    
    # Start the process with JSON input
    process = subprocess.Popen(
        ["python3", "workmanager.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send JSON to process stdin
    stdout, stderr = process.communicate(input=json_params)
    
    return process.pid, stdout, stderr

