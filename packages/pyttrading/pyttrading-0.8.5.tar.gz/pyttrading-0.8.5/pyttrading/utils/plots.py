
import matplotlib.pyplot as plt


def generate_market_value_plot(df_action_market, df_action_sl_market, best_sl):
    plt.figure(figsize=(8, 4)) 
    plt.plot(df_action_market['market_value'], label='Original')
    plt.plot(df_action_sl_market['market_value'], label=f'SL Opt {best_sl}') 
    plt.legend()
    plt.title('Market Value')
    plt.xlabel('Date') 
    plt.ylabel('Market Value') 
    plt.grid(True)
    plt.savefig('tmp/market_value_plot.png')
    plt.close()  # Close the figure to free memory

    return 'tmp/market_value_plot.png'

def generate_actions_plot(df_action_market):
    
    actions_1 = df_action_market[df_action_market['actions'] == 1]
    actions_2 = df_action_market[df_action_market['actions'] == 2]
    actions_2_sl = df_action_market[df_action_market['actions'] == 2]

    plt.figure(figsize=(10, 6))
    plt.scatter(actions_1.index, actions_1['open'], color='green', label='BUY')
    plt.scatter(actions_2.index, actions_2['open'], color='red', label='SELL')
    plt.scatter(actions_2_sl.index, actions_2_sl['open'], color='orange', label='StopLoss')
    plt.plot(df_action_market.index, df_action_market['close'], label='Close', linestyle='-')
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Scatter Plot for Actions 1 and 2 with Closing Line')
    plt.legend()
    plt.savefig('tmp/actions_plot.png')
    plt.close()  # Close the figure to free memory

    return 'tmp/actions_plot.png'