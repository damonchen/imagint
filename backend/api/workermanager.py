import time
import requests
import logging
import subprocess
import os
import json

TASK_TYPE = "qwen-image"  # 指定任务类型
API_BASE_URL = "http://localhost:5050"  # 根据实际服务器地址调整
API_KEY = "1234567890"
MODAL_PATH = "/mnt/f/dev/Imagint/src/backend/.venv/bin/python"

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
                stdout_output = None
                stderr_output = None
                try:
                    # Run subprocess with 10 second timeout
                    process = subprocess.Popen(
                        [MODAL_PATH, "workers/qwen.py"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    data = json.dumps(
                        {
                            "prompt": prompt,
                            "params": params,
                            "ratio": ratio,
                            "batch_size": batch_size,
                            "seed": seed,
                        }
                    )
                    print(data)

                    stdout_output, stderr_output = process.communicate(
                        input=data, timeout=600
                    )

                    if stdout_output:
                        print(stdout_output.strip())
                        # 解析输出
                        if "images" in stdout_output:
                            # 提取图片路径
                            images = stdout_output.split("images: ")[1].strip()
                            images = json.loads(images)
                            file_paths.extend(images)

                except subprocess.TimeoutExpired:
                    print("Process timed out after 600 seconds")
                    # raise
                except subprocess.CalledProcessError as e:
                    print(f"Process failed with return code {e.returncode}")
                    print(f"Error output: {e.stderr}")
                    # raise
                except Exception as e:
                    print(f"Failed to run subprocess: {str(e)}")
                    # raise

                if stdout_output is not None:
                    file_paths = stdout_output.split("\n")

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
        else:
            print("get task may occur error", response.status_code)
        # 等待1秒后继续
        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(1)
        continue
