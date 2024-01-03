from ...backtesting_custom.generic_backtesting import GenericBacktesting
from ...utils.pre_processing import remove_noise_trading
from scipy.optimize import minimize
from ta.trend import EMAIndicator


class Strategy:
    
    def __init__(self, df=None):
        self.df = df

    def eval(self, df=None, params=[20, 2]):
        # window_length, stddev_threshold = map(int, params)
        
        if len(params) != 2:
            return False
        window_length, stddev_threshold = params
        

        # Calculate the EMA indicator
        ema_indicator = EMAIndicator(close=df['close'], window=window_length)
        df['ema'] = ema_indicator.ema_indicator()

        # Initialize the actions column with 0
        df['actions'] = 0

        # Generate buy signals based on EMA indicator
        df.loc[df['close'] > df['ema'], 'actions'] = 1  # Buy signal
        df.loc[df['close'] < df['ema'], 'actions'] = 2  # Sell signal

        df['actions'] = remove_noise_trading(actions=df['actions'])

        return df

    def objective_function(self, params=[20, 2], df=None):
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

    def optimize(self, params=[(2, 50), (1, 10)], initial_guess=[2, 2], df=None, method="Nelder-Mead"):
        result = minimize(self.objective_function, initial_guess, bounds=params, args=(df,), method=method)
        best_parameters = result.x
        best_return = -result.fun
        return best_return, best_parameters

    def experiment(self, df=None, params=[(2, 50), (1, 10)], initial_guess=[2, 2]):
        methods_list = [
            'Nelder-Mead',
            'Powell',
            'CG',
            # 'BFGS',
            'L-BFGS-B',
            'TNC',
            # 'COBYLA',
            'SLSQP',
            'trust-constr',
            # 'dogleg',
            # 'trust-ncg',
            # 'trust-exact',
            # 'trust-krylov'
        ]
        results_methods = {}
        results_method_list = []
        result_method_name = []

        for method in methods_list:
            try:
                print(f"Method: {method}")
                best_return, best_parameters = self.optimize(params=params, initial_guess=initial_guess, df=df, method=method)
                results_method_list.append(best_return)
                result_method_name.append(method)
                results_methods[method] = best_return, best_parameters
            except Exception as e:
                print(f"Error in method {method}: {e}")

        # Get the maximum value from results_method_list
        optimize = results_method_list.index(max(results_method_list))
        method = result_method_name[optimize]
        best_return, best_parameters = results_methods[method]

        return method, best_return, best_parameters
