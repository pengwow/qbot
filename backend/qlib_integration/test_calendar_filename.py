#!/usr/bin/env python3
"""
测试日历文件名生成
验证不同频率格式下生成的日历文件名是否符合预期
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from qlib.data.storage.file_storage import FileCalendarStorage
from qlib.utils.time import Freq


def test_calendar_filename():
    """
    测试不同频率下的日历文件名生成
    """
    print("测试日历文件名生成")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        ('1m', '1m.txt'),
        ('1min', '1m.txt'),
        ('5m', '5m.txt'),
        ('30m', '30m.txt'),
        ('1h', '1h.txt'),
        ('2h', '2h.txt'),
        ('1d', '1d.txt'),
        ('5d', '5d.txt'),
    ]
    
    # 模拟FileCalendarStorage对象
    class MockFileCalendarStorage:
        def __init__(self, freq):
            self.freq = freq
            self.future = False
            
            # 导入自定义的freq_file属性
            from backend.qlib_integration import custom_calendar_provider
            
        @property
        def file_name(self) -> str:
            return f"{self._freq_file}_future.txt" if self.future else f"{self._freq_file}.txt".lower()
    
    # 测试每个频率
    for freq, expected_filename in test_cases:
        try:
            # 创建模拟对象
            mock_storage = MockFileCalendarStorage(freq)
            
            # 获取_freq_file属性
            freq_file = FileCalendarStorage._freq_file.fget(mock_storage)
            
            # 生成文件名
            file_name = f"{freq_file}.txt".lower()
            
            # 验证结果
            if file_name == expected_filename:
                print(f"✓ {freq:<8} -> {file_name:<10} (预期: {expected_filename})")
            else:
                print(f"✗ {freq:<8} -> {file_name:<10} (预期: {expected_filename})")
        except Exception as e:
            print(f"✗ {freq:<8} -> 错误: {str(e)}")
    
    print("=" * 50)
    print("测试完成!")


if __name__ == "__main__":
    # 先导入自定义频率和日历提供者
    from backend.qlib_integration import custom_freq, custom_calendar_provider
    
    # 运行测试
    test_calendar_filename()
