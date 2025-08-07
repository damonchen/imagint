import time
import requests
import logging
import subprocess
import os

TASK_TYPE = "qwen"  # 指定任务类型
API_BASE_URL = "http://localhost:5050"  # 根据实际服务器地址调整
API_KEY = "1234567890"

logger = logging.getLogger(__name__)

while True:
    try:
        # 获取任务
        response = requests.post(
            f"{API_BASE_URL}/api/v1/task",
            json={"task_type": TASK_TYPE, "media_type": "image"},
            headers={"Content-Type": "application/json", "X-API-KEY": API_KEY},
        )

        if response.status_code == 200:
            task_data = response.json()
            print("debug task data", task_data)

            if task_data:
                task_id = task_data.get("task_id")
            else:
                task_id = None

            if task_id is not None:
                logger.info(f"get new task {task_id}")
                prompt = task_data.get("prompt", "")
                params = task_data.get("params", {})

                # 从params中获取参数
                ratio = params.get("ratio", "16:9")
                batch_size = params.get("batch_size", 4)
                seed = params.get("seed")

                # 执行任务
                process = None
                try:
                    cmd = (
                        [
                            "modal",
                            "run",
                            "qwen.py",
                            "--prompt",
                            prompt,
                            "--ratio",
                            ratio,
                            "--batch_size",
                            str(batch_size),
                        ],
                    )
                    if seed:
                        cmd.extend(["--seed", str(seed)])

                    # Run subprocess with 10 second timeout
                    process = subprocess.run(
                        cmd,
                        capture_output=True,
                        timeout=10,
                        text=True,
                        check=True,
                    )
                except subprocess.TimeoutExpired:
                    print("Process timed out after 10 seconds")
                    # raise
                except subprocess.CalledProcessError as e:
                    print(f"Process failed with return code {e.returncode}")
                    print(f"Error output: {e.stderr}")
                    # raise
                except Exception as e:
                    print(f"Failed to run subprocess: {str(e)}")
                    # raise

                if process is not None:
                    file_paths = process.stdout.split("\n")

                    # 通知任务完成
                    requests.post(
                        f"{API_BASE_URL}/api/v1/task/complete",
                        json={
                            "task_id": task_id,
                            "status": "completed",
                            "result": {"images": file_paths, "media_type": "image"},
                        },
                        headers={
                            "Content-Type": "application/json",
                            "X-API-KEY": API_KEY,
                        },
                    )

        # 等待1秒后继续
        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(1)
        continue
