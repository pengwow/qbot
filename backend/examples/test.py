
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent 
sys.path.append(str(project_root))
from backend.qlib_integration import custom_calendar_provider

# 初始化qlib
import qlib
qlib.init(
    provider_uri='~/.qlib/crypto_data/qlib_data',
)
from qlib.data import D
ddd = D.calendar(start_time="2025-11-01", end_time="2025-11-30", freq="1m")
print(ddd[:2])  # calendar data

df = D.features(
    ["btcusdt"],
    ["$open", "$high", "$low", "$close", "$factor"],
    start_time="2025-11-01",
    end_time="2025-11-30",
    freq='1m'
)
print(df.head())

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "notebook"
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df.index.get_level_values("datetime"),
            open=df["$open"],
            high=df["$high"],
            low=df["$low"],
            close=df["$close"],
        )
    ]
)
fig.show()