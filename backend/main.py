from typing import Union
from contextlib import asynccontextmanager

from fastapi import FastAPI
from collector.routes import router as collector_router
from factor.routes import router as factor_router
from model.routes import router as model_router
from backtest.routes import router as backtest_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理
    
    Args:
        app: FastAPI应用实例
    
    Yields:
        None: 无返回值
    """
    # 启动时初始化数据库
    from collector.db import init_db
    init_db()
    
    # 初始化任务管理器，确保数据库表已创建
    from collector.utils.task_manager import task_manager
    task_manager.init()
    
    yield
    # 关闭时的清理工作


app = FastAPI(lifespan=lifespan)

# 注册数据处理API路由
app.include_router(collector_router)

# 注册因子计算API路由
app.include_router(factor_router)

# 注册模型训练API路由
app.include_router(model_router)

# 注册回测服务API路由
app.include_router(backtest_router)


@app.get("/")
def read_root():
    """根路径的处理函数
    
    Returns:
        dict: 返回一个包含问候语的字典
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """获取指定item_id的项目信息
    
    Args:
        item_id: 项目ID
        q: 可选的查询参数
    
    Returns:
        dict: 返回包含项目ID和查询参数的字典
    """
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    """当直接运行此文件时启动FastAPI应用服务器
    
    使用uvicorn作为ASGI服务器，在本地主机的8000端口启动应用
    禁用自动重载功能，避免DuckDB锁冲突
    """
    from collector.db import init_db
    # 只在主进程中初始化数据库，避免热重载时的锁冲突
    init_db()
    import uvicorn
    uvicorn.run(
        "main:app",  # 指定应用路径
        host="127.0.0.1",  # 主机地址
        port=8000,  # 端口号
        reload=False  # 禁用热重载，避免DuckDB锁冲突
    )
    