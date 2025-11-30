"""SQLAlchemy数据库连接配置

按照FastAPI官方文档标准结构，配置SQLAlchemy数据库连接
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import get_config
from pathlib import Path

# 数据库文件默认路径
default_db_path = Path(__file__).parent.parent.parent / "data" / "qbot.db"

# 确保数据库目录存在
default_db_path.parent.mkdir(parents=True, exist_ok=True)

# 从配置获取数据库信息
db_type = get_config("database.type", "sqlite")
db_file = get_config("database.file", str(default_db_path))

# 构建数据库URL
if db_type == "sqlite":
    # SQLite数据库URL格式
    db_url = f"sqlite:///{db_file}"
elif db_type == "duckdb":
    # DuckDB数据库URL格式
    db_url = f"duckdb:///{db_file}"
else:
    # 默认使用SQLite
    db_url = f"sqlite:///{db_file}"

# 创建SQLAlchemy引擎
# connect_args仅SQLite需要，用于允许同一连接在不同线程中使用
engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False}  # 仅SQLite需要
)

# 创建会话工厂
# autocommit=False: 不自动提交事务
# autoflush=False: 不自动刷新会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
# 所有SQLAlchemy模型都将继承自这个类
Base = declarative_base()


def get_db():
    """获取数据库会话依赖
    
    用于FastAPI路径操作函数中获取数据库会话
    确保会话在使用后正确关闭
    
    Yields:
        Session: SQLAlchemy数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
