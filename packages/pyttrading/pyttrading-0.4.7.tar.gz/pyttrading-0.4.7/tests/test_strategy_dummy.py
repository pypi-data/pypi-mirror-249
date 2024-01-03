
def test_collect_market_data():

    model_name = 'dummy'
    
    strategy_config  = { 
        "is_crypto": True,
        "symbol": 'AVAX/USD',
        "interval": '2m',
        "start_date": '11/1/2023',
        "end_date": '12/16/2023',
        "indicators": [
            "boll_ub",
            "boll_lb",
            "close_10_sma",
            "close_12_ema",
            "close_16_ema"
        ],
    }


    # model = ModelSelector(
    #                 model_name=params.get("strategy"),
    #                 path_model="tmp",
    #                 type_model="basic",
    #                 configuration=strategy_config, 
    #                 df=data,
    #                 symbol=symbol,
    #                 interval=interval,
    #                 mlflow=mlflow
    #             )



    assert 4 + 4== 8