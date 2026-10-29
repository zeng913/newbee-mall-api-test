"""这是配置文件，存放一些全局的配置参数"""

import os
from dotenv import load_dotenv

load_dotenv()

# 这里的 BASE_URL 是服务的基础地址
BASE_URL = "http://localhost:28019"

# 这里的 TEST_LOGIN_NAME 和 TEST_PASSWORD_MD5 是测试账号的登录名和密码
TEST_LOGIN_NAME = os.getenv("TEST_LOGIN_NAME")
TEST_PASSWORD_MD5 = os.getenv("TEST_PASSWORD_MD5")

