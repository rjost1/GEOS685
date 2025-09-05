import pandas as pd
import matplotlib.pyplot as plt

def load_dataset(csv_path: str = None, df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Load the ecosystem dataset from CSV or an existing DataFrame.

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

    return df

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
