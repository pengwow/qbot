import qlib
from qlib.constant import REG_CN
from qlib.data import D

# 初始化QLib
provider_uri = "/Users/liupeng/.qlib/crypto_data/ql/"  # target_dir
qlib.init(provider_uri=provider_uri, region=REG_CN)

# 测试修复后的代码
try:
    calendar = D.calendar(start_time='2023-01-01', end_time='2023-01-02', freq='day')
    print("修复成功！")
    print(f"交易日历: {calendar}")
except Exception as e:
    print(f"修复失败: {e}")
