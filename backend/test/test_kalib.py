import requests

url = "http://localhost:8000/kalib/kalib_task"

# 准备文件
left_zip_file = {'left_zip': open('/home/ying01li/kalib_service/data/data/left.zip', 'rb')}
right_zip_file = {'right_zip': open('/home/ying01li/kalib_service/data/data/right.zip', 'rb')}
yaml_file = {'yaml_file': open('/home/ying01li/kalib_service/data/checkboard.yaml', 'rb')}

# 发送POST请求
response = requests.post(url, files={**left_zip_file, **right_zip_file, **yaml_file})

# 打印响应
print(response.json())
