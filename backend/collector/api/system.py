from fastapi import APIRouter
from loguru import logger
import platform
import psutil
import time
from datetime import datetime
from typing import Dict, Any

from ..schemas import ApiResponse
from ..schemas.system import SystemInfoResponse


# 创建API路由实例
router = APIRouter(prefix="/api/system", tags=["system-info"])

# 应用启动时间
start_time = time.time()


@router.get("/info", response_model=ApiResponse)
def get_system_info():
    """获取系统信息
    
    Returns:
        ApiResponse: 包含系统信息的响应
    """
    try:
        logger.info("开始获取系统信息")
        
        # 获取版本信息
        version_info = {
            "system_version": "1.0.0",  # 系统版本，可从配置文件或环境变量获取
            "python_version": platform.python_version(),
            "build_date": "2025-11-30"  # 构建日期，可从环境变量或配置文件获取
        }
        
        # 计算运行时间
        uptime_seconds = time.time() - start_time
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        uptime_str = f"{days} 天 {hours} 小时"
        
        # 获取运行状态
        running_status = {
            "uptime": uptime_str,
            "status": "running",
            "status_color": "green",
            "last_check": datetime.now()
        }
        
        # 获取资源使用情况
        # CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_used = round(memory.used / (1024 ** 3), 2)
        memory_total = round(memory.total / (1024 ** 3), 2)
        memory_str = f"{memory_used}GB / {memory_total}GB"
        
        # 磁盘空间使用情况
        disk = psutil.disk_usage('/')
        disk_used = round(disk.used / (1024 ** 3), 2)
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_str = f"{disk_used}GB / {disk_total}GB"
        
        resource_usage = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_str,
            "disk_space": disk_str
        }
        
        # 构建响应数据
        system_info = {
            "version": version_info,
            "running_status": running_status,
            "resource_usage": resource_usage
        }
        
        logger.info("成功获取系统信息")
        
        return ApiResponse(
            code=0,
            message="获取系统信息成功",
            data=system_info
        )
    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        return ApiResponse(
            code=1,
            message="获取系统信息失败",
            data=str(e)
        )
