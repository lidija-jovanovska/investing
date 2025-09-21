# Value Investing with Python: Implementing Benjamin Graham's Defensive Investor Criteria

This project provides tools for financial data analysis using the Financial Modeling Prep API. 
The main notebook demonstrates how to fetch and analyze financial data such as market capitalization, financial ratios, 
earnings, and dividends for a given stock ticker. The notebook also provides a simple implementation of Benjamin Graham's
criteria for defensive investors, which can be used to identify potentially undervalued stocks.

## Project Organization

```
.
├── src/                    # Source code
│   ├── api/               # API related code
│   │   └── api_utils.py   # API utility functions for fetching financial data
│   ├── analysis/          # Analysis related code
│   │   ├── analysis_utils.py  # Utility functions for data analysis
│   │   └── company_analyzer.py # Company analysis logic
│   └── filters/           # Investment criteria filters
├── notebooks/             # Jupyter notebooks
│   ├── main.ipynb        # Main analysis notebook
│   └── buffett_analysis.ipynb # Warren Buffett analysis
├── data/                  # Data files
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (not in version control)
├── LICENSE.txt           # License information
└── README.md             # Project documentation
```g with Python: Implementing Benjamin Graham’s Defensive Investor Criteria

This project provides tools for financial data analysis using the Financial Modeling Prep API. 
The main notebook demonstrates how to fetch and analyze financial data such as market capitalization, financial ratios, 
earnings, and dividends for a given stock ticker. The notebook also provides a simple implementation of Benjamin Graham’s
criteria for defensive investors, which can be used to identify potentially undervalued stocks.

## Project Organization

```
.
├── api_utils.py            # API utility functions for fetching financial data
├── main.ipynb              # Main Jupyter notebook for data analysis
├── .gitignore              # Git ignore file
└── README.md               # Project README file
```

## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your API key:
    - Create a `.env` file in the project root directory.
    - Add your Financial Modeling Prep API key to the `.env` file:
      ```
      API_KEY=your_api_key_here
      ```

## Running the Notebook

1. Start Jupyter Notebook:
    ```sh
    jupyter notebook
    ```

2. Open `main.ipynb` in the Jupyter interface.

3. Follow the instructions in the notebook to fetch and analyze financial data.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.