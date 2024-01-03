from decouple import AutoConfig
import os


class DatabaseConfig:
    def __init__(self, env_file_path=None):
        # 使用 AutoConfig 自动查找并加载环境变量
        env_file_path = os.path.join(env_file_path, ".env")
        self.config = AutoConfig(search_path=env_file_path)

    def get_db_config(self):
        "获取数据库配置"
        return {
            "user": self.config("DB_USER"),
            "password": self.config("DB_PASSWORD"),
            "host": self.config("DB_HOST"),
            "port": self.config("DB_PORT", default=3306, cast=int),
            "database": self.config("DB_DATABASE"),
        }
