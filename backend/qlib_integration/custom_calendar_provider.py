from typing import List
from qlib.data.data import LocalCalendarProvider

# 确保先导入自定义Freq类，这样修改load_calendar方法时使用的就是自定义的Freq类
from backend.qlib_integration import custom_freq

# 现在导入的Freq就是自定义的Freq类
from qlib.utils.time import Freq

# 导入配置
from backend.qlib_integration.config import FREQ_MAP, CALENDAR_DIR


def patch_file_storage():
    """
    使用monkey patching方式修改FileCalendarStorage类，支持自定义日历文件名
    """
    try:
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # 导入FileCalendarStorage类
        from qlib.data.storage.file_storage import FileCalendarStorage
        
        logger.info("开始修改FileCalendarStorage类")
        
        # 保存原始_freq_file属性
        original_freq_file = FileCalendarStorage._freq_file
        
        @property
        def custom_freq_file(self) -> str:
            """
            自定义_freq_file属性，支持动态数字+时间范围的文件名
            - 当freq='1m'时，返回'1m'
            - 当freq='1min'时，返回'1m'
            - 当freq='5m'时，返回'5m'
            - 当freq='1h'时，返回'1h'
            - 当freq='1d'时，返回'1d'
            
            Returns
            -------
            str
                自定义的频率字符串
            """
            logger.info(f"调用custom_freq_file，self.freq: {self.freq}")
            
            # 检查缓存
            if hasattr(self, "_freq_file_cache"):
                cached_value = getattr(self, "_freq_file_cache")
                logger.info(f"使用缓存的_freq_file值: {cached_value}")
                return cached_value
            
            # 获取频率对象
            freq = self.freq
            logger.info(f"原始freq: {freq}, 类型: {type(freq)}")
            
            if isinstance(freq, str):
                freq_obj = Freq(freq)
                logger.info(f"将字符串freq转换为Freq对象: {freq_obj}")
            else:
                freq_obj = freq
            
            # 获取count和base
            count = freq_obj.count
            base = freq_obj.base
            logger.info(f"freq_obj.count: {count}, freq_obj.base: {base}")
            
            # 根据base属性决定使用哪个后缀
            if base == "min":
                # 分钟频率使用m作为后缀
                suffix = "m"
                logger.info(f"base为min，使用后缀m")
            elif base == "hour":
                # 小时频率使用h作为后缀
                suffix = "h"
                logger.info(f"base为hour，使用后缀h")
            elif base == "day":
                # 天频率使用day作为后缀，因为日历文件名为day.txt
                suffix = "day"
                logger.info(f"base为day，使用后缀day")
            else:
                # 其他频率使用默认逻辑
                logger.info(f"未知base: {base}，使用默认逻辑")
                return original_freq_file.fget(self)
            
            # 构建频率字符串，如1m, 5m, 1h, day
            freq_str = f"{count}{suffix}" if base != "day" else "day"
            logger.info(f"构建的频率字符串: {freq_str}")
            
            # 保存到缓存
            setattr(self, "_freq_file_cache", freq_str)
            logger.info(f"保存_freq_file到缓存: {freq_str}")
            return freq_str
        
        # 替换_freq_file属性
        FileCalendarStorage._freq_file = custom_freq_file
        logger.info("✓ 已成功修改FileCalendarStorage._freq_file属性，支持动态数字+时间范围的文件名")
        print("✓ 已成功修改FileCalendarStorage._freq_file属性，支持动态数字+时间范围的文件名")
        
        # 保存原始uri属性
        original_uri = FileCalendarStorage.uri
        
        @property
        def custom_uri(self):
            """
            自定义uri属性，支持从calendars/目录加载日历文件
            
            Returns
            -------
            Path
                自定义的日历文件路径
            """
            logger.info("调用custom_uri")
            
            try:
                # 获取原始uri
                original_path = original_uri.fget(self)
                logger.info(f"原始uri路径: {original_path}")
                logger.info(f"原始uri路径是否存在: {original_path.exists()}")
                
                # 获取频率字符串
                freq_str = self._freq_file
                logger.info(f"使用_freq_file: {freq_str}")
                
                # 直接使用day.txt作为日历文件名，无论频率是什么
                file_name = "day.txt"
                logger.info(f"使用固定的文件名: {file_name}")
                
                # 构建自定义路径
                parent_dir = original_path.parent
                logger.info(f"parent_dir: {parent_dir}")
                logger.info(f"parent_dir是否存在: {parent_dir.exists()}")
                
                custom_path = parent_dir / file_name
                logger.info(f"构建的自定义路径: {custom_path}")
                logger.info(f"自定义路径是否存在: {custom_path.exists()}")
                
                # 检查目录中的所有文件
                if parent_dir.exists():
                    files = list(parent_dir.iterdir())
                    logger.info(f"目录中的文件: {[f.name for f in files]}")
                
                return custom_path
            except Exception as e:
                logger.error(f"custom_uri执行失败: {e}")
                import traceback
                traceback.print_exc()
                # 如果出现错误，返回原始路径
                original_path = original_uri.fget(self)
                return original_path
        
        # 替换uri属性
        FileCalendarStorage.uri = custom_uri
        logger.info("✓ 已成功修改FileCalendarStorage.uri属性，支持自定义日历文件路径")
        print("✓ 已成功修改FileCalendarStorage.uri属性，支持自定义日历文件路径")
        
    except Exception as e:
        logger.error(f"patch_file_storage error: {e}")
        print(f"patch_file_storage error: {e}")
        import traceback
        traceback.print_exc()


# 自动执行monkey patching
patch_file_storage()






