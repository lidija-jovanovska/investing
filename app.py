import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from src.analysis.company_analyzer import CompanyAnalyzer
from src.filters import AVAILABLE_FILTERS, DEFAULT_FILTERS

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

if api_key is None:
    st.error("Error: API_KEY environment variable is not set")
    st.stop()

# Initialize the analyzer
analyzer = CompanyAnalyzer(api_key)


def convert_results_to_df(results):
    """Convert analysis results to a pandas DataFrame."""
    if "error" in results:
        return None

    data = []
    for name, filter_data in results["filters"].items():
        row = {
            "Metric": name.replace("_", " ").title(),
            "Value": f"{filter_data['value']:.2%}",
        }
        if "passes" in filter_data:
            row["Passes Threshold"] = "✓" if filter_data["passes"] else "✗"
            row["Threshold"] = filter_data["threshold"]
        if "classification" in filter_data:
            row["Classification"] = filter_data["classification"]
        data.append(row)

    return pd.DataFrame(data)


# Set up the Streamlit page
st.set_page_config(
    page_title="Company Financial Analysis", page_icon="📊", layout="wide"
)

# Title and description
st.title("Company Financial Analysis")
st.markdown("""
This tool analyzes companies using various financial metrics based on Warren Buffett's principles.
Enter a company name or ticker and select the metrics you want to analyze.
""")

# Input for company name/ticker
company_input = st.text_input(
    "Enter Company Name or Ticker",
    help="Enter the name of a company in the S&P 500 (e.g., 'Microsoft' or 'MSFT')",
)

# Filter selection
st.subheader("Select Analysis Metrics")

# Create columns for better layout
col1, col2 = st.columns(2)

# Filter selection with tooltips
selected_filters = st.multiselect(
    "Choose metrics to analyze:",
    options=list(AVAILABLE_FILTERS.keys()),
    default=DEFAULT_FILTERS,
    format_func=lambda x: x.replace("_", " ").title(),
    help="Select one or more metrics to analyze. Hover over the options to see descriptions.",
)

# Show descriptions of selected filters
if selected_filters:
    st.markdown("### Selected Metrics Details")

    # Use columns for better organization
    for filter_name in selected_filters:
        filter_obj = AVAILABLE_FILTERS[filter_name]

        # Create an expander for each metric
        with st.expander(f"📊 {filter_name.replace('_', ' ').title()}", expanded=False):
            # Main description
            st.markdown(f"**Description**: {filter_obj.description}")

            # Threshold information if available
            if hasattr(filter_obj, "threshold") and filter_obj.threshold is not None:
                st.markdown(f"**Target Threshold**: {filter_obj.threshold_text}")

            # Guidelines with better formatting
            if filter_obj.guidelines:
                st.markdown("**Guidelines**:")
                for guideline in filter_obj.guidelines.split("\n"):
                    if guideline.strip():
                        st.markdown(f"- {guideline.strip()}")

            # Classifications if available
            if hasattr(filter_obj, "classifications") and filter_obj.classifications:
                st.markdown("**Classifications**:")
                for classification in filter_obj.classifications:
                    # Format the range text
                    if classification.min_value is None:
                        range_text = f"< {classification.max_value:.0%}"
                    elif classification.max_value is None:
                        range_text = f"> {classification.min_value:.0%}"
                    else:
                        range_text = f"{classification.min_value:.0%} - {classification.max_value:.0%}"

                    st.markdown(f"- {range_text}: {classification.description}")

# Analyze button
if st.button("Analyze Company") and company_input:
    with st.spinner("Analyzing company..."):
        # Get analysis results
        results = analyzer.analyze_company(company_input, selected_filters)

        if "error" in results:
            st.error(results["error"])
        else:
            # Display company info
            st.subheader(f"Analysis Results for {results['company_name']}")
            st.markdown(f"**Sector**: {results['sector']}")

            # Convert results to DataFrame for display
            df = convert_results_to_df(results)

            # Display results in a table
            st.dataframe(
                df,
                column_config={
                    "Metric": st.column_config.TextColumn("Metric", width=200),
                    "Passes Threshold": st.column_config.TextColumn(
                        "Passes", width=100
                    ),
                    "Value": st.column_config.TextColumn("Value", width=100),
                    "Threshold": st.column_config.TextColumn("Threshold", width=100),
                    "Description": st.column_config.TextColumn(
                        "Description", width=400
                    ),
                    "Classification": st.column_config.TextColumn(
                        "Classification", width=200
                    ),
                    "Guidelines": st.column_config.TextColumn("Guidelines", width=400),
                },
            )

            # Display combined plot for time series data if available
            if "quarterly_data" in results:
                st.subheader("Historical Analysis")

                # Combine all metrics into a single DataFrame
                combined_data = pd.DataFrame()
                for metric_name, quarterly_data in results["quarterly_data"].items():
                    if quarterly_data is not None and not quarterly_data.empty:
                        # Rename the series to a more readable name
                        combined_data[metric_name.replace("_", " ").title()] = (
                            quarterly_data
                        )

                if not combined_data.empty:
                    # Create a single plot with all metrics
                    fig = px.line(
                        combined_data,
                        title=f"Financial Metrics Over Time - {results['company_name']}",
                        labels={
                            "index": "Fiscal Quarter",
                            "value": "Ratio",
                            "variable": "Metric",
                        },
                    )

                    # Customize the layout
                    fig.update_layout(
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                        ),
                        yaxis_title="Ratio Value",
                        hovermode="x unified",
                        xaxis=dict(
                            tickangle=45,  # Angle the labels for better readability
                            tickmode="array",
                            ticktext=combined_data.index,
                            tickvals=list(range(len(combined_data.index))),
                        ),
                    )

                    # Add a horizontal line at y=0 for reference
                    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

                    # Show the plot
                    st.plotly_chart(fig, use_container_width=True)

                    # Add an expandable section with the raw data
                    with st.expander("View Raw Data"):
                        st.dataframe(combined_data)

# Add footer with instructions
st.markdown("---")
st.markdown("""
### How to use this tool:
1. Enter a company name or ticker symbol in the input field
2. Select the metrics you want to analyze
3. Click the "Analyze Company" button
4. View the results and download them as CSV if needed

The analysis is based on quarterly financial data from the past 10 years.
""")
