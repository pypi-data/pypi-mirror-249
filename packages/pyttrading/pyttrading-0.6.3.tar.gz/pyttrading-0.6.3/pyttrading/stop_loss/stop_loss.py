
from scipy.optimize import minimize
from ..backtesting_custom.generic_backtesting import get_backtesting


def stop_loss_simple(data=None, stop_loss=-0.05, init_capital :float = 2000, column_action_name :str = 'actions', sell_value :int = 2):
    
    price_buy = None
    qty_buy = None
    capital = init_capital

    dff = data.copy()
    for i, action in enumerate(dff['actions']):
        if action == 1:
            # price_buy = dff['close'][i]
            price_buy = dff['close'].iloc[i]
            price_buy = float(price_buy)
            capital = float(capital)

            qty_buy = capital/price_buy

        if qty_buy:
            # current_capital = qty_buy * dff['close'][i]
            current_capital = qty_buy * dff['close'].iloc[i]

            equity = (current_capital-capital)/capital

            if equity < stop_loss:
                dff.loc[dff.index[i], column_action_name] = sell_value

                qty_buy = None
                
                try:
                    filtered_df = dff.iloc[i+1:]
                    idx = filtered_df.index[filtered_df["actions"] == 2][0]
                    dff.at[idx, 'actions'] = 0
                except:
                    pass
        
    return dff


# Optimization Stop Loss

def objective_function(stop_loss, df_original, init_capital=2000, sell_value=2):

    df_stop_loss = stop_loss_simple(data=df_original, stop_loss=stop_loss, init_capital=init_capital, sell_value=sell_value)
    return_data, _ = get_backtesting(df=df_stop_loss)

    print(f"SEARCH THE BEST STOP LOSS SL: {stop_loss} RETURN: {return_data}")
    return -return_data

def optimize_stop_loss_simple(df_original, st_from=0.01, st_to=10):

    #method='Nelder-Mead'
    method='Powell'
    result = minimize(objective_function, x0=0, args=(df_original,), bounds=[(st_from, st_to)], method=method, options={'maxiter': 1000})
    best_stop_loss = result.x[0]
    best_return = -result.fun
    
    return best_stop_loss, best_return