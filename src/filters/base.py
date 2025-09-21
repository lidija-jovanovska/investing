from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import pandas as pd


@dataclass
class Classification:
    """Class to represent a classification range for a metric."""

    min_value: Optional[float]
    max_value: Optional[float]
    description: str

    def contains(self, value: float) -> bool:
        """Check if value falls within this classification range."""
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True


@dataclass
class FinancialFilter:
    """Base class for financial metric filters."""

    name: str
    description: str
    threshold: Optional[float] = None
    threshold_text: Optional[str] = None
    comparison: Optional[str] = None
    classifications: List[Classification] = field(default_factory=list)
    guidelines: Optional[str] = None

    def calculate(self, income_df: pd.DataFrame) -> float:
        """Calculate the metric value. Must be implemented by subclasses."""
        raise NotImplementedError

    def passes_threshold(self, value: float) -> bool:
        """Check if the value passes the threshold."""
        if self.threshold is None or self.comparison is None:
            return True

        if self.comparison == ">=":
            return value >= self.threshold
        elif self.comparison == "<=":
            return value <= self.threshold
        elif self.comparison == ">":
            return value > self.threshold
        elif self.comparison == "<":
            return value < self.threshold
        return True

    def get_classification(self, value: float) -> Optional[str]:
        """Get the classification description for a given value."""
        for classification in self.classifications:
            if classification.contains(value):
                return classification.description
        return None
        """Get the classification description for a given value."""
        for classification in self.classifications:
            if classification.contains(value):
                return classification.description
        return None

    def get_quarterly_data(self, income_df: pd.DataFrame) -> Optional[pd.Series]:
        """Get quarterly time series data for the metric.

        Args:
            income_df: DataFrame of quarterly income statements

        Returns:
            A pandas Series with the quarterly metric values
        """
        try:
            # Calculate metric for each quarter
            values = []
            # Create fiscal quarter labels
            quarters = []
            for _, quarter in income_df.iterrows():
                values.append(self.calculate(pd.DataFrame([quarter])))
                fiscal_year = quarter.get("calendarYear", "")
                period = quarter.get("period", "")
                if fiscal_year and period:
                    quarters.append(f"{fiscal_year}-{period}")
                else:
                    quarters.append(None)
            return pd.Series(values, index=quarters)
        except Exception:
            return None

    def get_result(self, income_df: pd.DataFrame) -> Dict[str, Any]:
        """Get the analysis result for this filter."""
        value = self.calculate(income_df)
        result = {"value": value, "description": self.description}

        if self.threshold is not None:
            result["passes"] = self.passes_threshold(value)
            result["threshold"] = (
                self.threshold_text or f"{self.comparison} {self.threshold:.0%}"
            )

        if self.classifications:
            result["classification"] = self.get_classification(value)

        if self.guidelines:
            result["guidelines"] = self.guidelines

        return result
