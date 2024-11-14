import json 
from pydantic_settings import BaseSettings
from pydantic import  Field, SecretStr
from pathlib import Path



class Settings(BaseSettings):
    # log 配置
    log_level: str = Field(default="info", alias="log-level")
    log_file: str = Field(default="logs/app.log", alias="log-file")
    
    # 设置root-path 
    data_path: str = Field(default="./", alias="root-dir")

    @classmethod
    def from_json(cls, path: Path):
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    
base_dir = Path(__file__).resolve().parent.parent
config_path = base_dir / "config.json"

# 从 config.json 文件加载配置
settings = Settings.from_json(config_path)

# 打印配置以验证
print(settings)