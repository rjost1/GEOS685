import pandas as pd
import matplotlib.pyplot as plt

def load_dataset(csv_path: str = None, df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Load a dataset from CSV or an existing DataFrame.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file. Required if df is not provided.
    df : pandas.DataFrame, optional
        A Pandas DataFrame

    Returns
    -------
    pandas.DataFrame
        A cleaned DataFrame with categorical types applied.
    """
    if df is None:
        if csv_path is None:
            raise ValueError("Provide either a CSV file path or a DataFrame.")
        df = pd.read_csv(csv_path)

    # Ensure correct dtypes - make this generic
    if "Ecosystem" in df.columns:
        df["Ecosystem"] = df["Ecosystem"].astype("category")
    if "Season" in df.columns:
        df["Season"] = df["Season"].astype("category")

    return df

def group_dataset(csv_path: str = None, df: pd.DataFrame = None, group_by: str = None) -> pd.DataFrame:
    """
    group the CSV or an existing DataFrame.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file. Required if df is not provided.
    df : pandas.DataFrame, optional
        A DataFrame with the required columns:
        ['ID', 'Ecosystem', 'Season', 'P_conc', 'Ca_conc', 'flux_gm2yr'].

    Returns
    -------
    pandas.DataFrame
        A cleaned DataFrame with categorical types applied.
    """
    if df is None:
        if csv_path is None:
            raise ValueError("Provide either a CSV file path or a DataFrame.")
        df = pd.read_csv(csv_path)

    # Ensure correct dtypes
    if "Ecosystem" in df.columns:
        df["Ecosystem"] = df["Ecosystem"].astype("category")
    if "Season" in df.columns:
        df["Season"] = df["Season"].astype("category")

    # Return grouped object if requested
    if group_by:
        if group_by not in df.columns:
            raise ValueError(f"group_by must be a column in DataFrame. Got '{group_by}'.")
        return df.groupby(group_by, observed=True) # this isn't great

    return df

def visualize_dataset(csv_path: str = None, df: pd.DataFrame = None, group_by: str = None, value_col: str = None, scatter_x: str = None, scatter_y: str = None) -> None:
    """
    General function to visualize a dataset as a scatter plot using pandas and matplotlib.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file. Required if df is not provided.
    df : pandas.DataFrame, optional
        DataFrame to visualize. If not provided, will load from csv_path.
    group_by : str, optional
        Column to group by in plots (e.g., categorical variable).
    value_col : str, optional
        Column to use for boxplot values.
    scatter_x : str, optional
        Column for x-axis in scatter plots.
    scatter_y : str, optional
        Column for y-axis in scatter plots.

    Returns
    -------
    None
        Displays matplotlib plots (no return value).
    """
    if df is None:
        if csv_path is None:
            raise ValueError("Provide either a CSV file path or a DataFrame.")
        df = pd.read_csv(csv_path)

    # Boxplot by group
    if group_by and value_col:
        plt.figure(figsize=(8, 5))
        df.boxplot(column=value_col, by=group_by, grid=False)
        plt.title(f"{value_col} by {group_by}")
        plt.suptitle("")
        plt.xlabel(group_by)
        plt.ylabel(value_col)
        plt.show()

    # Scatter plot
    if scatter_x and scatter_y:
        plt.figure(figsize=(7, 6))
        if group_by:
            for key, group in df.groupby(group_by):
                plt.scatter(group[scatter_x], group[scatter_y], label=key, alpha=0.7)
            plt.legend(title=group_by)
        else:
            plt.scatter(df[scatter_x], df[scatter_y], c="blue", alpha=0.7)
        plt.title(f"{scatter_y} vs {scatter_x}{' by ' + group_by if group_by else ''}")
        plt.xlabel(scatter_x)
        plt.ylabel(scatter_y)
        plt.show()

def visualize_dataset(csv_path: str = None, df: pd.DataFrame = None, group_by: str = "Ecosystem") -> None:
    """
    Visualize ecosystem dataset using pandas and matplotlib.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file. Required if df is not provided.
    df : pandas.DataFrame, optional
        A DataFrame with the required columns:
        ['ID', 'Ecosystem', 'Season', 'P_conc', 'Ca_conc', 'flux_gm2yr'].
    group_by : str, default="Ecosystem"
        Column to group by in plots. Options: "Ecosystem", "Season", or None.

    Returns
    -------
    None
        Displays matplotlib plots (no return value).
    """
    if df is None:
        if csv_path is None:
            raise ValueError("Provide either a CSV file path or a DataFrame.")
        df = pd.read_csv(csv_path)

    # Validate group_by
    if group_by not in ["Ecosystem", "Season", None]:
        raise ValueError("group_by must be 'Ecosystem', 'Season', or None")

    # Ensure correct dtypes
    if "Ecosystem" in df.columns:
        df["Ecosystem"] = df["Ecosystem"].astype("category")
    if "Season" in df.columns:
        df["Season"] = df["Season"].astype("category")

    # 1. Boxplot of flux by group
    if group_by:
        plt.figure(figsize=(8, 5))
        df.boxplot(column="flux_gm2yr", by=group_by, grid=False)
        plt.title(f"Flux by {group_by}")
        plt.suptitle("")
        plt.xlabel(group_by)
        plt.ylabel("Flux (g/m²/yr)")
        plt.show()

    # 2. Scatter plot: P vs Ca (colored by group if specified)
    plt.figure(figsize=(7, 6))
    if group_by:
        for key, group in df.groupby(group_by):
            plt.scatter(group["P_conc"], group["Ca_conc"], label=key, alpha=0.7)
        plt.legend(title=group_by)
    else:
        plt.scatter(df["P_conc"], df["Ca_conc"], c="blue", alpha=0.7)
    plt.title(f"P vs Ca Concentration{' by ' + group_by if group_by else ''}")
    plt.xlabel("P concentration")
    plt.ylabel("Ca concentration")
    plt.show()

    # 3. Scatter plot: Flux vs P concentration
    plt.figure(figsize=(7, 6))
    if group_by:
        for key, group in df.groupby(group_by):
            plt.scatter(group["P_conc"], group["flux_gm2yr"], label=key, alpha=0.7)
        plt.legend(title=group_by)
    else:
        plt.scatter(df["P_conc"], df["flux_gm2yr"], c="blue", alpha=0.7)
    plt.title(f"Flux vs P Concentration{' by ' + group_by if group_by else ''}")
    plt.xlabel("P concentration")
    plt.ylabel("Flux (g/m²/yr)")
    plt.show()

def convert_area(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert an area measurement between square meters, square kilometers,
    acres, and hectares.

    Parameters
    ----------
    value : float
        The numeric value of the area to convert.
    from_unit : str
        The unit of the input value. Must be one of:
        "m2", "km2", "acre", "hectare".
    to_unit : str
        The target unit to convert to. Must be one of:
        "m2", "km2", "acre", "hectare".

    Returns
    -------
    float
        The converted area in the target unit.

    Examples
    --------
    >>> convert_area(10000, "m2", "hectare")
    1.0
    >>> convert_area(2, "acre", "m2")
    8093.712
    >>> convert_area(1, "km2", "acre")
    247.105
    """
    # Conversion factors to square meters
    factors_to_m2 = {
        "m2": 1,
        "km2": 1_000_000,       # 1 km² = 1,000,000 m²
        "hectare": 10_000,      # 1 hectare = 10,000 m²
        "acre": 4046.8564224,   # 1 acre ≈ 4046.8564224 m²
    }

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in factors_to_m2 or to_unit not in factors_to_m2:
        raise ValueError("Units must be one of: 'm2', 'km2', 'hectare', 'acre'")

    # Convert to square meters first
    value_in_m2 = value * factors_to_m2[from_unit]

    # Then convert from m² to target unit
    return value_in_m2 / factors_to_m2[to_unit]

