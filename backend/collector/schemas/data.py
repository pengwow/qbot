# 数据相关的Pydantic模型定义

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class DataInfoResponse(BaseModel):
    """数据信息响应模型
    
    Attributes:
        qlib_dir: QLib数据目录
        data_loaded: 数据是否已加载
        calendars: 交易日历信息
        instruments: 成分股信息
        features: 特征信息
        total_instruments: 总成分股数量
        total_features: 总特征数量
    """
    qlib_dir: Optional[str] = Field(None, description="QLib数据目录")
    data_loaded: bool = Field(..., description="数据是否已加载")
    calendars: Dict[str, List[str]] = Field(default_factory=dict, description="交易日历信息")
    instruments: Dict[str, List[str]] = Field(default_factory=dict, description="成分股信息")
    features: Dict[str, List[str]] = Field(default_factory=dict, description="特征信息")
    total_instruments: int = Field(default=0, description="总成分股数量")
    total_features: int = Field(default=0, description="总特征数量")


class CalendarInfoResponse(BaseModel):
    """交易日历信息响应模型
    
    Attributes:
        freq: 频率
        dates: 日期列表
        count: 日期数量
    """
    freq: str = Field(..., description="频率")
    dates: List[str] = Field(default_factory=list, description="日期列表")
    count: int = Field(default=0, description="日期数量")


class InstrumentInfoResponse(BaseModel):
    """成分股信息响应模型
    
    Attributes:
        index_name: 指数名称
        symbols: 股票列表
        count: 股票数量
    """
    index_name: str = Field(..., description="指数名称")
    symbols: List[str] = Field(default_factory=list, description="股票列表")
    count: int = Field(default=0, description="股票数量")


class FeatureInfoResponse(BaseModel):
    """特征信息响应模型
    
    Attributes:
        symbol: 股票代码
        features: 特征列表
        count: 特征数量
    """
    symbol: str = Field(..., description="股票代码")
    features: List[str] = Field(default_factory=list, description="特征列表")
    count: int = Field(default=0, description="特征数量")


class LoadDataRequest(BaseModel):
    """加载数据请求模型
    
    空的请求模型，不需要任何参数
    """
    pass


class SymbolFeaturesResponse(BaseModel):
    """股票特征响应模型
    
    Attributes:
        symbol: 股票代码
        features: 特征列表
        count: 特征数量
    """
    symbol: str = Field(..., description="股票代码")
    features: List[str] = Field(default_factory=list, description="特征列表")
    count: int = Field(default=0, description="特征数量")


class DataResponse(BaseModel):
    """数据响应模型，用于返回具体的特征数据
    
    Attributes:
        symbol: 股票代码
        feature: 特征名称
        data: 特征数据，格式为{日期: 值}
        count: 数据数量
    """
    symbol: str = Field(..., description="股票代码")
    feature: str = Field(..., description="特征名称")
    data: Dict[str, float] = Field(default_factory=dict, description="特征数据，格式为{日期: 值}")
    count: int = Field(default=0, description="数据数量")
