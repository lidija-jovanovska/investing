from dataclasses import dataclass
import pandas as pd
from .base import FinancialFilter, Classification


@dataclass
class GrossProfitRatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="gross_profit_ratio",
            description="Indicates pricing power and efficiency",
            threshold=0.4,
            comparison=">=",
            threshold_text="≥ 40%",
            guidelines="""Average over the last 10 years to ensure durable competitive advantage.
            Companies with excellent long-term economics have consistently higher gross profit margins.
            A company's durable advantage allows pricing well above cost of goods sold.""",
            classifications=[
                Classification(0.4, None, "Durable competitive advantage"),
                Classification(0.2, 0.4, "Highly-competitive industry"),
                Classification(None, 0.2, "Fiercely competitive industry"),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return income_df["grossProfitRatio"].mean()


@dataclass
class SGARatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="sga_ratio",
            description="Lower ratio indicates better operational efficiency",
            threshold=0.3,
            comparison="<=",
            threshold_text="≤ 30%",
            guidelines="""Look for consistency. Wild oscillations can indicate problems with adapting to falling sales.
            Some industries (e.g., Consumer) naturally have higher ratios due to advertising needs.
            Example: Coca Cola spends ~60% on SGA to maintain market relevance.""",
            classifications=[
                Classification(None, 0.3, "Excellent operational efficiency"),
                Classification(0.3, 0.8, "Normal range (varies by industry)"),
                Classification(0.8, None, "High overhead costs"),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (
            income_df["sellingGeneralAndAdministrativeExpenses"]
            / income_df["grossProfit"]
        ).mean()


@dataclass
class RDRatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="rd_ratio",
            description="R&D investment relative to gross profit",
            guidelines="""Buffett's view: Companies that spend heavily on R&D have inherent risk in their competitive advantage.
            High R&D often leads to increased costs in other areas (e.g., SGA for new product launches).
            Particularly important in pharmaceutical and tech sectors.""",
            classifications=[
                Classification(None, 0.1, "Low R&D dependency - more stable advantage"),
                Classification(0.1, 0.2, "Moderate R&D investment"),
                Classification(
                    0.2,
                    None,
                    "Heavy R&D investment - potential risk to long-term economics",
                ),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (
            income_df["researchAndDevelopmentExpenses"] / income_df["grossProfit"]
        ).mean()


@dataclass
class DepreciationRatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="depreciation_ratio",
            description="Lower ratio suggests less capital-intensive business",
            threshold=0.1,
            comparison="<=",
            threshold_text="≤ 10%",
            guidelines="""Companies with durable competitive advantages usually have low D&A costs.
            Exceptions: capital-intensive industries (utilities, airlines, telecoms) can have high D&A but still maintain moats.
            Best advantages come from scalable, asset-light sources (brands, network effects, software, proprietary platforms).""",
            classifications=[
                Classification(
                    None, 0.1, "Asset-light business with potential durable advantage"
                ),
                Classification(0.1, 0.2, "Moderate capital intensity"),
                Classification(
                    0.2, None, "Capital-intensive business (check industry context)"
                ),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (
            income_df["depreciationAndAmortization"] / income_df["grossProfit"]
        ).mean()


@dataclass
class InterestRatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="interest_ratio",
            description="Lower ratio indicates less debt burden",
            guidelines="""Varies significantly by industry: consumer goods (<15%), financial services (~30%).
            High interest expenses can indicate either fierce competition forcing debt-funded growth,
            or a leveraged buyout situation. Watch for dramatic increases over time.""",
            classifications=[
                Classification(
                    None, 0.15, "Strong position (typical for consumer goods)"
                ),
                Classification(0.15, 0.3, "Moderate interest burden"),
                Classification(
                    0.3, 0.7, "High interest burden (typical for financial services)"
                ),
                Classification(
                    0.7, None, "Warning: Very high interest burden (risk of distress)"
                ),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return (income_df["interestExpense"] / income_df["operatingIncome"]).mean()


@dataclass
class NetIncomeRatioFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="net_income_ratio",
            description="Net earnings relative to gross profit",
            threshold=0.2,
            comparison=">",
            threshold_text="> 20%",
            guidelines="""Higher ratio compared to competitors suggests durable advantage.
            Be cautious with financial sector - very high ratios might indicate excessive risk-taking.
            Look for historical upward trend in earnings.
            Note: Buffett prefers net earnings over EPS (which can be manipulated via share buybacks).""",
            classifications=[
                Classification(0.2, None, "Durable competitive advantage"),
                Classification(0.1, 0.2, "Gray area - requires further analysis"),
                Classification(
                    None, 0.1, "Competitive industry without clear advantage"
                ),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        return income_df["netIncomeRatio"].mean()


@dataclass
class OperatingPLFilter(FinancialFilter):
    def __init__(self):
        super().__init__(
            name="operating_pl_ratio",
            description="Operating Profit/Loss relative to gross profit",
            threshold=0.3,
            comparison=">=",
            threshold_text="≥ 30%",
            guidelines="""Operating P/L measures operational efficiency by showing how much profit remains after all operating expenses.
            Higher ratios indicate better cost management and operational efficiency.
            Watch for:
            - Consistent positive operating margins
            - Stable or improving trends
            - Comparison with industry averages""",
            classifications=[
                Classification(0.3, None, "Strong operational efficiency"),
                Classification(0.15, 0.3, "Moderate operational efficiency"),
                Classification(0, 0.15, "Low operational efficiency"),
                Classification(None, 0, "Operating at a loss - concerning"),
            ],
        )

    def calculate(self, income_df: pd.DataFrame) -> float:
        # Operating P/L = Gross Profit - Operating Expenses
        # Operating expenses include R&D, SGA, D&A, and other operating expenses
        operating_pl = income_df["grossProfit"] - income_df["operatingExpenses"]
        return (operating_pl / income_df["grossProfit"]).mean()
