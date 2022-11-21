#contributors: zhongyiio, hosuke

import json
import requests
from typing import List, Any

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

def _precheck(tokens: List[dict]) -> (bool, List[Any]):
    coins = _list_coinpaprika_coins()
    pass_check = True
    failed_tokens = []
    for token in tokens:
        if token[0] not in coins:
            pass_check = False
            failed_tokens.append(token)
        else:
            coin = coins[token[0]]
            # AVAX, WAVAX, USDC.e, BTC.B...
            if coin["symbol"].upper() not in token[2].upper():
                pass_check = False
                failed_tokens.append(token)
    return pass_check, failed_tokens


def _check_item(token: dict) -> bool:
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
    pass_precheck, failed_tokens = _precheck(tokens)
    passed_tokens = []
    # check item
    if not pass_precheck:
        for token in failed_tokens:
            print("Not pass precheck, token: {}".format(json.dumps(token)))
    for token in tokens:
        if token not in failed_tokens:
            valid = _check_item(token)
            if not valid:
                print("Token not valid, token: {}".format(json.dumps(token)))
            else:
                passed_tokens.append(token)
    if len(passed_tokens) > 0:
        print("===== Token passed: =====")
    for token in passed_tokens:
        print("{}".format(json.dumps(token)))


if __name__ == '__main__':
    valid_tokens = [

        ### some seeds to pass
        ("frax-frax", "avalanche_c", "FRAX", "0xd24c2ad096400b6fbcd2ad8b24e7acbc21a1da64", 18),
        ("fxs-frax-share", "avalanche_c", "FXS", "0x214db107654ff987ad859f34125307783fc8e387", 18),
        ("avax-avalanche", "avalanche_c", "WAVAX", "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", 18),
        ("dai-dai", "avalanche_c", "DAI", "0xd586e7f844cea2f87f50152665bcbc2c279d8d70", 18),
        ("usdc-usd-coin", "avalanche_c", "USDC", "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e", 6),

        ### test cases starts here
        ("tusd-trueusd", "avalanche_c", "TUSD", "0x1c20e891bab6b1727d14da358fae2984ed9b59eb", 18),
        ("usdd-usdd", "avalanche_c", "USDD", "0xcf799767d366d789e8b446981c2d578e241fa25c", 18),
        ("knc-kyber-network", "avalanche_c", "KNC", "0x39fc9e94caeacb435842fadedecb783589f50f5f", 18),
        ("spell-spell-token", "avalanche_c", "SPELL", "0xce1bffbd5374dac86a2893119683f4911a2f7814", 18),
        ("orbs-orbs", "avalanche_c", "ORBS", "0x340fe1d898eccaad394e2ba0fc1f93d27c7b717a", 18),
        ("sure-insure", "avalanche_c", "SURE", "0x5fc17416925789e0852fbfcd81c490ca4abc51f9", 18),
        ("joe-trader-joe", "avalanche_c", "JOE", "0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd", 18),
        ("qi-qiswap", "avalanche_c", "QI", "0x8729438eb15e2c8b576fcc6aecda6a148776c0f5", 18),
        ("bifi-beefyfinance", "avalanche_c", "BIFI", "0xd6070ae98b8069de6b494332d1a1a81b6179d960", 18),
        ("jade-jade-protocol", "avalanche_c", "JADE", "0x80b010450fdaf6a3f8df033ee296e92751d603b3", 18),
        ("rai-rai-reflex-index", "avalanche_c", "RAI", "0x97cd1cfe2ed5712660bb6c14053c0ecb031bff7d", 18),
        ("wxt-wirex-token", "avalanche_c", "WXT", "0xfcde4a87b8b6fa58326bb462882f1778158b02f1", 18),
        ("walbt-wrapped-allianceblock-token", "avalanche_c", "WALBT", "0x9e037de681cafa6e661e6108ed9c2bd1aa567ecd", 18),
        ("uncx-unicrypt", "avalanche_c", "UNCX", "0x3b9e3b5c616a1a038fdc190758bbe9bab6c7a857", 18),
        ("pendle-pendle", "avalanche_c", "PENDLE", "0xfb98b335551a418cd0737375a2ea0ded62ea213b", 18),
        ("png-pangolin", "avalanche_c", "PNG", "0x60781c2586d68229fde47564546784ab3faca982", 18),
        ("ooe-openocean", "avalanche_c", "OOE", "0x0ebd9537a25f56713e34c45b38f421a1e7191469", 18),
        ("dyp-defi-yield-protocol", "avalanche_c", "DYP", "0x961c8c0b1aad0c0b10a51fef6a867e3091bcef17", 18),
        ("insur-insurace", "avalanche_c", "INSUR", "0x544c42fbb96b39b21df61cf322b5edc285ee7429", 18),
        ("nftd-nftrade", "avalanche_c", "NFTD", "0x9e3ca00f2d4a9e5d4f0add0900de5f15050812cf", 18),
        ("frm-ferrum-network", "avalanche_c", "FRM", "0xe5caef4af8780e59df925470b050fb23c43ca68c", 18),
        ("uncl-uncl", "avalanche_c", "UNCL", "0x7d86f1eaff29f076576b2ff09ce3bcc7533fd2c5", 18),
        ("oddz-oddz", "avalanche_c", "ODDZ", "0xb0a6e056b587d0a85640b39b1cb44086f7a26a1e", 18),
        ("klo-kalao", "avalanche_c", "KLO", "0xb27c8941a7df8958a1778c0259f76d1f8b711c35", 18),
        ("acr-acreage-coin", "avalanche_c", "ACRE", "0x00ee200df31b869a321b10400da10b561f3ee60d", 18),
        ("roobee-roobee", "avalanche_c", "ROOBEE", "0x4036f3d9c45a20f44f0b8b85dd6ca33005ff9654", 18),
        ("spo-spores-network", "avalanche_c", "SPORE", "0x6e7f5c0b9f4432716bdd0a77a3601291b9d9e985", 9),
        ("ethm-ethereum-meta", "avalanche_c", "ETHM", "0x55b1a124c04a54eefdefe5fa2ef5f852fb5f2f26", 18),
        ("vso-verso", "avalanche_c", "VSO", "0x846d50248baf8b7ceaa9d9b53bfd12d7d7fbb25a", 18),
        ("dfiat-defiato-via-chainportio", "avalanche_c", "DFIAT", "0xafe3d2a31231230875dee1fa1eef14a412443d22", 18),
        ("ncash-nucleus-vision", "avalanche_c", "ncash", "0xc69eba65e87889f0805db717af06797055a0ba07", 18),
        ("melt-defrost-finance", "avalanche_c", "MELT", "0x47eb6f7525c1aa999fbc9ee92715f5231eb1241d", 18),
        ("boofi-boo-finance", "avalanche_c", "BOOFI", "0xb00f1ad977a949a3ccc389ca1d1282a2946963b0", 18),
        ("more-buymore", "avalanche_c", "MORE", "0xd9d90f882cddd6063959a9d837b05cb748718a05", 18),
        ("atl-atlantis-loans", "avalanche_c", "ATL", "0x90fbe9dfe76f6ef971c7a297641dfa397099a13e", 18),
        ("gaj-gaj-finance", "avalanche_c", "GAJ", "0x595c8481c48894771ce8fade54ac6bf59093f9e8", 18),
        ("avxt-avaxtars-token", "avalanche_c", "AVXT", "0x397bbd6a0e41bdf4c3f971731e180db8ad06ebc1", 6),
        ("gohm-governance-ohm", "avalanche_c", "gOHM", "0x321e7092a180bb43555132ec53aaa65a5bf84251", 18),
        ("yak-yield-yak", "avalanche_c", "YAK", "0x59414b3089ce2af0010e7523dea7e2b35d776ec7", 18),
        ("wshare-frozen-walrus-share", "avalanche_c", "WSHARE", "0xe6d1afea0b76c8f51024683dd27fa446ddaf34b6", 18),
        ("time-chronotech", "avalanche_c", "TIME", "0xb54f16fb19478766a268f172c9480f8da1a7c9c3", 9),
        ("kitty-kitty-inu", "avalanche_c", "KITTY", "0x788ae3b5d153d49f8db649aacba1857f744b739e", 18),
        ("cat-cat-token", "avalanche_c", "CAT", "0x094bfac9894d2a2a35771d0bd6d2447689190f32", 18),
        ("syn-synapse", "avalanche_c", "SYN", "0x1f1e7c893855525b303f99bdf5c3c05be09ca251", 18),
        ("mim-magic-internet-money", "avalanche_c", "MIM", "0x130966628846bfd36ff31a822705796e8cb8c18d", 18),
        ("cream-cream", "avalanche_c", "CREAM", "0xae21d31a6494829a9e4b2b291f4984aae8121757", 18),
        ("piggy-piggy", "avalanche_c", "PIGGY", "0x1a877b68bda77d78eea607443ccde667b31b0cdf", 18),
        ("pshare-partial-share", "avalanche_c", "PSHARE", "0xa5e2cfe48fe8c4abd682ca2b10fcaafe34b8774c", 18),
        ("xava-avalaunch", "avalanche_c", "XAVA", "0xd1c3f94de7e5b45fa4edbba472491a9f4b166fc4", 18),
        ("start-bscstarter", "avalanche_c", "START", "0xf44fb887334fa17d2c5c0f970b5d320ab53ed557", 18),
        ("tryb-bilira", "avalanche_c", "TRYB", "0x564a341df6c126f90cf3ecb92120fd7190acb401", 6),
        ("mfi-marginswap", "avalanche_c", "MFI", "0x9fda7ceec4c18008096c2fe2b85f05dc300f94d0", 18),
        ("ave-avaware", "avalanche_c", "AVE", "0x78ea17559b3d2cf85a7f9c2c704eda119db5e6de", 18),
        ("a4-a4-finance", "avalanche_c", "A4", "0x9767203e89dcd34851240b3919d4900d3e5069f1", 6),
        ("pefi-plant-empires", "avalanche_c", "PEFI", "0xe896cdeaac9615145c0ca09c8cd5c25bced6384c", 18),
        ("hon-heroes-of-nft", "avalanche_c", "HON", "0xed2b42d3c9c6e97e11755bb37df29b6375ede3eb", 18),
        ("oh-oh-finance", "avalanche_c", "OH", "0x937e077abaea52d3abf879c9b9d3f2ebd15baa21", 18),
        ("teddy-teddy-cash", "avalanche_c", "TEDDY", "0x094bd7b2d99711a1486fb94d4395801c6d0fddcc", 18),
        ("chro-chronicum", "avalanche_c", "CHRO", "0xbf1230bb63bfd7f5d628ab7b543bcefa8a24b81b", 18),
        ("hct-hurricane-token", "avalanche_c", "HCT", "0x45c13620b55c35a5f539d26e88247011eb10fdbd", 18),
        ("orbit-europa", "avalanche_c", "ORBIT", "0x4bf5cd1ac6fff12e88aedd3c70eb4148f90f8894", 18),
        ("jpeg-jpeg39d", "avalanche_c", "JPEG", "0x6241af3817db48a7f9e19fd9446d78e50936d275", 18),
        ("cnr-canary", "avalanche_c", "CNR", "0x8d88e48465f30acfb8dac0b3e35c9d6d7d36abaf", 18),
        ("bpt-blackpool-token", "avalanche_c", "BPT", "0x1111111111182587795ef1098ac7da81a108c97a", 18),
        ("vee-blockv", "avalanche_c", "VEE", "0x3709e8615e02c15b096f8a9b460ccb8ca8194e86", 18),
        ("blzz-blizz-finance", "avalanche_c", "BLZZ", "0x0f34919404a290e71fc6a510cb4a6acb8d764b24", 18),
        ("smrt-solminter", "avalanche_c", "SMRT", "0xcc2f1d827b18321254223df4e84de399d9ff116c", 18),
        ("tractor-tractor-joe", "avalanche_c", "TRACTOR", "0x542fa0b261503333b90fe60c78f2beed16b7b7fd", 9),
        ("xcrs-novaxcrystal", "avalanche_c", "XCRS", "0x70b4ae8eb7bd572fc0eb244cd8021066b3ce7ee4", 18),
        ("xslr-novaxsolar", "avalanche_c", "XSLR", "0xe6ee049183b474ecf7704da3f6f555a1dcaf240f", 18),
        ("smrtr-smartercoin", "avalanche_c", "SMRTr", "0x6d923f688c7ff287dc3a5943caeefc994f97b290", 18),
        ("husky-husky-avax", "avalanche_c", "HUSKY", "0x65378b697853568da9ff8eab60c13e1ee9f4a654", 18),
        ("alpha-alpha-labz", "avalanche_c", "$ALPHA", "0x325a98f258a5732c7b06555603f6af5bc1c17f0a", 9),
        ("bavax-baby-avax", "avalanche_c", "bAVAX", "0xb2ac04b71888e17aa2c5102cf3d0215467d74100", 18),
        ("busdc-busdcash", "avalanche_c", "bUSDC", "0xc25ff1af397b76252d6975b4d7649b35c0e60f69", 6),
        ("blight-blight", "avalanche_c", "BLIGHT", "0x350b3ff32ab1b6beabec41abcebff682e0f37a3b", 9),
        ("gmx-gmx", "avalanche_c", "GMX", "0x62edc0692bd897d2295872a9ffcac5425011c661", 18),
        ("sushi-sushi", "avalanche_c", "SUSHI", "0x39cf1bd5f15fb22ec3d9ff86b0727afc203427cc", 18),
        ("tsd-teddy-dollar", "avalanche_c", "TSD", "0x4fbf0429599460d327bd5f55625e30e4fc066095", 18),
        ("busd-binance-usd", "avalanche_c", "BUSD", "0x9c9e5fd8bbc25984b178fdce6117defa39d2db39", 18),
        ("feed-feeder-finance", "avalanche_c", "FEED", "0xab592d197acc575d16c3346f4eb70c703f308d1e", 18),
        ("frt-fertilizer", "avalanche_c", "FERT", "0x9c846d808a41328a209e235b5e3c4e626dab169e", 18),
        ("vpnd-vapornodes", "avalanche_c", "VPND", "0x83a283641c6b4df383bcddf807193284c84c5342", 18),
        ("dcar-dragon-crypto-argenti", "avalanche_c", "DCAR", "0x250bdca7d1845cd543bb55e7d82dca24d48e9f0f", 18),
        ("egg-chikn-egg", "avalanche_c", "EGG", "0x7761e2338b35bceb6bda6ce477ef012bde7ae611", 18),
        ("ptp-platypus-finance", "avalanche_c", "PTP", "0x22d4002028f537599be9f666d1c4fa138522f9c8", 18),
        ("stg-stargatetoken", "avalanche_c", "STG", "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590", 18),
        ("pizza-pizza-game", "avalanche_c", "PIZZA", "0x6121191018baf067c6dc6b18d42329447a164f05", 18),
        ("polar-polar", "avalanche_c", "POLAR", "0x6c1c0319d8ddcb0ffe1a68c5b3829fd361587db4", 18),
        ("cra-crabada", "avalanche_c", "CRA", "0xa32608e873f9ddef944b24798db69d80bbb4d1ed", 18),
        ("bnb-binance-coin", "avalanche_c", "BNB", "0x264c1383ea520f73dd837f915ef3a732e204a493", 18),
        ("weth-weth", "avalanche_c", "WETH", "0x8b82a291f83ca07af22120aba21632088fc92931", 18),
        ("lost-lost-world", "avalanche_c", "LOST", "0x449674b82f05d498e126dd6615a1057a9c088f2c", 18),
        ("sol-solana", "avalanche_c", "SOL", "0xfe6b19286885a4f7f55adad09c3cd1f906d2478f", 9),
        ("zeus-zeus-finance", "avalanche_c", "ZEUS", "0x8c3633ee619a42d3755327c2524e4d108838c47f", 18),
        ("rux-runblox", "avalanche_c", "RUX", "0xa1afcc973d44ce1c65a21d9e644cb82489d26503", 18),
        ("wmatic-wrapped-matic-wormhole", "avalanche_c", "WMATIC", "0xf2f13f0b7008ab2fa4a2418f4ccc3684e49d20eb", 18),
        ("acs-acryptos", "avalanche_c", "ACS", "0x18fc6360e83fe91404d47ea4400a221dfbbacf06", 18),
        ("mask-mask-network", "avalanche_c", "MASK", "0x0db995f93dd05ae966ab4c57e43b443a9b18a532", 18),
        ("vtx-vector-finance", "avalanche_c", "VTX", "0x5817d4f0b62a59b17f75207da1848c2ce75e7af4", 18),
        ("grape-grape-finance", "avalanche_c", "GRAPE", "0x5541d83efad1f281571b343977648b75d95cdac2", 18),
        ("fdt-fiat-dao-token", "avalanche_c", "FDT", "0x4e51e67f1c6da0f9ba52fe27a6e9a9dbd36ac479", 18),
        ("kgc-kingdom-quest", "avalanche_c", "KGC", "0x54a77f27d2346c3a8f5b43a501434f0f21f33e3c", 18),
        ("biofi-biofi", "avalanche_c", "BioFi", "0x9366d30feba284e62900f6295bc28c9906f33172", 6),
        ("xeta-xeta", "avalanche_c", "XETA", "0x31c994ac062c1970c086260bc61babb708643fac", 18),
        ("alot-dexalot", "avalanche_c", "ALOT", "0x093783055f9047c2bff99c4e414501f8a147bc69", 18),
        ("yeti-yearn-ecosystem-token-index", "avalanche_c", "YETI", "0x77777777777d4554c39223c354a05825b2e8faa3", 18),
        ("isa-islander", "avalanche_c", "ISA", "0x3eefb18003d033661f84e48360ebecd181a84709", 18),
        ("ethw-ethereum-pow", "avalanche_c", "ETHW", "0x08f9492ee68594fcc356f9d91af93d8e4f8c9f33", 18),
        ("slime-squishiverse", "avalanche_c", "SLIME", "0x5a15bdcf9a3a8e799fa4381e666466a516f2d9c8", 18),
        ("brise-bitrise-token", "avalanche_c", "BRISE", "0xb6c353d519d7721b18c813130625d04de4f53580", 18),
        ("dcau-dragon-crypto-aurum", "avalanche_c", "DCAU", "0x100cc3a819dd3e8573fd2e46d1e66ee866068f30", 18),
        ("pln-plearn-token", "avalanche_c", "PLN", "0x7b2b702706d9b361dfe3f00bd138c0cfda7fb2cf", 18),
        ("luna-luna-wormhole", "avalanche_c", "LUNA", "0x70928e5b188def72817b7775f0bf6325968e563b", 6),
        ("3ull-playa3ull-games", "avalanche_c", "3ULL", "0x9e15f045e44ea5a80e7fbc193a35287712cc5569", 18),



        ### some more seeds to pass
        ("btcb-bitcoin-avalanche-bridged-btcb", "avalanche_c", "BTC.b", "0x152b9d0fdc40c096757f570a51e494bd4b943e50", 8),
        ("woo-wootrade", "avalanche_c", "WOO.e", "0xabc9547b534519ff73921b1fba6e672b5f58d083", 18)
            ]

    check_valid(valid_tokens)
