import pandas as pd

# Updating the file paths with the specified directory
file_path_prefix = "fhir-fastapiapp/"

# List of CSV files with updated paths
csv_files = [
    f"{file_path_prefix}CPU Saturation (Load1 per CPU)-data-2024-08-06 08_32_33.csv",
    f"{file_path_prefix}CPU Usage-data-2024-08-06 08_30_16.csv",
    f"{file_path_prefix}CPU Utilisation-data-2024-08-06 08_32_27.csv",
    f"{file_path_prefix}CPU usage-data-2024-08-06 08_49_17.csv",
    f"{file_path_prefix}Cgroup manager operation rate-data-as-joinbyfield-2024-08-06 08_48_31.csv",
    f"{file_path_prefix}Disk IO Saturation-data-2024-08-06 08_33_04.csv",
    f"{file_path_prefix}Disk IO Utilisation-data-2024-08-06 08_32_59.csv",
    f"{file_path_prefix}Disk I_O-data-as-joinbyfield-2024-08-06 08_30_54.csv",
    f"{file_path_prefix}Load Average-data-as-joinbyfield-2024-08-06 08_30_24.csv",
    f"{file_path_prefix}Memory Saturation (Major Page Faults)-data-2024-08-06 08_32_43.csv",
    f"{file_path_prefix}Memory Usage-data-2024-08-06 08_30_44.csv",
    f"{file_path_prefix}Memory Usage-data-as-joinbyfield-2024-08-06 08_30_36.csv",
    f"{file_path_prefix}Memory Utilisation-data-2024-08-06 08_32_38.csv",
    f"{file_path_prefix}Memory-data-2024-08-06 08_49_10.csv",
    f"{file_path_prefix}Network Received-data-as-joinbyfield-2024-08-06 08_31_05.csv",
    f"{file_path_prefix}Network Transmitted-data-as-joinbyfield-2024-08-06 08_31_26.csv",
    f"{file_path_prefix}Network Utilisation (Bytes Receive_Transmit)-data-2024-08-06 08_32_49.csv",
    f"{file_path_prefix}Network Utilisation (Bytes Receive_Transmit)-data-2024-08-06 08_32_50.csv",
    f"{file_path_prefix}Observed Concurrency-data-as-joinbyfield-2024-08-06 08_23_11.csv",
    f"{file_path_prefix}PLEG relist duration-data-2024-08-06 08_48_44.csv",
    f"{file_path_prefix}Pod Counts-data-as-joinbyfield-2024-08-06 08_19_29.csv",
    f"{file_path_prefix}Pod Memory Usage-data-2024-08-06 08_19_16.csv",
    f"{file_path_prefix}Pod Start Duration-data-as-joinbyfield-2024-08-06 08_47_55.csv",
    f"{file_path_prefix}Pod Start Rate-data-as-joinbyfield-2024-08-06 08_48_04 (1).csv",
    f"{file_path_prefix}Pod Start Rate-data-as-joinbyfield-2024-08-06 08_48_04.csv",
    f"{file_path_prefix}RPC rate-data-as-joinbyfield-2024-08-06 08_48_52.csv",
    f"{file_path_prefix}Reconcile Count (per min)-data-as-joinbyfield-2024-08-06 08_26_54.csv",
    f"{file_path_prefix}Request Concurrency-data-2024-08-06 08_18_40.csv",
    f"{file_path_prefix}Request Concurrency-data-2024-08-06 08_24_27.csv",
    f"{file_path_prefix}Request Count in last minute by Response Code-data-2024-08-06 08_23_41.csv",
    f"{file_path_prefix}Request Volume-data-2024-08-06 08_25_20.csv",
    f"{file_path_prefix}Request duration 99th quantile-data-as-joinbyfield-2024-08-06 08_49_01.csv",
    f"{file_path_prefix}Response Time in last minute-data-as-joinbyfield-2024-08-06 08_24_02.csv",
    f"{file_path_prefix}Revision CPU Usage-data-as-joinbyfield-2024-08-06 08_19_02.csv",
    f"{file_path_prefix}Revision Pod Counts-data-as-joinbyfield-2024-08-06 08_18_08.csv",
    f"{file_path_prefix}Storage Operation Duration 99th quantile-data-as-joinbyfield-2024-08-06 08_48_23.csv",
    f"{file_path_prefix}Storage Operation Rate-data-as-joinbyfield-2024-08-06 08_48_12.csv",
    f"{file_path_prefix}knative.dev.serving.pkg.reconciler.configuration.Reconciler Reconcile Count (per min)-data-2024-08-06 08_27_06.csv"
]

# Dictionary to store the dataframes
dataframes = {}

# Read and store dataframes
for file in csv_files:
    try:
        df = pd.read_csv(file)
        dataframes[file] = df
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Print columns and head for each dataframe
for file, df in dataframes.items():
    print(f"\nFile: {file}")
    print("Columns:", df.columns.tolist())
    print("Head:\n", df.head(), "\n")
