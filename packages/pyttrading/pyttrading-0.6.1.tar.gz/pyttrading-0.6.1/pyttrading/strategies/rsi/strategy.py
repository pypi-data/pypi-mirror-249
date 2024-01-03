from ...backtesting_custom.generic_backtesting import GenericBacktesting
from ...utils.pre_processing import remove_noise_trading

from scipy.optimize import minimize
from ta.momentum import RSIIndicator

class Strategy:
    
    def __init__(self, df=None):
        pass
    
    def eval(self, df=None, params=[5, 100]):
        
        if len(params) != 2:
            print(f"Print error")
            return False
        
        window_length, buy_threshold = params
        
        # Calculate the RSI indicator
        rsi_indicator = RSIIndicator(df['close'], window=window_length)
        self.df = df
        df['rsi'] = rsi_indicator.rsi()
        df['actions'] = 0  # Initialize the actions column with 0
        df.loc[df['rsi'] < buy_threshold, 'actions'] = 1  # Buy signal
        df.loc[df['rsi'] >= buy_threshold, 'actions'] = 2 # Sell Signal
        df['actions'] = remove_noise_trading(actions=df['actions'])
        
        
        return df
    
    def objective_function(self, params=[14, 30], df=None):
        result_df = self.eval(df=df.copy(), params=params)
        
        back_testing = GenericBacktesting(
            df=result_df,
            skip=True,
            initial_money=2000.0,
            commission=0.02,
            plot_result=False,
            path_save_result=".",
            print_stacks=False
        )
        return_data, _ = back_testing.calculate_bk()
        
        return -return_data
    
    def optimize(self, params: list = [(5, 100), (5, 100)], initial_guess: list = [5, 5], df=None, method: str = "Nelder-Mead"):
        threshold_bounds = params
        result = minimize(self.objective_function, initial_guess, bounds=threshold_bounds, args=(df,), method=method)
        best_parameters = result.x
        best_return = -result.fun
        return best_return, best_parameters
    
    def experiment(self, df=None, params=[(5, 100), (5, 100)], initial_guess=[5, 5]):
        methods_list = [
            'Nelder-Mead',
            'Powell',
            'CG',
            'L-BFGS-B',
            'COBYLA',
            'trust-constr'
        ]
        results_methods = {}
        results_method_list = []
        result_method_name = []
        
        for method in methods_list:
            print(f"Method: {method}")
            best_return, best_parameters = self.optimize(params=params, initial_guess=initial_guess, df=df, method=method)
            results_method_list.append(best_return)
            result_method_name.append(method)
            results_methods[method] = best_return, best_parameters
        
        # Get the maximum value from results_method_list
        optimize = results_method_list.index(max(results_method_list))
        method = result_method_name[optimize]
        best_return, best_parameters = results_methods[method]
        
        return method, best_return, best_parameters
