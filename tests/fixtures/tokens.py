import boa
import pytest


@pytest.fixture()
def plain_tokens(deployer, decimals):
    tokens = []
    with boa.env.prank(deployer):
        for i, d in enumerate(decimals):
            tokens.append(boa.load("contracts/mocks/ERC20.vy", f"TKN{i}", f"TKN{i}", decimals[i]))
    return tokens


@pytest.fixture()
def oracle_tokens(deployer, decimals):
    tokens = []
    with boa.env.prank(deployer):
        tokens.append(
            boa.load(
                "contracts/mocks/ERC20Oracle.vy",
                "OTA",
                "OTA",
                18,
                1006470359024000000,
            )
        )
        tokens.append(
            boa.load(
                "contracts/mocks/ERC20Oracle.vy",
                "OTB",
                "OTB",
                18,
                1007580460035000000,
            )
        )
    return tokens


@pytest.fixture()
def rebase_tokens(deployer, decimals):
    tokens = []
    with boa.env.prank(deployer):
        for i, d in enumerate(decimals):
            tokens.append(boa.load("contracts/mocks/ERC20Rebasing.vy", f"OR_TKN{i}", f"OR_TKN{i}", decimals[i], True))
    return tokens


@pytest.fixture()
def pool_tokens(pool_token_types, plain_tokens, oracle_tokens, rebase_tokens):
    tokens = {0: plain_tokens, 1: oracle_tokens, 2: rebase_tokens}
    return [tokens[t][i] for i, t in enumerate(pool_token_types)]


# <---------------------   Metapool configuration   --------------------->
@pytest.fixture()
def metapool_token(metapool_token_type, plain_tokens, oracle_tokens, rebase_tokens):
    return {0: plain_tokens, 1: oracle_tokens, 2: rebase_tokens}[metapool_token_type][0]


@pytest.fixture()
def base_pool_decimals():
    return [18, 18, 18]


@pytest.fixture()
def base_pool_tokens(deployer, base_pool_decimals):
    with boa.env.prank(deployer):
        return [
            boa.load("contracts/mocks/ERC20.vy", c, c, base_pool_decimals[i])
            for i, c in enumerate(("DAI", "USDC", "USDT"))
        ]


@pytest.fixture()
def base_pool_lp_token(deployer):
    with boa.env.prank(deployer):
        return boa.load("contracts/mocks/CurveTokenV3.vy", "LP", "LP")


@pytest.fixture()
def underlying_tokens(metapool_token, base_pool_tokens, base_pool_lp_token):
    return [metapool_token, base_pool_lp_token, *base_pool_tokens]


# <---------------------   Gauge rewards  --------------------->
@pytest.fixture()
def coin_reward(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CR", "CR", 18)


@pytest.fixture()
def coin_reward_a(owner, mint_owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CRa", "CRa", 18)


@pytest.fixture()
def coin_reward_b(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CRb", "CRb", 18)


@pytest.fixture()
def coin_rewards_additional(owner):
    coins = []
    with boa.env.prank(owner):
        for i in range(8):
            coins.append(boa.load("contracts/mocks/ERC20.vy", f"CR{i}", f"CR{i}", 18))

    return coins
