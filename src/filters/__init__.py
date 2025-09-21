from .core_filters import (
    GrossProfitRatioFilter,
    SGARatioFilter,
    RDRatioFilter,
    DepreciationRatioFilter,
    InterestRatioFilter,
    NetIncomeRatioFilter,
)
from .additional_filters import (
    RevenueTrendFilter,
    OperatingMarginFilter,
    SGAConsistencyFilter,
    IndustryAdjustedInterestFilter,
)

# Dictionary of all available filters
AVAILABLE_FILTERS = {
    "gross_profit_ratio": GrossProfitRatioFilter(),
    "sga_ratio": SGARatioFilter(),
    "rd_ratio": RDRatioFilter(),
    "depreciation_ratio": DepreciationRatioFilter(),
    "interest_ratio": InterestRatioFilter(),
    "net_income_ratio": NetIncomeRatioFilter(),
    "revenue_trend": RevenueTrendFilter(),
    "operating_margin": OperatingMarginFilter(),
    "sga_consistency": SGAConsistencyFilter(),
    "industry_interest": IndustryAdjustedInterestFilter(),
}

# Default filters to use if none specified
DEFAULT_FILTERS = [
    "gross_profit_ratio",
    "sga_ratio",
    "rd_ratio",
    "depreciation_ratio",
    "interest_ratio",
    "net_income_ratio",
]
