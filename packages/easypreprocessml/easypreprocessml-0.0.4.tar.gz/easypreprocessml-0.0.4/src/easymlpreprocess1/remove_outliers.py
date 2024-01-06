import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def remove_outliers(data, method="iqr", threshold=1.5):
    """
  Removes outliers from a dataset using the specified method and threshold, and drops rows containing NaNs.

  Args:
    data (pd.Series or pd.DataFrame): The data to process.
    method (str, optional): The outlier detection method to use. Defaults to "iqr". Supported methods:
      - "iqr": Interquartile Range (IQR) method, based on Q1 and Q3 quartiles.
      - "zscore": Z-score method, based on standard deviations from the mean.
      - "visual": Visual inspection using a box plot, with manual outlier selection by specifying lower and upper limits.
    threshold (float, optional): The threshold for outlier detection (used for IQR and Z-score methods). Defaults to 1.5.

  Returns:
    pd.Series or pd.DataFrame: The data with outliers removed and NaNs dropped.

  Raises:
    ValueError: If an invalid method is provided.

  Details on outlier detection methods:

  - **IQR method:**
      - Calculates Q1 (25th percentile) and Q3 (75th percentile) of the data.
      - Defines outliers as values falling below Q1 - (threshold * IQR) or above Q3 + (threshold * IQR).
  - **Z-score method:**
      - Calculates the mean and standard deviation of the data.
      - Defines outliers as values falling below mean - (threshold * std) or above mean + (threshold * std).
  - **Visual method:**
      - Creates a box plot of the data for visual inspection.
      - Prompts the user to enter lower and upper limits to define outlier boundaries.
      - Removes values falling outside the specified limits.

  Important considerations:

  - Removing outliers can significantly impact data distribution and analysis.
  - Carefully consider the implications before proceeding.
  - Explore alternative outlier handling techniques like winsorization or imputation if appropriate.
  - Consult with experts if uncertain about the best approach.
  """

    if method == "iqr":
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        return data[~((data < lower_bound) | (data > upper_bound))].dropna()
        
    elif method == "zscore":
        mean = data.mean()
        std = data.std()
        lower_bound = mean - (threshold * std)
        upper_bound = mean + (threshold * std)
        return data[~((data < lower_bound) | (data > upper_bound))].dropna()
        
    elif method == "visual":
        # Create a box plot to visually identify outliers
        sns.histplot(data=data,kde="True")
        plt.show()
        sns.boxplot(data=data,orient="h")
        plt.show()
        
        
        # Prompt the user for upper and lower limits
        lower_limit = float(input("Enter the lower limit for outlier removal: "))
        upper_limit = float(input("Enter the upper limit for outlier removal: "))

        return data[~((data < lower_limit) | (data > upper_limit))].dropna()  # Filter based on limits

  
    else:
        raise ValueError(f"Invalid method '{method}'. Supported methods are 'iqr', 'zscore', and 'visual'.")