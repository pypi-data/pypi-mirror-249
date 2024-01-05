import json
from backtesting import Backtest, Strategy
import pandas as pd

class DataBacktesting(Strategy):
    """
    Custom strategy class for backtesting.
    """

    def init(self):
        """
        Initialization method called at the beginning of the backtest.
        """
        self.buy_signal = False
        self.sell_signal = False

    def next(self):
        """
        Method called for each data point in the backtest.
        Executes buy or sell based on the 'actions' column value.
        """
        if self.data.actions == 1:
            self.buy()
        elif self.data.actions == 2:
            self.sell()


class GenericBacktesting:
    """
    Generic backtesting class.
    """

    def __init__(self, df, skip=True, initial_money=2000.0, commission=0.02, plot_result=True, path_save_result=".", print_stacks :bool=False):
        """
        Initializes the GenericBacktesting object.

        Parameters:
        - df: DataFrame, input data for backtesting.
        - skip: bool, whether to skip column renaming (default: True).
        - initial_money: float, initial amount of money (default: 2000.0).
        - commission: float, commission rate (default: 0.02).
        - plot_result: bool, whether to plot the backtesting result (default: True).
        - path_save_result: str, path to save the backtesting result (default: ".").
        """
        self.df = df
        self.skip = skip
        self.initial_money = initial_money
        self.commission = commission
        self.plot_result = plot_result
        self.path_save_result = path_save_result
        self.print_stacks = print_stacks

    def rename_columns(self):
        """
        Renames the columns of the input DataFrame.

        The columns 'open', 'height', 'low', 'close', and 'volume' are renamed
        to 'Open', 'High', 'Low', 'Close', and 'Volume', respectively.
        """
        self.df_bk = self.df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })

    def calculate_bk(self):
        """
        Calculates the backtesting results and saves them.

        The backtesting results include statistics and optionally plots the result.
        The results are saved in both HTML and JSON formats.
        """
        self.rename_columns()

        self.df_bk_pandas = pd.DataFrame(self.df_bk)
            
        bt = Backtest(self.df_bk_pandas, DataBacktesting,
                    cash=self.initial_money,
                    commission=self.commission,
                    exclusive_orders=True)

        stats = bt.run()

        stats_json = json.loads(stats.to_json()) # Get the value of Return [%]
        
        if self.print_stacks:
            print(stats)
        return stats_json['Return [%]'], stats_json
    
    


def get_backtesting(df=None, initial_money :float = 2000.0):

    back_testing = GenericBacktesting(
                    df=df,
                    skip=True,
                    initial_money=initial_money,
                    commission=0.02,
                    plot_result=False,
                    path_save_result='tmp',
                    print_stacks=False
                )

    return_data, stats_json = back_testing.calculate_bk()
    
    return return_data, stats_json 