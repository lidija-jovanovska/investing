from typing import List, Dict, Any, Optional
import pandas as pd
from src.api.api_utils import FinancialModelingPrepAPI
from src.filters import AVAILABLE_FILTERS, DEFAULT_FILTERS


class CompanyAnalyzer:
    def __init__(self, api_key: str):
        """Initialize the CompanyAnalyzer with API key."""
        self.api = FinancialModelingPrepAPI(api_key)
        self.n_quarters = 40  # 10 years * 4 quarters

    def get_company_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        company_profile = self.api.get_company_profile(ticker)
        income_statement = self.api.get_income_statement(ticker)[: self.n_quarters][
            ::-1
        ]

        return {"company_info": company_profile, "income_statement": income_statement}

    def analyze_company(
        self, company_name: str, filters: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a company using selected filters.

        Available filters:
        - gross_profit_ratio
        - sga_ratio
        - rd_ratio
        - depreciation_ratio
        - interest_ratio
        - net_income_ratio
        """
        company_data = self.get_company_data(company_name)
        if not company_data:
            return {"error": f"Company {company_name} not found"}

        if filters is None:
            filters = DEFAULT_FILTERS

        results = {
            "company_name": company_data["company_info"]["companyName"],
            "sector": company_data["company_info"]["sector"],
            "filters": {},
            "quarterly_data": {},
        }

        income_df = pd.DataFrame(company_data["income_statement"])

        for filter_name in filters:
            if filter_name not in AVAILABLE_FILTERS:
                continue

            filter_obj = AVAILABLE_FILTERS[filter_name]
            filter_result = filter_obj.get_result(income_df)
            results["filters"][filter_name] = filter_result

            # Add quarterly data for time series plotting
            if hasattr(filter_obj, "get_quarterly_data"):
                quarterly_data = filter_obj.get_quarterly_data(income_df)
                if quarterly_data is not None:
                    results["quarterly_data"][filter_name] = quarterly_data

        return results


def format_results(results: Dict[str, Any]) -> str:
    """Format analysis results for display."""
    if "error" in results:
        return results["error"]

    output = [f"Analysis for {results['company_name']} ({results['sector']})", "-" * 50]

    for name, filter_data in results["filters"].items():
        filter_name = name.replace("_", " ").title()
        value = f"{filter_data['value']:.2%}"

        line = f"{filter_name}: {value}"
        if "passes" in filter_data:
            status = "✓" if filter_data["passes"] else "✗"
            threshold = filter_data["threshold"]
            line += f" [{status}] (Threshold: {threshold})"

        output.append(line)
        output.append(f"  {filter_data['description']}")

    return "\n".join(output)


# Example usage:
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("API_KEY")

    if api_key is None:
        print("Error: API_KEY environment variable is not set")
        exit(1)

    analyzer = CompanyAnalyzer(api_key)

    # Example: Analyze Microsoft with all filters
    results = analyzer.analyze_company(
        "Microsoft",
        [
            "gross_profit_ratio",
            "sga_ratio",
            "rd_ratio",
            "depreciation_ratio",
            "interest_ratio",
            "net_income_ratio",
            "revenue_trend",
            "sga_consistency",
            "earnings_stability",
            "industry_interest",
        ],
    )

    print(format_results(results))
