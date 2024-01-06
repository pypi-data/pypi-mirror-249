from fetchfox.apis import coingeckocom


def usd(currency: str) -> float:
    return coingeckocom.usd(currency)


def ath_usd(currency: str) -> float:
    return coingeckocom.ath_usd(currency)
