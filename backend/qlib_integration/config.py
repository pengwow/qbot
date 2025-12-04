# 频率映射配置
# 用于自定义日历文件名的频率映射
# 格式：{原始频率: 目标文件名}
# 例如：{"1min": "1m", "min": "m"}

FREQ_MAP = {
    "1min": "1m",  # 将1min映射到1m
    "min": "m",     # 将min映射到m
    "1h": "1h",     # 将1h映射到1h
    "hour": "h",     # 将hour映射到h
    "1d": "1d",     # 将1d映射到1d
    "day": "d"       # 将day映射到d
}

# 日历文件目录
CALENDAR_DIR = "calendars"
