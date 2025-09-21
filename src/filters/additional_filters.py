from dataclasses import dataclass
import numpy as np
import pandas as pd
from typing import Dict, Any
from .base import FinancialFilter


@dataclass
class RevenueTrendFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="revenue_trend",
            description="Measures revenue growth trend over time",
            threshold=0.0,
            comparison=">",
            threshold_text="Positive growth",
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        revenues = income_df["revenue"].to_numpy()
        # Calculate average quarterly growth rate
        growth_rates = np.diff(revenues) / revenues[:-1]
        return float(np.mean(growth_rates))


@dataclass
class OperatingMarginFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="operating_margin",
            description="Operating profit as percentage of revenue",
            threshold=0.15,  # 15% is generally considered good
            comparison=">=",
            threshold_text="≥ 15%",
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (income_df["operatingIncome"] / income_df["revenue"]).mean()


@dataclass
class SGAConsistencyFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="sga_consistency",
            description="Measures consistency of SGA expenses relative to gross profit",
            threshold=0.25,  # Max 25% standard deviation
            comparison="<=",
            threshold_text="≤ 25% variation",
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        sga_ratios = (
            income_df["sellingGeneralAndAdministrativeExpenses"]
            / income_df["grossProfit"]
        )
        # Return the coefficient of variation (std/mean)
        return sga_ratios.std() / sga_ratios.mean()


@dataclass
class IndustryAdjustedInterestFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="industry_interest_ratio",
            description="Interest to operating income ratio with industry-specific thresholds",
        )
        # Industry-specific thresholds based on index.md
        self.industry_thresholds = {
            "Consumer Goods": 0.15,  # 15% threshold
            "Financials": 0.30,  # 30% threshold
            "Default": 0.20,  # 20% default threshold
        }

    def get_result(self, income_df: pd.DataFrame) -> Dict[str, Any]:
        """Override get_result to handle industry-specific thresholds."""
        value = self.calculate(income_df)
        result = {"value": value, "description": self.description}

        # Note: We'll need to modify the CompanyAnalyzer to pass industry info
        # For now, we'll use the default threshold
        threshold = self.industry_thresholds["Default"]
        result["passes"] = value <= threshold
        result["threshold"] = f"≤ {threshold:.0%}"

        return result

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (income_df["interestExpense"] / income_df["operatingIncome"]).mean()
