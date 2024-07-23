## Class for each order that the user passes to the program

def float_convert(potential_float):
    try:
        return float(potential_float) if potential_float is not None else None
    except ValueError:
        print(f"Error in order_class file converting the '{potential_float}' user input")


def int_convert(potential_int):
    try:
        return float(potential_int) if potential_int is not None else None
    except ValueError:
        print(f"Error in order_class file converting the '{potential_int}' user input")


class Order:
    def __init__(self,
                 # Required user inputs
                 bot_type,
                 asset,
                 capital,
                 start_type,
                 percent_loss_limit,
                 profit_loss_function,
                 initial_capital,
                 menu,
                 log_trade,
                 # Individually optional user inputs
                 buy_order_type=None,
                 sell_order_type=None,
                 asset_bought_price=None,
                 basic_buy_price=None,
                 basic_sell_profit=None,
                 swing_trade_skim=None,
                 rsi_buy_number=None,
                 rsi_drop_limit=None,
                 rsi_wait_period=None,
                 minimum_ladder_profit=None,
                 ladder_step_gain=None,
                 ladder_step_loss=None,
                 ladder_timer_duration=None,
                 ladder_step_sensitivity=None,
                 ladder_timer_sensitivity=None,
                 history=None,
                 amount_bought=None,
                 ):
        self.bot_type = bot_type
        self.asset = asset
        self.capital = capital
        self.start_type = start_type
        self.percent_loss_limit = -float_convert(percent_loss_limit)
        self.profit_loss_function = profit_loss_function
        self.initial_capital = float_convert(initial_capital)
        self.menu = menu
        self.log_trade = log_trade
        self.buy_order_type = buy_order_type
        self.sell_order_type = sell_order_type
        self.asset_bought_price = float_convert(asset_bought_price)
        self.basic_buy_price = float_convert(basic_buy_price)
        self.basic_sell_profit = float_convert(basic_sell_profit)
        self.swing_trade_skim = float_convert(swing_trade_skim)
        self.rsi_buy_number = int_convert(rsi_buy_number)
        self.rsi_drop_limit = int_convert(rsi_drop_limit)
        self.rsi_wait_period = rsi_wait_period
        self.minimum_ladder_profit = float_convert(minimum_ladder_profit)
        self.ladder_step_gain = float_convert(ladder_step_gain)
        self.ladder_step_loss = float_convert(ladder_step_loss)
        self.ladder_timer_duration = ladder_timer_duration
        self.ladder_step_sensitivity = float_convert(ladder_step_sensitivity)
        self.ladder_timer_sensitivity = float_convert(ladder_timer_sensitivity)
        self.history = history
        self.amount_bought = amount_bought

    def __repr__(self):
        return (f"Order(bot_type={self.bot_type}, asset={self.asset}, capital={self.capital}, "
                f"start_type={self.start_type}, buy_order_type={self.buy_order_type}, "
                f"sell_order_type={self.sell_order_type}, percent_loss_limit={self.percent_loss_limit}, "
                f"profit_loss_function={self.profit_loss_function}, initial_capital={self.initial_capital}, "
                f"asset_bought_price={self.asset_bought_price}, basic_buy_price={self.basic_buy_price}, "
                f"basic_sell_profit={self.basic_sell_profit}, swing_trade_skim={self.swing_trade_skim}, "
                f"menu={self.menu}, rsi_buy_number={self.rsi_buy_number}, rsi_drop_limit={self.rsi_drop_limit}, "
                f"rsi_wait_period={self.rsi_wait_period}, minimum_ladder_profit={self.minimum_ladder_profit}, "
                f"ladder_step_gain={self.ladder_step_gain}, ladder_step_loss={self.ladder_step_loss}, "
                f"ladder_timer_duration={self.ladder_timer_duration}, ladder_step_sensitivity={self.ladder_step_sensitivity},"
                f"ladder_timer_sensitivity={self.ladder_timer_sensitivity}, history={self.history})")

    def buy_scan(self):
        pass

    def sell_scan(self):
        pass
