"""Utility functions for extracting and summarizing quarterly metrics from
income statement DataFrames used in the Buffett analysis notebook.

Each function accepts the income_statements DataFrame (rows are companies,
each cell is a list/sequence of quarterly dictionaries) and the corresponding
`snp_data` DataFrame so company names/sectors can be resolved.

These helpers are intentionally small and well-documented so they can be
reused from notebooks or other scripts.
"""

from typing import Union, Tuple, Dict
import pandas as pd


def compute_quarterly_metric_by_key(
    income_statements_df: pd.DataFrame,
    snp_data: pd.DataFrame,
    key: Union[str, Tuple[str, str]],
    n_quarters: int = 40,
) -> pd.DataFrame:
    """Compute a quarterly metric DataFrame for all companies.

    Args:
        income_statements_df: DataFrame where each row is a company and each
            cell contains a sequence (list) of quarterly statement dicts.
        snp_data: DataFrame with matching row ordering that contains at least
            a ``name`` column used for column labels.
        key: Either a string key to extract directly from each quarterly dict
            (e.g. "grossProfitRatio" or "incomeBeforeTax"), or a tuple of
            two keys (numerator_key, denominator_key) to compute a ratio.
        n_quarters: Number of most-recent quarters to include (default 40).

    Returns:
        DataFrame with shape (n_quarters, n_companies). Columns are company
        names (from `snp_data['name']`) and rows represent quarters (oldest -> newest).

    Notes:
        - If a quarterly entry is None it is skipped and later padded with
          leading None values so all series are length ``n_quarters``.
        - Division by zero results in a 0
    """
    metrics: Dict[str, list] = {}

    for i, row in income_statements_df.iterrows():
        company = snp_data.iloc[i]["name"]
        vals = []
        for quarter in row.values[:n_quarters]:
            if quarter is None:
                continue
            if isinstance(key, str):
                vals.append(quarter.get(key))
            else:
                # ratio case: (num_key, den_key)
                num_key, den_key = key
                num = quarter.get(num_key)
                den = quarter.get(den_key)
                try:
                    if den == 0:
                        vals.append(0)
                    else:
                        vals.append(None if den is None else (num / den))
                except Exception:
                    vals.append(0)

        # pad with leading Nones if the company has fewer than n_quarters
        if len(vals) < n_quarters:
            vals = [None] * (n_quarters - len(vals)) + vals

        metrics[company] = vals

    df = pd.DataFrame(metrics)
    # Sort by company name
    df = df[sorted(df.columns)]
    return df


def analyze_by_sector(
    metric_df: pd.DataFrame,
    snp_data: pd.DataFrame,
    sector_key: str = "sector",
    include_companies: bool = False,
) -> pd.DataFrame:
    """Build a sector-level summary DataFrame for the given metric.

    Args:
        metric_df: DataFrame containing the metric values, with companies as columns
        snp_data: DataFrame containing company metadata (must have 'name' and sector_key columns)
        sector_key: Column in snp_data to use for grouping ('sector', 'subSector', etc)
        include_companies: If True, adds a column listing all companies in each sector

    Returns:
        DataFrame with sector-level statistics including median values and counts.
        If include_companies is True, also includes a column listing all companies
        in each sector.
    """
    # compute means per company
    means = metric_df.mean(skipna=True)

    # map companies to their sectors
    name_to_sector = pd.Series(
        snp_data[sector_key].values, index=snp_data["name"]
    ).to_dict()

    # build company-level summary
    summary = pd.DataFrame({"company": means.index, "metric_mean": means.values})
    summary["sector"] = summary["company"].map(name_to_sector)

    # compute sector-level metrics
    sector_summary = pd.DataFrame(
        summary.groupby("sector")["metric_mean"].median().sort_values(ascending=False)
    )
    sector_summary["num_companies"] = summary["sector"].value_counts()

    if include_companies:
        sector_summary["companies"] = summary.groupby("sector")["company"].apply(
            lambda x: ", ".join(x)
        )

    return sector_summary


def plot_metric(metric_df: pd.DataFrame, title: str, y_label: str):
    """Small wrapper that returns a plotly express line figure for the metric.

    Keeps the notebook plotting calls concise while allowing a single
    import for plotting.
    """
    import plotly.express as px

    fig = px.line(
        metric_df,
        title=title,
        labels={"value": y_label, "index": "Quarter", "variable": "Company"},
    )
    return fig


__all__ = [
    "compute_quarterly_metric_by_key",
    "analyze_by_sector",
    "plot_metric",
]
