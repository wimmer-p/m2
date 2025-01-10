### Description: This program calculates yearly average water levels for three lakes and visualizes the results.
### Version: 01 by Patrick Wimmer
### Date: 2025-01-10

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def process_and_plot(file_path, output_file):
    """
    Process the water level data and create yearly average plots.
    
    Parameters:
    - file_path: str, path to the input Excel file.
    - output_file: str, path to save the output Excel file.
    """
    # Load the Excel file
    data = pd.ExcelFile(file_path)
    sheet_name = 'Wasserpegel_Tagesdurchschnitt'
    df = data.parse(sheet_name)

    # Clean the dataset
    df.columns = ["DateTime", "Wallersee", "Mondsee", "Zeller See (Irrsee)"]
    df = df.iloc[2:].reset_index(drop=True)

    # Convert the DateTime column to datetime format and the lake levels to numeric
    df["DateTime"] = pd.to_datetime(df["DateTime"], errors='coerce', dayfirst=True)
    df["Wallersee"] = pd.to_numeric(df["Wallersee"], errors='coerce')
    df["Mondsee"] = pd.to_numeric(df["Mondsee"], errors='coerce')
    df["Zeller See (Irrsee)"] = pd.to_numeric(df["Zeller See (Irrsee)"], errors='coerce')

    # Add a 'Year' column for grouping by year
    df["Year"] = df["DateTime"].dt.year

    # Check if required columns exist
    if df[["Wallersee", "Mondsee", "Zeller See (Irrsee)"]].isnull().all().all():
        print("No valid data found. Exiting.")
        return

    # Drop rows with NaN in DateTime or water levels
    df_cleaned = df.dropna(subset=["DateTime", "Wallersee", "Mondsee", "Zeller See (Irrsee)"])

    # Calculate yearly averages
    yearly_averages = df_cleaned.groupby("Year")[["Wallersee", "Mondsee", "Zeller See (Irrsee)"]].mean()

    # Add unit of measurement to Excel output
    yearly_averages.columns = [f"{col} (cm)" for col in yearly_averages.columns]
    yearly_averages.to_excel(output_file, sheet_name='Yearly Averages')
    print(f"Yearly averages table (with unit cm) exported to {output_file}.")

    # Create bar charts for each lake with a curve statistic overlay
    sns.set(style="whitegrid")
    plt.figure(figsize=(18, 10))

    lakes = ["Wallersee", "Mondsee", "Zeller See (Irrsee)"]
    for i, lake in enumerate(lakes, start=1):  # Loop for generating plots
        plt.subplot(3, 1, i)
        # Align bar chart and trend curve
        x_values = yearly_averages.index.astype(str)  # Convert years to string for alignment
        plt.bar(x=x_values, height=yearly_averages[f"{lake} (cm)"], color="skyblue", alpha=0.7, label=f"Yearly Avg {lake}")
        plt.plot(x_values, yearly_averages[f"{lake} (cm)"], color="orange", linewidth=2, label=f"Trend {lake}")
        plt.title(f"Yearly Average Water Levels for {lake} (cm)", fontsize=14)
        plt.xlabel("Year")
        plt.ylabel("Water Level (cm)")
        plt.legend()
        plt.xticks(rotation=45, fontsize=8)

    plt.tight_layout()
    plt.show()

# Main script
file_path = 'input_wasserpegel.xlsx'  
output_file = 'yearly_averages_with_units.xlsx'  
process_and_plot(file_path, output_file)
