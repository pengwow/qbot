#!/usr/bin/env python3
"""初始化数据库脚本

确保正确设置Python路径后初始化数据库
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
backend_root = Path(__file__).parent
project_root = backend_root.parent

sys.path.append(str(project_root))

if __name__ == "__main__":
    print("初始化数据库...")
    
    try:
        from collector.db import init_db
        init_db()
        print("数据库初始化成功")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
