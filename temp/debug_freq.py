import re

# 测试QLib的频率解析正则表达式
freq_regex = r'^([0-9]*)(month|mon|week|w|day|d|minute|min)$'

# 测试各种频率格式
test_freqs = ['day', '1day', 'd', '1d', 'week', '1week', 'w', '1w', 'month', '1month', 'mon', '1mon', 'minute', '1minute', 'min', '1min']

for freq in test_freqs:
    match = re.match(freq_regex, freq)
    if match:
        print(f"✓ '{freq}' 匹配成功: count={match.group(1)}, base={match.group(2)}")
    else:
        print(f"✗ '{freq}' 匹配失败")
