import uuid
import zipfile
from fastapi import APIRouter, BackgroundTasks, UploadFile, File,HTTPException
import os
from config.config import settings
from utils.docker_async import run_docker_container
from fastapi.responses import JSONResponse
import aiofiles
from fastapi.responses import FileResponse
import yaml
import shutil

router = APIRouter()

async def run_docker_task(docker_image, environment, volumes, data_path):
    result = await run_docker_container(docker_image, "", environment, volumes)
    
    if result and result["status"] == "success":
        # 查看data_path路径下是否有yaml文件
        yaml_file_path = os.path.join(data_path, "checkboard.yaml")
        if os.path.exists(yaml_file_path):
            return yaml_file_path
    return None

@router.post("/kalib_task")
async def kalib_task(background_tasks: BackgroundTasks, left_zip: UploadFile = File(...), right_zip: UploadFile = File(...), yaml_file: UploadFile = File(...)):
    # Step 1: 新建任务存储文件的地址
    data_path = settings.data_path
    task_id = str(uuid.uuid4())
    task_data_path = os.path.join(data_path, task_id)
    os.makedirs(task_data_path, exist_ok=True)
    
    # Step 2: 接收上传的left压缩文件，并存储在新建任务下的data/left文件夹下
    left_data_path = os.path.join(task_data_path, "data", "left")
    os.makedirs(left_data_path, exist_ok=True)
    left_zip_path = os.path.join(left_data_path, left_zip.filename)
    with open(left_zip_path, "wb") as f:
        f.write(await left_zip.read())
    with zipfile.ZipFile(left_zip_path, 'r') as zip_ref:
        zip_ref.extractall(left_data_path)
    
    # Step 3: 接收上传的right压缩文件，并存储在新建任务下的data/right文件夹下
    right_data_path = os.path.join(task_data_path, "data", "right")
    os.makedirs(right_data_path, exist_ok=True)
    right_zip_path = os.path.join(right_data_path, right_zip.filename)
    with open(right_zip_path, "wb") as f:
        f.write(await right_zip.read())
    with zipfile.ZipFile(right_zip_path, 'r') as zip_ref:
        zip_ref.extractall(right_data_path)
    
    # Step 4: 接收上传的yaml文件，并存储在新建任务文件夹下
    yaml_file_path = os.path.join(task_data_path, yaml_file.filename)
    # with open(yaml_file_path, "wb") as f:
        # f.write(await yaml_file.read())
    async with aiofiles.open(yaml_file_path, "wb") as f:
        content = await yaml_file.read()
        await f.write(content)

    
    # Step 5: 将上传数据启动docker容器，并返回前端容器开始结果
    environment = {
        'DISPLAY': ':0',  # 确保 DISPLAY 环境变量正确
        'QT_X11_NO_MITSHM': '1',
        'BAG': '/data/data/camera.bag',
        'TARGET': '/data/checkboard.yaml',
        'MODELS': 'pinhole-radtan pinhole-radtan',
        'LEFT_TOPIC': '/camera/left/image_raw',
        'RIGHT_TOPIC': '/camera/right/image_raw',
        'TOPICS': '/camera/left/image_raw /camera/right/image_raw',
        'INPUT_DATA': "/data/data",        
    }
    
    volumes = {
        '/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'},
        task_data_path: {'bind': '/data', 'mode': 'rw'},
    }

    # 启动后台任务
    background_tasks.add_task(run_docker_task, "kalibr:v2", environment, volumes, task_data_path)
    
    return {
        "message": "Kalib task started",
        "task_id": task_id
    }
    

@router.get("/kalib_task_result/{task_id}")
async def kalib_task_result(task_id: str):
    data_path = settings.data_path
    task_data_path = os.path.join(data_path, task_id)
    yaml_file_path = os.path.join(task_data_path, 'data', "camera-camchain.yaml")
    
    # 读取yaml_file_path文件内容并返回
    
    
    if os.path.exists(yaml_file_path):
        # 构建 YAML 文件的 URL
        # yaml_url = f"/static/{task_id}/data/camera-camchain.yaml"
        with open(yaml_file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)

        # 确保文件在静态文件目录中
        # static_file_path = os.path.join("static", task_id, "data", "camera-camchain.yaml")
        # os.makedirs(os.path.dirname(static_file_path), exist_ok=True)
        # if not os.path.exists(static_file_path):
        #     with open(yaml_file_path, 'r') as src_file:
        #         with open(static_file_path, 'w') as dst_file:
        #             dst_file.write(src_file.read())

        
        # 返回yaml内容
        
        return JSONResponse(content={
            "message": "Kalib task completed",
            "status": 1,
            "yaml_url": yaml_content
        })
    elif os.path.exists(os.path.join(task_data_path, "checkboard.yaml")):
        ## 返回JSONResponse
        return JSONResponse(content={
            "message": "Kalib task is running",
            "status": 2,
            "yaml_url": None
        })
    else :
        return JSONResponse(content={
            "message": "Kalib task is failed",
            "status": 3,
            "yaml_url": None
        })



@router.get("/static/{task_id}/data/camera-camchain.yaml") 
async def dowmload_file(task_id: str):
    # 将文件压缩后返回给前端
    
    file_path = f"/static/{task_id}/data/camera-camchain.yaml"
    zip_path = f"/static/{task_id}/camera-camchain.zip"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 压缩文件
    with shutil.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

    return FileResponse(zip_path, filename="camera-camchain.zip")    
