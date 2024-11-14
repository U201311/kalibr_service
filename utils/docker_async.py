import asyncio
import docker
from docker.errors import ContainerError, ImageNotFound, APIError
from loguru import logger

async def docker_login(client, username, password):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, client.login, username, password)



async def image_exists_locally(image_name: str, client):
    loop = asyncio.get_event_loop()
    images = await loop.run_in_executor(None, client.images.list)
    for image in images:
        if image_name in image.tags:
            return True
    return False



async def pull_docker_image(image_name: str, client):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, client.images.pull, image_name)

async def run_docker_container(image_name: str, command: str, environment, volumes, client=None):
    if client is None:
        client = docker.from_env()
    
    try:
        
        # 拉取镜像
        if not await image_exists_locally(image_name, client):
            # 拉取镜像
            await pull_docker_image(image_name, client)

        logger.info(f"Running Docker container with image {image_name}")
        
        # 运行容器
        container = await asyncio.to_thread(client.containers.run, image_name, command, detach=True, environment=environment, volumes=volumes)
        logger.info(f"Running Docker container {container.id}")
        
        docker_run_cmd = f"docker run -it --rm  -e {environment} -v {volumes}"
        docker_run_cmd += f" {image_name} {command} --name {container.name} "
        
        print(f"Running Docker container with command: {docker_run_cmd}")
        
        # 等待容器完成
        result = await asyncio.to_thread(container.wait)
        logs = await asyncio.to_thread(container.logs)
        if result["StatusCode"]  != 0:
            logger.info(f"Docker container: {result} finished with status code {result['StatusCode']}")
            await asyncio.to_thread(container.remove)
            return {"status": "success"}
        
        # 获取容器日志
        print(logs.decode('utf-8'))
        # 删除容器
        await asyncio.to_thread(container.remove)
        
        return {
            "status": "success",
            "result": result,
            "logs": logs.decode('utf-8'),
            "name": container.name
        }
    except ImageNotFound as e:
        logger.error(f"Image not found: {e}")
    except ContainerError as e:
        logger.error(f"Error running Docker container: {e}")
    except APIError as e:
        logger.error(f"API error: {e}")
    finally:
        client.close()