from __future__ import annotations
from typing import List,Union
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from .constants import NetValueData, DividendData

@dataclass
class PositionSnapshot:
    date: datetime
    shares: float
    dividend_amount: float
    perf_fee: float
    redeemed_amount: float
    dividend_reinvestment: bool
    highwatermark_price: float
    highwatermark_cumprice: float
    highwatermark_date: datetime
    message: str


class Position:
    def __init__(
        self,
        client_id: str,  # 所属客户
        prodcode: str,  # 买入产品
        creation_date: datetime,  # 创建日期
        cost: float,  # 成本(买入金额)
        init_shares: float = None,  # 初始份额
        init_price: float = None,  # 买入时单位净值
        init_cum_price: float = None,  # 买入时累计净值
        dividend_reinvestment: bool = False,  # 红利再投设置
    ) -> None:
        self.client_id = client_id
        self.prodcode = prodcode
        self.creation_date = creation_date
        self.cost = cost
        self.init_shares = init_shares
        self.init_price = init_price
        self.init_cum_price = init_cum_price

        self.dividend_reinvestment = dividend_reinvestment
        self.snapshots: List[PositionSnapshot] = []
        # 初始化
        self._init()

    def _init(self):
        """初始化头寸状态属性"""
        self.shares = self.init_shares
        self.highwatermark_price = self.init_price
        self.highwatermark_cumprice = self.init_cum_price
        self.highwatermark_date = self.creation_date

        self.dividend_amount = 0
        self.perf_fee = 0
        self.redeemed_amount = 0
        self.create_snapshot(self.creation_date,"创建持仓")

    @property
    def closed(self):
        return self.shares == 0

    def _calc_perf_fee(self, nvdata: NetValueData, shares=None) -> float:
        """
        计算应提取的业绩报酬金额
        """
        if self.highwatermark_cumprice is None or self.highwatermark_price is None:
            return 0
        # R = [ (P1- P0) /P0x] / (T÷365) X100%
        p1 = nvdata.cum_netvalue
        p0 = self.highwatermark_cumprice
        p0x = self.highwatermark_price
        t = (nvdata.date - self.highwatermark_date).days
        try:
            r = ((p1 - p0) / p0x) / (t / 365)
        except ZeroDivisionError:
            raise ZeroDivisionError()
        # Y=N×P0x×(T÷365)×R×20%
        if r > 0:
            if not shares:
                shares = self.shares
            y = shares * p0x * (t / 365) * r * 0.2
            return y
        else:
            return 0

    def extract_fixedtime_perffee(self, nvdata: NetValueData) -> None:
        """
        固定时点提取业绩报酬，缩减份额
        """

        perf_fee = self._calc_perf_fee(nvdata)
        if perf_fee > 0:
            self.shares -= round(perf_fee / nvdata.netvalue, 2)
            self.perf_fee += perf_fee
            self.highwatermark_date = nvdata.date
            self.highwatermark_price = nvdata.netvalue
            self.highwatermark_cumprice = nvdata.cum_netvalue
            self.create_snapshot(nvdata.date, "固定时点提取业绩报酬")

    def handle_dividend(self, nvdata: NetValueData, divdata: DividendData):
        """
        分红,业绩报酬从分红款中扣除
        method:
            cash:现金分红
            reinvest:红利再投
        """
        perf_fee = self._calc_perf_fee(nvdata)
        if perf_fee > 0:
            self.perf_fee += perf_fee
            self.highwatermark_date = nvdata.date
            self.highwatermark_price = nvdata.netvalue
            self.highwatermark_cumprice = nvdata.cum_netvalue

        raw_dividend = self.shares * divdata.dividend_per_share
        dividend = raw_dividend - perf_fee
        if not self.dividend_reinvestment:
            self.dividend_amount += dividend
        else:
            self.shares += round(dividend / nvdata.netvalue, 2)

        self.create_snapshot(nvdata.date,"分红")
        return dividend

    def redempt(
        self,
        nvdata: NetValueData,
        redemptshares: float = None,
        redemptamount: float = None,
    ):
        """
        赎回，业绩报酬计提赎回部分
        """
        if not redemptshares:
            redemptshares = self.shares

        if nvdata is not None:
            perf_fee = self._calc_perf_fee(nvdata=nvdata, shares=redemptshares)
            self.perf_fee += perf_fee

            calc_redeemed_amount = redemptshares * nvdata.netvalue
            if redemptamount is not None:
                self.redeemed_amount += redemptamount
                # if redemptamount != calc_redeemed_amount:
                #     Warning(
                #         f"{self.client.name}于{date}赎回{self.product.name},按净值计算赎回金额应该为{calc_redeemed_amount},实际赎回金额为{redemptamount},请核对"
                #     )
            else:
                self.redeemed_amount += calc_redeemed_amount - perf_fee
        else:
            self.redeemed_amount += redemptamount

        self.shares -= redemptshares
        # self.log("赎回", nvdata)
        self.create_snapshot(nvdata.date, "赎回")

    def market_value(self, nvdata: NetValueData):
        return self.shares * nvdata.netvalue

    def pnl(self, nvdata: NetValueData):
        market_value = self.market_value(nvdata)
        if market_value is not None:
            return (
                market_value + self.dividend_amount + self.redeemed_amount - self.cost
            )
        else:
            return None

    def create_snapshot(self, date,message=None) -> None:
        date = pd.to_datetime(date)
        snapshot = PositionSnapshot(
            date,
            self.shares,
            self.dividend_amount,
            self.perf_fee,
            self.redeemed_amount,
            self.dividend_reinvestment,
            self.highwatermark_price,
            self.highwatermark_cumprice,
            self.highwatermark_date,
            message,
        )
        self.snapshots.append(snapshot)

    def get_snapshot(self, date:Union[str, pd.Timestamp])->PositionSnapshot:
        date = pd.to_datetime(date)
        sorted_snapshots = sorted(self.snapshots, key=lambda s: s.date)
        for snapshot in reversed(sorted_snapshots):
            if snapshot.date <= date:
                return snapshot
        return None
