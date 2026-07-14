from .momentum_strategy import MomentumStrategy
from .mean_reversion import MeanReversionStrategy
from .factor_strategy import FactorStrategy

STRATEGIES = {
    "momentum": MomentumStrategy,
    "mean_reversion": MeanReversionStrategy,
    "factor": FactorStrategy,
}
