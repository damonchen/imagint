import glob
import time
import requests
import logging
import subprocess
import os
import json
import uuid
import traceback
import shutil

TASK_TYPE = "qwen-image"  # 指定任务类型
API_BASE_URL = "http://localhost:5050"  # 根据实际服务器地址调整
API_KEY = "1234567890"
MODAL_PATH = "/mnt/f/dev/Imagint/src/backend/.venv/bin/python"
TEMP_PATH = "/tmp"

IMAGE_PATH = "/mnt/f/dev/Imagint/src/backend/images"
VIDEO_PATH = "/mnt/f/dev/Imagint/src/backend/videos"

logger = logging.getLogger(__name__)

import sqlite3
from enum import Enum


class TaskStatus(Enum):
    PULLED = "pulled"
    PROCESSING = "processing"
    PROCESSED = "processed"


class TaskDB:
    def __init__(self):
        self.db_path = os.path.join(TEMP_PATH, "tasks.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    task_data TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result TEXT
                )
            """
            )
            conn.commit()

    def add_task(self, task_id: str, task_type: str, task_data: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (task_id, task_type, task_data, status, result) VALUES (?, ?, ?, ?, ?)",
                (task_id, task_type, task_data, TaskStatus.PULLED.value, ""),
            )
            conn.commit()

    def get_tasks(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return [
                {
                    "task_id": row[0],
                    "type": row[1],
                    "task_data": row[2],
                    "status": row[3],
                    "result": row[4],
                }
                for row in rows
            ]

    def get_task(self, task_id: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "task_id": row[0],
                    "task_type": row[1],
                    "task_data": row[2],
                    "status": row[3],
                    "result": row[4],
                }
            return None

    def update_task_status(self, task_id: str, status: TaskStatus, result: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET status = ?, result = ? WHERE task_id = ?",
                (status.value, result, task_id),
            )
            conn.commit()

    def delete_task(self, task_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()


# Initialize global task database
task_db = TaskDB()


class Text2ImageWorker(object):
    media_type = "image"

    def __init__(self, task_id, task_data):
        self.task_id = task_id
        self.task_data = task_data

        # 确保MODAL_PATH存在
        if not os.path.exists(MODAL_PATH):
            raise FileNotFoundError(f"MODAL_PATH {MODAL_PATH} does not exist")

    def run(self):
        logger.info(f"get new task {self.task_id}")

        task_data = self.task_data

        self.prompt = task_data.get("prompt", "")
        self.params = task_data.get("params", {})
        self.model = task_data.get("model", "qwen-image")
        self.type = task_data.get("type", "text2image")

        params = self.params

        # 从params中获取参数
        self.ratio = params.get("ratio", "16:9")
        self.batch_size = params.get("batch_size", 4)
        self.seed = params.get("seed")
        self.timeout = params.get("timeout", 600)

        return self._run()

    def _run(self):
        model_script = {
            "qwen-image": "workers/qwen.py",
        }

        script = model_script.get(self.model)
        if not script:
            raise ValueError(f"Unsupported model: {self.model}")

        # Run subprocess with 10 second timeout
        process = subprocess.Popen(
            [MODAL_PATH, script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        data = json.dumps(
            {
                "prompt": self.prompt,
                "params": self.params,
                "ratio": self.ratio,
                "batch_size": self.batch_size,
                "seed": self.seed,
            }
        )

        try:
            stdout_output, stderr_output = process.communicate(
                input=data, timeout=self.timeout
            )
        except subprocess.TimeoutExpired:
            print(f"Process timed out after {self.timeout} seconds")
            return {
                "status": "timeout",
                "message": f"Process timed out after {self.timeout} seconds",
            }
            # raise
        except subprocess.CalledProcessError as e:
            print(f"Process failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")
            return {
                "status": "error",
                "message": f"Process failed with return code {e.returncode}: {e.stderr}",
            }
        except Exception as e:
            print(f"Failed to run subprocess: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to run subprocess: {str(e)}",
            }
            # raise
        
        if stderr_output:
            print(stderr_output.strip())

        file_paths = []
        if stdout_output:
            print(stdout_output.strip())
            # 解析输出
            # 从stdout的------之后提取
            prefix = "------------------------------"
            start = stdout_output.find(prefix)
            if start != -1:
                stdout_output = stdout_output[start + len(prefix):].strip()

            info = json.loads(stdout_output)
            file_paths = info["images"]

            # if "images" in stdout_output:
            #     # 提取图片路径
            #     images = stdout_output.split("images: ")[1].strip()
            #     images = json.loads(images)
            #     file_paths.extend(images)

        return {
            "status": "success",
            "message": "Images generated successfully",
            "images": file_paths,
            "media_type": self.media_type,
            "task_id": self.task_id,
        }


class Image2ImageWorker(object):
    media_type = "image"

    def __init__(self, task_id, task_data):
        self.task_id = task_id
        self.task_data = task_data

        # 确保MODAL_PATH存在
        if not os.path.exists(MODAL_PATH):
            raise FileNotFoundError(f"MODAL_PATH {MODAL_PATH} does not exist")

    def prepare(self):
        task_data = self.task_data

        self.prompt = task_data.get("prompt", "")
        self.params = task_data.get("params", {})
        self.model = task_data.get("model", "flux1.dev")
        self.type = task_data.get("type", "image2image")

        params = self.params
        # 从params中获取参数
        self.ratio = params.get("ratio", "16:9")
        self.batch_size = params.get("batch_size", 4)
        self.seed = params.get("seed")
        self.timeout = params.get("timeout", 600)

        image_url = task_data.get("image_url")
        if not image_url:
            raise ValueError("image_url is required for image2image tasks")

        response = requests.get(image_url, stream=True)
        # save image to a temporary file
        name = str(uuid.uuid4())
        self.temp_image_path = os.path.join(TEMP_PATH, f"{name}.png")
        with open(self.temp_image_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def run(self):
        logger.info(f"get new task {self.task_id}")
        self.prepare()

        return self._run()

    def _run(self):
        task_data = self.task_data

        model_script = {
            "flux1.dev": "workers/flux.py",
        }

        script = model_script.get(self.model)
        # 处理image2image类型的任务
        process = subprocess.Popen(
            [MODAL_PATH, script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        data = json.dumps(
            {
                "prompt": self.prompt,
                "params": self.params,
                "ratio": self.ratio,
                "batch_size": self.batch_size,
                "seed": self.seed,
                "image_path": self.temp_image_path,  # 使用临时图片路径
            }
        )

        try:
            stdout_output, stderr_output = process.communicate(
                input=data, timeout=self.timeout
            )
        except subprocess.TimeoutExpired:
            print(f"Process timed out after {self.timeout} seconds")
            return {
                "status": "timeout",
                "message": f"Process timed out after {self.timeout} seconds",
            }
            # raise
        except subprocess.CalledProcessError as e:
            print(f"Process failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")
            return {
                "status": "error",
                "message": f"Process failed with return code {e.returncode}: {e.stderr}",
            }
            # raise
        except Exception as e:
            print(f"Failed to run subprocess: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to run subprocess: {str(e)}",
            }
            # raise

        if stderr_output:
            print(stderr_output.strip())

        file_paths = []
        if stdout_output:
            print(stdout_output.strip())
            # 解析输出
            # 从stdout的------之后提取
            prefix = "------------------------------"
            start = stdout_output.index(prefix)
            stdout_output = stdout_output[start + len(prefix):].strip()

            if "images" in stdout_output:
                # 提取图片路径
                images = stdout_output.split("images: ")[1].strip()
                images = json.loads(images)
                file_paths.extend(images)

        return {
            "status": "success",
            "message": "Images generated successfully",
            "images": file_paths,
            "media_type": self.media_type,
            "task_id": self.task_id,
        }


class Image2VideoWorker(object):
    media_type = "video"

    def __init__(self, task_id, task_data):
        self.task_id = task_id
        self.task_data = task_data

    def prepare(self):
        task_data = self.task_data

        self.prompt = task_data.get("prompt", "")
        self.params = task_data.get("params", {})
        self.model = task_data.get("model", "flux.dev")
        self.type = task_data.get("type", "image2image")

        params = self.params
        # 从params中获取参数
        self.ratio = params.get("ratio", "16:9")
        self.batch_size = params.get("batch_size", 4)
        self.seed = params.get("seed")
        self.timeout = params.get("timeout", 600)

        image_url = task_data.get("image_url")
        if not image_url:
            raise ValueError("image_url is required for image2image tasks")

        response = requests.get(image_url, stream=True)
        name = str(uuid.uuid4())
        self.temp_image_path = os.path.join(TEMP_PATH, f"{name}.png")
        with open(self.temp_image_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def run(self):
        logger.info(f"get new task {self.task_id}")
        self.prepare()

        return self._run()

    def _run(self):
        task_data = self.task_data

        model_script = {
            "wan22": "workers/wan22.py",
        }
        script = model_script.get(self.model)

        data = json.dumps(
            {
                "prompt": self.prompt,
                "params": self.params,
                "ratio": self.ratio,
                "batch_size": self.batch_size,
                "seed": self.seed,
                "image_path": self.temp_image_path,  # 使用临时图片路径
            }
        )

        process = subprocess.Popen(
            [MODAL_PATH, script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            stdout_output, stderr_output = process.communicate(
                input=data, timeout=self.timeout
            )
        except subprocess.TimeoutExpired:
            print(f"Process timed out after {self.timeout} seconds")
            return {
                "status": "timeout",
                "message": f"Process timed out after {self.timeout} seconds",
            }
            # raise
        except subprocess.CalledProcessError as e:
            print(f"Process failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")
            # raise
            return {
                "status": "error",
                "message": f"Process failed with return code {e.returncode}: {e.stderr}",
            }
        except Exception as e:
            print(f"Failed to run subprocess: {str(e)}")
            # raise
            return {
                "status": "error",
                "message": f"Failed to run subprocess: {str(e)}",
            }

        if stderr_output:
            print(stderr_output.strip())

        file_paths = []
        if stdout_output:
            print(stdout_output.strip())
            # 解析输出
            # 从stdout的------之后提取
            prefix = "------------------------------"
            start = stdout_output.index(prefix)
            stdout_output = stdout_output[start + len(prefix):].strip()

            if "videos" in stdout_output:
                # 提取图片路径
                videos = stdout_output.split("videos: ")[1].strip()
                videos = json.loads(videos)
                file_paths.extend(videos)

        return {
            "status": "success",
            "message": "Videos generated successfully",
            "videos": file_paths,
            "media_type": self.media_type,
        }


def upload_task_result(task_id, status, result):
    # 通知任务完成
    requests.post(
        f"{API_BASE_URL}/api/v1/task/complete",
        json={
            "task_id": task_id,
            "status": status,
            "result": result,  # 返回处理结果
        },
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": API_KEY,
        },
    )


def prepare_image_path(file_id):
    file_id = os.path.basename(file_id)
    prefix = file_id[:2]
    os.makedirs(os.path.join(IMAGE_PATH, prefix), exist_ok=True)
    # change to webp file???
    return os.path.join(IMAGE_PATH, prefix, f"{file_id}.png")


def move_image(image_path):
    prepare_image_path(image_path)
    shutil.move(image_path, prepare_image_path(image_path))


def move_images(images):
    for image_path in images:
        move_image(image_path)


def prepare_video_path(file_id):
    file_id = os.path.basename(file_id)
    prefix = file_id[:2]
    os.makedirs(os.path.join(VIDEO_PATH, prefix), exist_ok=True)
    return os.path.join(VIDEO_PATH, prefix, f"{file_id}.mp4")


def move_video(video_path):
    prepare_video_path(video_path)
    shutil.move(video_path, prepare_video_path(video_path))


def move_videos(videos):
    for video_path in videos:
        move_video(video_path)


def process_task(task_id, type, task_data):
    type_cls = {
        "text2image": Text2ImageWorker,
        "image2image": Image2ImageWorker,
        "image2video": Image2VideoWorker,
    }

    cls = type_cls[type]
    instance = cls(task_id, task_data)

    start = time.time()
    resp = instance.run()
    end = time.time()

    elapsed = end - start
    print(f"task id response {resp}, elapsed {elapsed}")

    resp["elapsed"] = elapsed  # 添加处理时间

    # 需要将图像或者视频，转移到目标目录下
    if resp.get("media_type") == "image":
        for image_path in resp["images"]:
            # 存储路径格式要求如下，IMAGE_PATH下面有2个字母构建的目录，然后再将文件放到此目录下
            # 例如：/mnt/f/dev/Imagint/src/backend/images/ab/1234567890.png
            # 其中ab是2个字母构建的目录，1234567890.png是文件名
            # 需要将image_path的文件移动到此目录下
            move_image(image_path)

    elif resp.get("media_type") == "video":
        for video_path in resp["videos"]:
            move_video(video_path)

    task_db.update_task_status(
        task_id, TaskStatus.PROCESSED, json.dumps(resp, ensure_ascii=False)
    )

    status = resp.pop("status", None)  # 移除status字段
    upload_task_result(task_id, status, resp)


def load_tasks():
    tasks = task_db.get_tasks()
    return tasks


def recover_task():
    tasks = load_tasks()

    for task in tasks:
        # 如果任务是已经处理过的，则跳过
        task_id = task["task_id"]

        if task["status"] == TaskStatus.PROCESSED.value:
            result = task["result"]
            status = result["status"]
            upload_task_result(task_id, status, result)
            task_db.delete_task(task_id)
            continue

        type = task["type"]

        print(f"recover task {task_id} {type}")
        process_task(task_id, type, json.loads(task["task_data"]))
        task_db.delete_task(task_id)


def consume():
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

                if task_id is None:
                    print("No task found, waiting for next iteration")
                    time.sleep(1)
                    continue

                type = task_data.get("type")
                if type is None:
                    print("No task type found, waiting for next iteration")
                    time.sleep(1)
                    continue

                if type not in ["text2image", "image2image", "image2video"]:
                    print(f"Unsupported task type: {type}, waiting for next iteration")
                    time.sleep(1)
                    continue

                task_db.add_task(
                    task_id, type, json.dumps(task_data, ensure_ascii=False)
                )
                process_task(task_id, type, task_data)
                task_db.delete_task(task_id)
            else:
                print("get task may occur error", response.status_code)
            # 等待1秒后继续
            time.sleep(1)

        except Exception as e:
            print(f"Error occurred: {str(e)}", traceback.format_exc())
            time.sleep(1)
            continue


def main():
    recover_task()
    consume()


if __name__ == "__main__":
    main()
