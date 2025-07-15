# server/main.py
import requests
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os

# --- Jenkins 连接配置 ---
JENKINS_URL = os.getenv('JENKINS_URL', 'http://127.0.0.1:8080')
JENKINS_USERNAME = os.getenv('JENKINS_USERNAME', 'hugh')
JENKINS_API_TOKEN = os.getenv('JENKINS_API_TOKEN', '11c07273b54dbe71c17da03e829533aa0e')
# --------------------------------

app = FastAPI(title="Juez del Juego v0.4 - Jenkins Controller (requests based)")

origins = [
    "http://localhost",
    "http://localhost:3000", # 允许来自Next.js开发服务器的请求
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 允许访问的源
    allow_credentials=True,    # 允许携带cookies
    allow_methods=["*"],       # 允许所有HTTP方法 (GET, POST, PUT, OPTIONS 等)
    allow_headers=["*"],       # 允许所有HTTP请求头
)
# 我们不再需要在启动时连接，而是在每次请求时连接，这样更健壮

def get_jenkins_crumb(auth):
    """获取Jenkins的CSRF令牌(Crumb)"""
    crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
    try:
        response = requests.get(crumb_url, auth=auth, timeout=10)
        response.raise_for_status()
        crumb_data = response.json()
        return {crumb_data['crumbRequestField']: crumb_data['crumb']}
    except Exception as e:
        print(f"获取Crumb失败: {e}")
        raise HTTPException(status_code=500, detail=f"Could not get Jenkins crumb: {e}")


@app.get("/")
async def root():
    return {"message": "Juez del Juego v0.4 is online. Ready to control Jenkins."}


# 在 server/main.py 文件中，只替换这个函数
# 其他部分（import, 配置, get_jenkins_crumb等）保持不变

@app.post("/v1/jobs/{job_name}/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_jenkins_build(job_name: str):
    """
    通过 'requests' 库远程触发一个指定的Jenkins流水线任务，
    并从响应头中解析出队列编号。
    """
    print(f"--- 接收到构建请求，目标任务: {job_name} ---")
    auth = HTTPBasicAuth(JENKINS_USERNAME, JENKINS_API_TOKEN)

    # 1. 获取Crumb
    crumb_header = get_jenkins_crumb(auth)
    if not crumb_header:
        raise HTTPException(status_code=500, detail="Failed to get a valid crumb from Jenkins.")

    # 2. 触发构建
    build_url = f"{JENKINS_URL}/job/{job_name}/build"
    try:
        print(f"正在使用Crumb触发任务 '{job_name}'...")
        response = requests.post(build_url, auth=auth, headers=crumb_header, timeout=10)
        response.raise_for_status()  # 检查 4xx/5xx 错误

        # Jenkins成功接收任务后，会返回 201 Created
        if response.status_code == 201:
            # ======================= 新增的核心逻辑 =======================
            queue_url = response.headers.get('Location')
            queue_item_number = None

            if queue_url:
                # 从URL中解析出队列编号
                # 例如从 'http://.../queue/item/123/' 中提取 '123'
                try:
                    # strip('/') 移除末尾的斜杠，split('/') 按斜杠分割，[-1] 取最后一部分
                    queue_item_number = int(queue_url.strip('/').split('/')[-1])
                    print(f"从响应头'Location'中成功解析出队列编号: {queue_item_number}")
                except (ValueError, IndexError):
                    print(f"警告：找到了Location响应头，但无法解析出队列编号。URL: {queue_url}")
            else:
                print("警告：Jenkins的响应中没有找到'Location'头，无法获取队列编号。")
            # ==========================================================

            print(f"任务 '{job_name}' 已成功放入队列。")

            # 现在我们把队列编号也返回给前端
            return {
                "message": "Build triggered successfully!",
                "job_name": job_name,
                "jenkins_queue_item": queue_item_number
            }
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Jenkins returned an unexpected status code: {response.text}")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Job '{job_name}' not found on Jenkins.")
        else:
            raise HTTPException(status_code=500, detail=f"HTTP Error when triggering build: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")