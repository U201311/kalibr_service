import docker
import asyncio
from loguru import logger

def pull_docker_image(image_name: str, client=None):
    if client is None:
        client = docker.from_env()
    try:
        # 判断镜像是否存在
        images = client.images.list()
        if image_name in [tag for image in images for tag in image.tags]:
            logger.info(f"Image {image_name} already exists.")
            return
        
        # 拉取镜像
        client.images.pull(image_name)
        logger.info(f"Image {image_name} pulled successfully.")
    except docker.errors.ImageNotFound as e:
        logger.error(f"Error pulling Docker image: {e}")
        raise
    except docker.errors.APIError as e:
        logger.error(f"Error pulling Docker image: {e}")
        raise
    finally:
        client.close()



def run_docker_container(image_name: str, command: str, environment, volumes, client=None):
    if client is None:
        client = docker.from_env()
    
    try:
        # 拉取镜像
        pull_docker_image(image_name, client)
        logger.info(f"Running Docker container with image {image_name}")
        
        # 运行容器
        container = client.containers.run(
                    image_name, 
                    command, 
                    detach=True, 
                    environment=environment, 
                    volumes=volumes                )        
        logger.info(f"Running Docker container {container.id}")
        
        docker_run_cmd = f"docker run -it --rm  -e {environment} -v {volumes}"
        docker_run_cmd+= f" {image_name} {command} --name {container.name} "
        
        print(f"Running Docker container with command: {docker_run_cmd}")
        
        # 等待容器完成
        result = container.wait()
        logs = container.logs()
        if result["StatusCode"] != None:
            logger.info(f"Docker container: {result} finished with status code {result['StatusCode']}")
            container.remove()
            return {"status": "sucess"}
        
        # 获取容器日志
        
        print(logs.decode('utf-8'))
        # 删除容器
        container.remove()
        
        return {
            "status": "success",
            "result": result,
            "logs": logs.decode('utf-8'),
            "name": container.name
        }
    except docker.errors.ContainerError as e:
        logger.error(f"Error running Docker container: {e}")
    except docker.errors.ImageNotFound as e:
        logger.error(f"Error running Docker container: {e}")
    except docker.errors.APIError as e:
        logger.error(f"Error running Docker container: {e}")
    finally:
        client.close()


def main():
    client = docker.from_env()
    # 示例调用
    environment = {
        'DISPLAY': ':0',  # 确保 DISPLAY 环境变量正确
        'QT_X11_NO_MITSHM': '1',
        'BAG': '/data/data/camera_7.bag',
        'TARGET': '/data/checkboard.yaml',
        'MODELS': 'pinhole-radtan pinhole-radtan',
        'LEFT_TOPIC': '/camera/left/image_raw',
        'RIGHT_TOPIC': '/camera/right/image_raw',
        'TOPICS': '/camera/left/image_raw /camera/right/image_raw',
        'INPUT_DATA':'/data/data',        
    }
    data_path = "/home/ying01li/kalib_service/data"
    volumes = {
        '/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'},
        data_path: {'bind': '/data', 'mode': 'rw'},
    }
    docker_command=""
    result = run_docker_container("kalibr:v1", docker_command, environment, volumes,client)
    print(result)

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
 

if __name__ == "__main__":
    main()
