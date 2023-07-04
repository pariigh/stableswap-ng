import boa
import pytest


@pytest.fixture(scope="module")
def plain_tokens(deployer, decimals):
    tokens = []
    with boa.env.prank(deployer):
        for i, d in enumerate(decimals):
            tokens.append(boa.load("contracts/mocks/ERC20.vy", f"TKN{i}", f"TKN{i}", decimals[i]))
    return tokens


@pytest.fixture(scope="module")
def weth(deployer):
    with boa.env.prank(deployer):
        return boa.load("contracts/mocks/WETH.vy")


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def rebase_tokens(deployer, decimals):
    tokens = []
    with boa.env.prank(deployer):
        for i, d in enumerate(decimals):
            tokens.append(boa.load("contracts/mocks/ERC20Rebasing.vy", f"OR_TKN{i}", f"OR_TKN{i}", decimals[i], i != 0))
    return tokens


@pytest.fixture(scope="module")
def pool_tokens(pool_token_types, plain_tokens, weth, oracle_tokens, rebase_tokens):
    pool_tokens = []
    for i, t in enumerate(pool_token_types):
        if t == 0:
            pool_tokens.append(plain_tokens[i])
        elif t == 1:
            # Enforce eth as 0th token
            pool_tokens = [weth] + pool_tokens
        elif t == 2:
            pool_tokens.append(oracle_tokens[i])
        elif t == 3:
            pool_tokens.append(rebase_tokens[i])
        else:
            raise ValueError("Wrong pool token type")

    return pool_tokens


# <---------------------   Metapool configuration   --------------------->
@pytest.fixture(scope="module")
def base_pool_decimals():
    return [18, 6, 6]


@pytest.fixture(scope="module")
def base_pool_tokens(deployer, base_pool_decimals):
    tokens = []
    with boa.env.prank(deployer):
        tokens.append(boa.load("contracts/mocks/ERC20.vy", "DAI", "DAI", base_pool_decimals[0]))
        tokens.append(boa.load("contracts/mocks/ERC20.vy", "USDC", "USDC", base_pool_decimals[1]))
        tokens.append(boa.load("contracts/mocks/ERC20.vy", "USDT", "USDT", base_pool_decimals[2]))
    return tokens


@pytest.fixture(scope="module")
def base_pool_lp_token(deployer):
    with boa.env.prank(deployer):
        return boa.load("contracts/mocks/CurveTokenV3.vy", "LP", "LP")


@pytest.fixture(scope="module")
def underlying_tokens(
    pool_token_types, plain_tokens, weth, oracle_tokens, rebase_tokens, base_pool_tokens, base_pool_lp_token
):
    pool_tokens = []
    metapool_token_type = pool_token_types[0]
    if metapool_token_type == 0:
        pool_tokens.append(plain_tokens[0])
    elif metapool_token_type == 1:
        pool_tokens = pool_tokens.append(weth)
    elif metapool_token_type == 2:
        pool_tokens.append(oracle_tokens[0])
    elif metapool_token_type == 3:
        pool_tokens.append(rebase_tokens[0])
    else:
        raise ValueError("Wrong pool token type")

    return pool_tokens + [base_pool_lp_token.address, *[t.address for t in base_pool_tokens]]


# <---------------------   Gauge rewards  --------------------->
@pytest.fixture(scope="module")
def coin_reward(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CR", "CR", 18)


@pytest.fixture(scope="module")
def coin_reward_a(owner, mint_owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CRa", "CRa", 18)


@pytest.fixture(scope="module")
def coin_reward_b(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/mocks/ERC20.vy", "CRb", "CRb", 18)


@pytest.fixture(scope="module")
def coin_rewards_additional(owner):
    coins = []
    with boa.env.prank(owner):
        for i in range(8):
            coins.append(boa.load("contracts/mocks/ERC20.vy", f"CR{i}", f"CR{i}", 18))

    return coins
