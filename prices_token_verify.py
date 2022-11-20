#author: zhongyiio

import json
import requests


def _precheck(tokens: list[dict]):
    coins = _list_coinpaprika_coins()
    for token in tokens:
        if token[0] not in coins:
            return False, token
        coin = coins[token[0]]
        # AVAX, WAVAX, USDC.e, BTC.B...
        if coin["symbol"].upper() not in token[2].upper():
            return False, token
    return True, None


def _check_item(token: dict):
    coin = _get_coinpaprika_coin(token[0])
    if not coin:
        return False
    if "contract" in coin \
            and coin["contract"] \
            and token[3] \
            and coin["contract"].lower() == token[3].lower():
        return True

    # default True
    return True


# [
#     ...,
#     {
#         "id": "wbtc-wrapped-bitcoin",
#         "name": "Wrapped Bitcoin",
#         "symbol": "WBTC",
#         "rank": 21,
#         "is_new": false,
#         "is_active": true,
#         "type": "token"
#     },
#     ...
# ]
def _list_coinpaprika_coins():
    resp = requests.get("https://api.coinpaprika.com/v1/coins")
    if resp.status_code == 200:
        items = resp.json()
        data = {}
        for item in items:
            data[item["id"]] = item
        return data
    else:
        return {}


# {
#     "id": "wbtc-wrapped-bitcoin",
#     "name": "Wrapped Bitcoin",
#     "symbol": "WBTC",
#     "rank": 21,
#     "is_new": false,
#     "is_active": true,
#     "type": "token",
#     "contract": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
#     ...
# }
def _get_coinpaprika_coin(coin_id: str):
    resp = requests.get("https://api.coinpaprika.com/v1/coins/{}".format(coin_id))
    if resp.status_code == 404:
        return {}
    else:
        return resp.json()


def check_valid(tokens):
    # pre check
    pass_precheck, token = _precheck(tokens)
    # check item
    if not pass_precheck:
        raise Exception("Not pass precheck, token: {}".format(json.dumps(token)))
    for token in valid_tokens:
        valid = _check_item(token)
        if not valid:
            raise Exception("Token not valid, token: {}".format(json.dumps(token)))


if __name__ == '__main__':
    valid_tokens = [("frax-frax", "avalanche_c", "FRAX", "0xd24c2ad096400b6fbcd2ad8b24e7acbc21a1da64", 18),
                    ("fxs-frax-share", "avalanche_c", "FXS", "0x214db107654ff987ad859f34125307783fc8e387", 18),
                    ("avax-avalanche", "avalanche_c", "WAVAX", "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", 18),
                    ("dai-dai", "avalanche_c", "DAI", "0xd586e7f844cea2f87f50152665bcbc2c279d8d70", 18),
                    ("usdc-usd-coin", "avalanche_c", "USDC", "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e", 6),
                    ("usdt-tether", "avalanche_c", "USDT", "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7", 6),
                    ("wbtc-wrapped-bitcoin", "avalanche_c", "WBTC", "0x50b7545627a5162f82a992c33b87adc75187b218", 8),
                    ("bets-betswirl", "avalanche_c", "BETS", "0xc763f8570a48c4c00c80b76107cbe744dda67b79", 18),
                    ("thor-thor", "avalanche_c", "THOR", "0x8f47416cae600bccf9530e9f3aeaa06bdd1caa79", 18),
                    ("weth-weth", "avalanche_c", "WETH.e", "0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab", 18),
                    ("btcb-bitcoin-avalanche-bridged-btcb", "avalanche_c", "BTC.b", "0x152b9d0fdc40c096757f570a51e494bd4b943e50", 8),
                    ("woo-wootrade", "avalanche_c", "WOO.e", "0xabc9547b534519ff73921b1fba6e672b5f58d083", 18),
                    ("usdte-tether-usde", "avalanche_c", "USDT.e", "0xc7198437980c041c805a1edcba50c1ce5db95118", 6),
                    ("usdce-usd-coine", "avalanche_c", "USDC.e", "0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664", 6),
                    ("savax-benqi-liquid-staked-avax", "avalanche_c", "sAVAX", "0x2b2c81e08f1af8835a78bb2a90ae924ace0ea4be", 18),
                    ("mimatic-mimatic", "avalanche_c", "MIMATIC", "0x3b55e45fd6bd7d4724f5c47e0d1bcaedd059263e", 18),
                    ]

    check_valid(valid_tokens)

    not_valid_tokens = [("frax-frax-not-valid", "avalanche_c", "FRAX", "0xd24c2ad096400b6fbcd2ad8b24e7acbc21a1da64", 18),
                        ("fxs-frax-share", "avalanche_c", "FXS", "0x214db107654ff987ad859f34125307783fc8e387", 18),
                        ("avax-avalanche", "avalanche_c", "WAVAX", "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", 18),
                       ]
    # will raise exception here
    check_valid(not_valid_tokens)
