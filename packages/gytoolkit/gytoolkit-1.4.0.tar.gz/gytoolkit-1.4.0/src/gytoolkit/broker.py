from typing import List, Dict, Union,Optional
import pandas as pd
from .client import Client
from .product import Product
from .constants import TradeData, DividendData,PerfFeeData,FundEventData,OrderData
from .position import Position


class Broker:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.clients: Dict[str, Client] = {}
        self.events_by_dates = {}
        self.logs = []
    
    def add_product(self, product: Union[Product, List[Product]]):
        if isinstance(product, Product):
            product = [product]
        for p in product:
            self.products[p.code] = p

    def get_product(self, prodcode)->Product:
        # Get the fund from the transaction
        product = self.products.get(prodcode)
        if not product:
            product = Product(prodcode)
            self.add_product(product)
        return product

    def add_client(self, client: Union[Client, List[Client]]):
        if isinstance(client, Client):
            client = [client]
        for c in client:
            self.clients[c.id] = c

    def get_client(self, client_id)->Client:
        # Get the fund from the transaction
        client = self.clients.get(client_id)
        if not client:
            client = Client(client_id)
            self.add_client(client)
        return client
    
    def process_trade(self, trade: TradeData):
        # Get the fund from the transaction
        product = self.get_product(trade.prodcode)
        nv_data = product.get_net_value(trade.date)
        client = self.get_client(trade.client_id)

        if trade.divmod == "0-红利转投资":
            dividend_reinvestment = True
        else:
            dividend_reinvestment = False

        # If it's a purchase transaction, create a new position
        if trade.type in ("110-认购", "111-申购"):
            if trade.type == "110-认购":
                if trade.shares is None:
                    Warning("Shares not provided for purchase transaction. Assuming 1 share.")
                    shares = trade.amount
                else:
                    shares = trade.shares
                new_position = Position(
                    client_id=client.id,
                    prodcode=product.code,
                    creation_date=trade.date,
                    cost=trade.amount,
                    init_shares=shares,
                    init_price=1,
                    init_cum_price=1,
                    dividend_reinvestment = dividend_reinvestment
                )

            if trade.type == "111-申购":
                current_nv = product.get_net_value(trade.date)
                if trade.shares is None:
                    shares = trade.amount/current_nv.netvalue
                else:
                    shares = trade.shares
                new_position = Position(
                    client_id=client.id,
                    prodcode=product.code,
                    creation_date=trade.date,
                    cost=trade.amount,
                    init_shares=shares,
                    init_price=current_nv.netvalue,
                    init_cum_price=current_nv.cum_netvalue,
                    dividend_reinvestment = dividend_reinvestment
                )

            client.add_position(new_position)
            product.add_position(new_position)  # Added this line

        # If it's a redemption transaction, remove the shares from the position
        if trade.type == "112-赎回":
            if trade.amount is not None:
                redeemed_amount = trade.amount
            else:
                redeemed_amount = None
            # Get the remaining shares
            if trade.shares is None:
                # 全仓赎回
                remaining_shares = sum(
                    [
                        position.shares
                        for position in client.positions
                        if position.prodcode == trade.prodcode
                    ]
                )
            else:
                remaining_shares = trade.shares
            # Assuming positions have a creation_date attribute
            for position in sorted(client.positions, key=lambda p: p.creation_date):
                if (
                    position.prodcode == trade.prodcode and not position.closed
                ):  # Added a check for the closed attribute
                    if position.shares <= remaining_shares:
                        # Close the entire position
                        remaining_shares -= position.shares
                        # update the redeemed amount
                        position.redempt(nv_data, position.shares, redeemed_amount)
                    else:
                        # Remove part of the position
                        # update the redeemed amount
                        if position.shares < remaining_shares + 0.01:
                            position.redempt(nv_data, position.shares, redeemed_amount)
                        else:
                            position.redempt(nv_data, remaining_shares, redeemed_amount)
                        remaining_shares = 0
                if remaining_shares == 0:
                    break

        if trade.type == "129-分红设置":
            self.set_dividend_method(trade.client_id,trade.prodcode,dividend_reinvestment)
    
        client.add_trade(trade)
        product.trades.append(trade)

    def process_dividend(self, dividend_data: DividendData):
        # Get the fund from the transaction
        product = self.get_product(dividend_data.prodcode)
        nvdata = product.get_net_value(dividend_data.date)

        # Calculate the dividend amount for each position and handle accordingly
        for position in product.positions:
            if not position.closed and position.creation_date <= dividend_data.date:
                position.handle_dividend(nvdata, dividend_data)

        # Add the dividend to the fund's dividends list
        product.add_dividend(dividend_data)

    def extract_perffee(self, perffee_data:PerfFeeData):
        # Get the fund from the transaction
        product = self.get_product(perffee_data.prodcode)
        nvdata = product.get_net_value(perffee_data.date)

        # extract fixed time performance fee
        for position in product.positions:
            if not position.closed and position.creation_date <= perffee_data.date - pd.Timedelta(
                product.info.perf_fee_lock_period, "D"
            ):
                position.extract_fixedtime_perffee(nvdata)

        product.fixedtime_perfees.append(perffee_data.date)

    def add_event(self, event_data):
        if not isinstance(event_data,list):
            event_data = [event_data]
        for e in event_data:
            if e.date in self.events_by_dates:
                self.events_by_dates[e.date].append(e)
            else:
                self.events_by_dates[e.date] = [e]

    def process_events(self,end_date=None,client_ids=None):

        dates = sorted(self.events_by_dates)
        for date in dates:
        # start_date = min(self.events_by_dates.keys())
        # if end_date is None:
        #     end_date = pd.Timestamp.now()
        # dates = pd.date_range(start_date,end_date,freq="D")
        # for date in dates:
            # if date in self.events_by_dates:
            today_events = self.events_by_dates[date]
            today_redemption = [event for event in today_events if event.__class__.__name__ == "TradeData" and event.type=="112-赎回"]
            today_buy = [event for event in today_events if event.__class__.__name__ == "TradeData" and event.type in ["110-认购","111-申购"]]
            today_set_div = [event for event in today_events if event.__class__.__name__ == "TradeData" and event.type=="129-分红设置"]
            today_div = [event for event in today_events if event.__class__.__name__ == "DividendData"]
            today_perffee = [event for event in today_events if event.__class__.__name__ == "PerfFeeData"]

            for event in today_redemption:
                self.process_trade(event)
            for event in today_div:
                self.process_dividend(event)
            for event in today_perffee:
                self.extract_perffee(event)
            for event in today_buy:
                self.process_trade(event)
            for event in today_set_div:
                self.process_trade(event)

    def get_position_statistic(self,position:Position,date)->Optional[Dict]:
        date = pd.to_datetime(date)
        position_snapshot = position.get_snapshot(date)
        
        if position_snapshot is None:
            return None
        
        client = self.get_client(position.client_id)
        prod = self.get_product(position.prodcode)
        nvdata = prod.get_net_value(date)

        market_value = nvdata.netvalue * position_snapshot.shares
        pnl = market_value + position_snapshot.dividend_amount + position_snapshot.redeemed_amount - position.cost
        statistics = {
            "产品代码": prod.code,
            "产品简称": prod.info.shortname,
            "客户代码": client.id,
            "客户名称": client.name,
            "当前日期": date,
            "买入日期": position.creation_date,
            "买入份额": position.init_shares,
            "成本": position.cost,
            "净值日期":nvdata.date,
            "当前净值":nvdata.netvalue,
            "累计净值":nvdata.cum_netvalue,
            "持仓份额": position_snapshot.shares,
            "市值":market_value,
            "分红金额": position_snapshot.dividend_amount,
            "提取业绩报酬": position_snapshot.perf_fee,
            "已赎回金额": position_snapshot.redeemed_amount,
            "盈亏":pnl,
        }
        return statistics
    
    def get_prod_statistics(self,client_id,date,prodcode):
        date = pd.to_datetime(date)
        client = self.get_client(client_id)
        prod = self.get_product(prodcode)
        nvdata = prod.get_net_value(date)

        statistics = {
            "产品代码": prodcode,
            "产品名称": prod.info.shortname,
            "客户代码": client_id,
            "客户名称": client.name,
            "当前日期": date,
            "初次买入日期": [],
            "买入份额": [],
            "成本": [],
            "净值日期":nvdata.date,
            "当前净值": nvdata.netvalue,
            "累计净值": nvdata.cum_netvalue,
            "持仓份额": [],
            "市值": [],
            "分红金额": [],
            "提取业绩报酬": [],
            "已赎回金额": [],
            "盈亏": [],
        }
        for position in self.get_client(client_id).positions:
            if position.prodcode == prodcode:
                pos_stat_dict = self.get_position_statistic(position,date)
                if pos_stat_dict is not None:
                    statistics["初次买入日期"].append(pos_stat_dict["买入日期"])
                    statistics["买入份额"].append(pos_stat_dict["买入份额"])
                    statistics["成本"].append(pos_stat_dict["成本"])
                    statistics["持仓份额"].append(pos_stat_dict["持仓份额"])
                    statistics["市值"].append(pos_stat_dict["市值"])
                    statistics["分红金额"].append(pos_stat_dict["分红金额"])
                    statistics["提取业绩报酬"].append(pos_stat_dict["提取业绩报酬"])
                    statistics["已赎回金额"].append(pos_stat_dict["已赎回金额"])
                    statistics["盈亏"].append(pos_stat_dict["盈亏"])

        if len(statistics["初次买入日期"]) == 0:
            return None
        
        statistics["买入笔数"] = len(statistics["初次买入日期"])            
        statistics["初次买入日期"] = min(statistics["初次买入日期"])
        statistics["买入份额"] = sum(statistics["买入份额"])
        statistics["成本"] = sum(statistics["成本"])
        statistics["持仓份额"] = sum(statistics["持仓份额"])
        statistics["市值"] = sum(statistics["市值"])
        statistics["分红金额"] = sum(statistics["分红金额"])
        statistics["提取业绩报酬"] = sum(statistics["提取业绩报酬"])
        statistics["已赎回金额"] = sum(statistics["已赎回金额"])
        statistics["盈亏"] = sum(statistics["盈亏"])
        return statistics
    
    def get_statistics(self,client_id,date,detail=True,df=True):
        date = pd.to_datetime(date)
        client = self.get_client(client_id)
        prodcodes = set([position.prodcode for position in client.positions])
        stats_list = []
        for prodcode in prodcodes:
            stats = self.get_prod_statistics(client_id,date,prodcode)
            stats_list.append(stats)
        return pd.DataFrame(stats_list)
    
    def set_dividend_method(self, client_id: str, prodcode: str, dividend_reinvestment):
        client = self.get_client(client_id)
        for position in client.positions:
            if position.prodcode == prodcode:
                position.dividend_reinvestment = dividend_reinvestment

    # def get_market_value(self,client_id,date,prodcode=None):
    #     client = self.get_client(client_id)
    #     assets = 0
    #     for position in client.positions:
    #         if prodcode is not None and position.prodcode != prodcode:
    #             continue
    #         position_snapshot = position.get_snapshot(date)
    #         prod = self.get_product(position.prodcode)
    #         nvdata = prod.get_net_value(date)
    #         value = nvdata.netvalue * position_snapshot.shares
    #         assets += value
    #     return assets
                
    # def get_client_holding_status_by_date(self,client_id,date,summary_by_prod=False):
    #     status_list = []
    #     status_by_prod = {}
    #     client = self.get_client(client_id)
    #     for position in client.positions:
    #         prod = self.get_product(position.prodcode)
    #         nvdata = prod.get_net_value(date)
    #         log = position.log("日终记录",nvdata)
    #         status_list.append(log)
    #         # 按产品进行汇总
    #         if summary_by_prod:
    #             cum_item_keys = ["买入份额","持仓份额","成本","市值","分红金额","已赎回金额","提取业绩报酬","盈亏"]
    #             if position.prodcode not in status_by_prod:
    #                 status_by_prod[position.prodcode] = log
    #             else:
    #                 for item in cum_item_keys:
    #                     status_by_prod[position.prodcode][item] += log[item]
        
    #     if summary_by_prod:
    #         return pd.DataFrame.from_dict(status_by_prod, orient="index")
    #     return pd.DataFrame(status_list)


            
    # def process_client_positions(self, clent_id: str, prodcode: str,start_date=None,end_date=None):
    #     self.events_by_dates
    #     client = self.get_client(clent_id)
    #     if start_date = None:
    #         start_date = min(self.events_by_dates.keys())
    #     if end_date = None:
    #         end_date = pd.Timestamp.now()
    #     dates = pd.date_range(start_date,end_date,freq="D")

    #     for date in dates:
            
    #     for position in client.positions:
    #         if position.prodcode == prodcode:
    #             return position

    # def process_order(self,order:OrderData)->TradeData:
    #     prod = self.get_product(order.prodcode)
    #     nvdata = prod.get_net_value(order.date)
    #     if order.type == "认购":
    #         pass
    #     elif order.type == "申购":
    #         pass
    #     elif order.type == "赎回":
    #         pass


