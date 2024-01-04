import pandas as pd
from datetime import datetime, date
import numpy as np
class From_:
    def __init__(self, from_):
        self.date = [i.get('date') for i in from_]
        self.days = [i.get('days') for i in from_]
        self.weekly = [i.get('weekly') for i in from_]
        self.unSymbol = [i.get('unSymbol') for i in from_]



        self.data_dict = { 

            'date': self.date,
            'days': self.days,
            'weekly': self.weekly,
            'symbol': self.unSymbol
        }


        self.as_dataframe = pd.DataFrame(self.data_dict)


class BaseData:
    def __init__(self, data):
        self.under_tickerId = data['tickerId'] if 'tickerId' in data else None
        self.name = data['name'] if 'name' in data else None
        self.disSymbol = data['disSymbol'] if 'disSymbol' in data else None
        self.under_close = float(data['close']) if 'close' in data else None
        self.under_preClose = float(data['preClose']) if 'preClose' in data else None
        self.under_volume = float(data['volume']) if 'volume' in data else None
        self.under_open = float(data['open']) if 'open' in data else None
        self.under_high = float(data['high']) if 'high' in data else None
        self.under_low = float(data['low']) if 'low' in data else None
        self.under_change = float(data['change']) if 'change' in data else None
        self.under_changeRatio = round(float(data['changeRatio'])*100,2) if 'changeRatio' in data else None
        self.vol1y = float(data['vol1y']) if 'vol1y' in data else None
        self.expireDateList = data['expireDateList'] if 'expireDateList' in data else None




    @staticmethod
    async def create_table(connection):
        try:
            await connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS base_data (
                    ticker_id VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    dis_symbol VARCHAR,
                    close FLOAT,
                    pre_close FLOAT,
                    volume FLOAT,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    change FLOAT,
                    change_ratio FLOAT,
                    vol1y FLOAT,
                    expire_date_list TEXT[]
                );
                '''
            )
        except Exception as e:
            print(f"Error creating table asynchronously: {e}")




class OptionData:
    def __init__(self, base_response):


        self.under_tickerId = base_response['tickerId'] if 'tickerId' in base_response else None
        self.name = base_response['name'] if 'name' in base_response else None
        self.disSymbol = base_response['disSymbol'] if 'disSymbol' in base_response else None
        self.under_close = float(base_response['close']) if 'close' in base_response else None
        self.under_preClose = float(base_response['preClose']) if 'preClose' in base_response else None
        self.under_volume = float(base_response['volume']) if 'volume' in base_response else None
        self.under_open = float(base_response['open']) if 'open' in base_response else None
        self.under_high = float(base_response['high']) if 'high' in base_response else None
        self.under_low = float(base_response['low']) if 'low' in base_response else None
        self.under_change = float(base_response['change']) if 'change' in base_response else None
        self.under_changeRatio = round(float(base_response['changeRatio'])*100,2) if 'changeRatio' in base_response else None
        self.vol1y = float(base_response['vol1y']) if 'vol1y' in base_response else None


        data = base_response['expireDateList'] if 'expireDateList' in base_response else None
        data = [i.get('data') for i in data if i.get('data') is not None]


        self.data = [item for sublist in data for item in sublist]
        self.open = [float(i.get('open')) if i.get('open') is not None else 0 for i in self.data]
        self.high = [float(i.get('high')) if i.get('high') is not None else 0 for i in self.data]
        self.low = [float(i.get('low')) if i.get('low') is not None else 0 for i in self.data]
        self.strikePrice = [int(float(i.get('strikePrice'))) if i.get('strikePrice') is not None else None for i in self.data]
        self.preClose = [float(i.get('preClose')) if i.get('preClose') is not None else 0 for i in self.data]
        self.openInterest = [float(i.get('openInterest')) if i.get('openInterest') is not None else 0 for i in self.data]
        self.volume = [float(i.get('volume')) if i.get('volume') is not None else 0 for i in self.data]
        self.latestPriceVol = [float(i.get('latestPriceVol')) if i.get('latestPriceVol') is not None else 0 for i in self.data]
        self.delta = [round(float(i.get('delta')),4) if i.get('delta') is not None else 0 for i in self.data]
        self.vega = [round(float(i.get('vega')),4) if i.get('vega') is not None else 0 for i in self.data]
        self.impVol = [round(float(i.get('impVol')),4) if i.get('impVol') is not None else 0 for i in self.data]
        self.gamma = [round(float(i.get('gamma')),4) if i.get('gamma') is not None else 0 for i in self.data]
        self.theta = [round(float(i.get('theta')),4) if i.get('theta') is not None else 0 for i in self.data]
        self.rho = [round(float(i.get('rho')),4) if i.get('rho') is not None else 0 for i in self.data]
        self.close = [float(i.get('close')) if i.get('close') is not None else 0 for i in self.data]
        self.change = [float(i.get('change')) if i.get('change') is not None else 0 for i in self.data]
        self.changeRatio = [round(float(i.get('changeRatio'))*100,2) if i.get('changeRatio') is not None else 0 for i in self.data]
        self.expireDate = [datetime.strptime(i.get('expireDate'), '%Y-%m-%d').date() if i.get('expireDate') is not None else None for i in self.data]
        self.tickerId = [i.get('tickerId') for i in self.data]
        self.belongTickerId = [i.get('belongTickerId') for i in self.data]
        self.openIntChange = [float(i.get('openIntChange')) if i.get('openIntChange') is not None else None for i in self.data]
        self.activeLevel = [float(i.get('activeLevel')) if i.get('activeLevel') is not None else 0 for i in self.data]
        self.cycle = [float(int(i.get('cycle'))) for i in self.data]
        self.direction = [i.get('direction') for i in self.data]
        self.symbol = [i.get('symbol') for i in self.data]
        self.unSymbol = [i.get('unSymbol') for i in self.data]
        self.oi_weighted_delta = self.option_open_interest_weighted_delta(deltas=self.delta, ois=self.openInterest),
        self.iv_spread = self.option_implied_volatility_spread(self.impVol,self.vol1y),
        self.avg_iv = self.average_implied_volatility(),
        self.aggregate_delta = self.get_aggregate_delta(deltas=self.delta, call_puts=self.direction, ois=self.openInterest),
        self.avg_strike_distance = self.average_option_strike_distance(strike_prices=self.strikePrice,underlying_close=self.under_close),
        self.oi_change_vol_adjusted = self.change_in_open_interest_adjusted_for_volume(oi_changes=self.openIntChange, volumes=self.volume),
        self.delta_sensitivity = self.get_delta_sensitivity(self.delta,self.gamma,self.under_change),
        self.iv_skew = self.implied_volatility_skew(ivs=self.impVol, strike_prices=self.strikePrice, underlying_close=self.under_close)
        self.gamma_weighted_range = self.get_gamma_weighted_range(self.high,self.low,self.gamma),

        self.optvol_to_underlying_vol_ratio = self.option_volume_to_underlying_volume_ratio(volumes=self.volume, underlying_vol=self.under_volume),
        self.port_gamma = self.portfolio_gamma(self.gamma,self.openInterest),
        self.port_rho = self.portfolio_rho(self.rho, self.openInterest),
        self.port_theta = self.portfolio_theta(self.theta, self.openInterest),
        self.port_vega = self.portfolio_vega(self.vega, self.openInterest),
        self.oi_pcr = self.put_call_open_interest_ratio(ois=self.openInterest, call_puts=self.direction),
        self.vol_pcr = self.put_call_volume_ratio(self.volume, self.direction)
        self.liquidity_indicator = self.options_liquidity_indicator(self.volume, self.openInterest)
        self.weighted_avg_moneyness = self.weighted_average_moneyness(self.strikePrice, self.under_close, self.openInterest)
        self.vega_weighted_maturity = self.get_vega_weighted_maturity(expirys=self.expireDate, vegas=self.vega)






        


      
        self.data_dict = {
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'strike_price': self.strikePrice,
            'pre_close': self.preClose,
            'open_interest': self.openInterest,
            'volume': self.volume,
            'latest_price_vol': self.latestPriceVol,
            'delta': self.delta,
            'vega': self.vega,
            'imp_vol': self.impVol,
            'gamma': self.gamma,
            'theta': self.theta,
            'rho': self.rho,
            'close': self.close,
            'change': self.change,
            'change_ratio': self.changeRatio,
            'expire_date': self.expireDate,
            'ticker_id': self.tickerId,
            'belong_ticker_id': self.belongTickerId,
            'open_int_change': self.openIntChange,
            'active_level': self.activeLevel,
            'cycle': self.cycle,
            'call_put': self.direction,
            'option_symbol': self.symbol,
            'underlying_symbol': self.unSymbol,
            'oi_weighted_delta': self.option_open_interest_weighted_delta(deltas=self.delta, ois=self.openInterest),
            'iv_spread': self.option_implied_volatility_spread(self.impVol,self.vol1y),
            'avg_iv': self.average_implied_volatility(),
            'aggregate_delta': self.get_aggregate_delta(deltas=self.delta, call_puts=self.direction, ois=self.openInterest),
            'avg_strike_distance': self.average_option_strike_distance(strike_prices=self.strikePrice,underlying_close=self.under_close),
            'oi_change_vol_adjusted': self.change_in_open_interest_adjusted_for_volume(oi_changes=self.openIntChange, volumes=self.volume),
            'delta_sensitivity': self.get_delta_sensitivity(self.delta,self.gamma,self.under_change),
            'gamma_weighted_range': self.get_gamma_weighted_range(self.high,self.low,self.gamma),
            'iv_skew': self.iv_skew,
            'optvol_to_underlying_vol_ratio': self.option_volume_to_underlying_volume_ratio(volumes=self.volume, underlying_vol=self.under_volume),
            'port_gamma': self.portfolio_gamma(self.gamma,self.openInterest),
            'port_rho': self.portfolio_rho(self.rho, self.openInterest),
            'port_theta': self.portfolio_theta(self.theta, self.openInterest),
            'port_vega': self.portfolio_vega(self.vega, self.openInterest),
            'oi_pcr': self.put_call_open_interest_ratio(ois=self.openInterest, call_puts=self.direction),
            'volume_pcr': self.put_call_volume_ratio(self.volume, self.direction),
            'vega_weighted_maturity': self.vega_weighted_maturity,
            'weighted_avg_moneyness': self.weighted_avg_moneyness,
            'liquidity_indicator': self.liquidity_indicator,







        }


        self.as_dataframe = pd.DataFrame(self.data_dict)

    def option_open_interest_weighted_delta(self,deltas, ois):
        return [delta * oi for delta, oi in zip(deltas, ois)]

    def option_volume_to_underlying_volume_ratio(self,volumes, underlying_vol):
        total_option_volume = sum(volumes)
        return total_option_volume / underlying_vol if underlying_vol != 0 else 0

    def option_implied_volatility_spread(self,ivs, underlying_vol_1y):
        return [iv - underlying_vol_1y for iv in ivs]

    def average_option_strike_distance(self, strike_prices, underlying_close):
        return sum([abs(underlying_close - strike) for strike in strike_prices]) / len(strike_prices)

    def put_call_open_interest_ratio(self, ois, call_puts):
        puts = [oi for oi, cp in zip(ois, call_puts) if cp.lower() == 'put']
        calls = [oi for oi, cp in zip(ois, call_puts) if cp.lower() == 'call']
        total_puts = sum(puts)
        total_calls = sum(calls)
        return total_puts / total_calls if total_calls != 0 else 0

    def put_call_volume_ratio(self, volumes, call_puts):
        puts_volume = [vol for vol, cp in zip(volumes, call_puts) if cp.lower() == 'put']
        calls_volume = [vol for vol, cp in zip(volumes, call_puts) if cp.lower() == 'call']
        total_puts_volume = sum(puts_volume)
        total_calls_volume = sum(calls_volume)
        return total_puts_volume / total_calls_volume if total_calls_volume != 0 else 0

    def weighted_average_moneyness(self, strike_prices, underlying_close, ois):
        weighted_moneyness = [(underlying_close - strike) / underlying_close * oi for strike, oi in zip(strike_prices, ois)]
        total_oi = sum(ois)
        return sum(weighted_moneyness) / total_oi if total_oi != 0 else 0

    def change_in_open_interest_adjusted_for_volume(self, oi_changes, volumes):
        return [oi_change / vol if vol != 0 else 0 for oi_change, vol in zip(oi_changes, volumes)]

    def options_liquidity_indicator(self, volumes, ois):
        total_volume = sum(volumes)
        total_open_interest = sum(ois)
        return total_volume / total_open_interest if total_open_interest != 0 else 0



    # Function to calculate the aggregate delta, taking into account the direction of the option (call or put).
    def get_aggregate_delta(self, deltas, call_puts, ois):
        adjusted_deltas = [delta * oi if cp.lower() == 'call' else -delta * oi for delta, cp, oi in zip(deltas, call_puts, ois)]
        return sum(adjusted_deltas)

    # Function to calculate the portfolio gamma, which represents the rate of change of delta.
    def portfolio_gamma(self, gammas, ois):
        weighted_gammas = [gamma * oi for gamma, oi in zip(gammas, ois)]
        return sum(weighted_gammas)

    # Function to calculate the vega exposure of the portfolio.
    def portfolio_vega(self, vegas, ois):
        weighted_vegas = [vega * oi for vega, oi in zip(vegas, ois)]
        return sum(weighted_vegas)

    # Function to calculate the theta decay per day for the portfolio.
    def portfolio_theta(self, thetaas, ois):
        weighted_thetas = [theta * oi for theta, oi in zip(thetaas, ois)]
        return sum(weighted_thetas)

    # Function to calculate the rho exposure for interest rate changes.
    def portfolio_rho(self, rhos, ois):
        weighted_rhos = [rho * oi for rho, oi in zip(rhos, ois)]
        return sum(weighted_rhos)

    # Function to calculate the weighted average implied volatility of all options.
    def average_implied_volatility(self):
        # Convert lists to numpy arrays if they aren't already
        ivs = np.array(self.impVol)
        ois = np.array(self.openInterest)
        
        # Ensure that ois is not empty and contains no negative values
        if ois.size == 0 or (ois < 0).any():
            raise ValueError("Open interest array is empty or contains negative values.")
        
        # Ensure ivs and ois have the same length
        if len(ivs) != len(ois):
            raise ValueError("The length of IVs and OIs must be the same.")

        # Calculate the total implied volatility weighted by open interest
        total_iv = np.dot(ivs, ois)
        # Calculate the total open interest
        total_oi = np.sum(ois)
        # Calculate the average implied volatility
        return total_iv / total_oi if total_oi > 0 else 0

    # Function to calculate the implied volatility surface skewness.
    def implied_volatility_skew(self, ivs, strike_prices, underlying_close):
        if not isinstance(underlying_close, (int, float)):
            raise TypeError("underlying_close must be a single numeric value.")

        # Calculate moneyness for each option
        moneyness = [(strike - underlying_close) / underlying_close for strike in strike_prices]

        # Calculate skewness
        skewness = np.corrcoef(moneyness, ivs)[0, 1] if len(ivs) > 1 and len(moneyness) > 1 else 0
        return skewness


    # Function to measure the sensitivity of the delta to changes in the underlying price.
    def get_delta_sensitivity(self, deltas, gammas, underlying_change):
        return [delta + gamma * underlying_change for delta, gamma in zip(deltas, gammas)]

    # Function to calculate the vega-weighted average maturity of the options.
    def get_vega_weighted_maturity(self, expirys, vegas):
        current_date = datetime.today().date()  # Ensure current_date is a datetime.date object

        # Make sure expirys list contains datetime.date objects
        days_to_expiry = [(expiry - current_date).days if expiry and isinstance(expiry, date) else 0 for expiry in expirys]

        total_vega = sum(vegas)
        vega_weighted_days = sum([days * vega for days, vega in zip(days_to_expiry, vegas)])
        return vega_weighted_days / total_vega if total_vega != 0 else 0



    # Function to calculate the gamma-weighted range of the option.
    def get_gamma_weighted_range(self, highs, lows, gammas):
        ranges = [high - low for high, low in zip(highs, lows)]
        total_gamma = sum(gammas)
        return np.dot(gammas, ranges) / total_gamma if total_gamma != 0 else 0


    @staticmethod
    def create_table(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS wb_opts (
                        ticker_id VARCHAR,
                        belong_ticker_id VARCHAR,
                        open FLOAT,
                        high FLOAT,
                        low FLOAT,
                        strike_price INT,
                        pre_close FLOAT,
                        open_interest FLOAT,
                        volume FLOAT,
                        latest_price_vol FLOAT,
                        delta FLOAT,
                        vega FLOAT,
                        imp_vol FLOAT,
                        gamma FLOAT,
                        theta FLOAT,
                        rho FLOAT,
                        close FLOAT,
                        change FLOAT,
                        change_ratio FLOAT,
                        expire_date DATE,
                        open_int_change FLOAT,
                        active_level FLOAT,
                        cycle FLOAT,
                        call_put VARCHAR,
                        option_symbol VARCHAR,
                        underlying_symbol VARCHAR,
                        PRIMARY KEY (option_symbol, expire_date)
                    );
                    '''
                )
            connection.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    @staticmethod
    async def batch_insert_data(connection, data_frame: pd.DataFrame):
        try:
            records = data_frame.to_records(index=False)
            columns = data_frame.columns.tolist()
            values = ','.join([f"${i+1}" for i in range(len(columns))])
            query = f"INSERT INTO wb_opts ({', '.join(columns)}) VALUES ({values}) ON CONFLICT (option_symbol, expire_date) DO NOTHING"

            async with connection.transaction():
                await connection.executemany(query, records)
        except Exception as e:
            print(f"Error in batch insert: {e}")

    @staticmethod
    async def query_data(connection, query: str):
        try:
            async with connection.transaction():
                rows = await connection.fetch(query)
                return rows
        except Exception as e:
            print(f"Error in querying data: {e}")







      

class GroupData:
    def __init__(self, call_put):
        self.option = [i.get('option') for i in call_put]
        self.side = [i.get('side') for i in call_put]
        self.gravity = [i.get('gravity') for i in call_put]


        self.data_dict = { 
            'option_id': self.option,
            'side': self.side,
            'gravity': self.gravity
        }


        self.as_dataframe = pd.DataFrame(self.data_dict)