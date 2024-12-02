import pandas as pd

# Load the files
hr_file = "../../outputs/cleaned/781756_cleaned_hr.out"
motion_file = "../../outputs/cleaned/781756_cleaned_motion.out"
psg_file = "../../outputs/cleaned/781756_cleaned_psg.out"
output_file = "../../train_data.csv"

print("Loading data files...")

# Load data into pandas DataFrames
hr_data = pd.read_csv(hr_file, sep=" ", header=None, names=["timestamp", "heart_rate"])
print(f"Loaded heart rate data: {len(hr_data)} rows.")

motion_data = pd.read_csv(motion_file, sep=" ", header=None, names=["timestamp", "Ax", "Ay", "Az"])
print(f"Loaded motion data: {len(motion_data)} rows.")

psg_data = pd.read_csv(psg_file, sep=" ", header=None, names=["timestamp", "label"])
print(f"Loaded PSG data: {len(psg_data)} rows.")

print("Adding heart rate data to motion data...")

# Add heart rate data to motion data
motion_data["heart_rate"] = motion_data["timestamp"].apply(
    lambda x: hr_data.loc[hr_data["timestamp"] <= x, "heart_rate"].iloc[-1]
    if not hr_data.loc[hr_data["timestamp"] <= x].empty else None
)
print("Heart rate data added to motion data.")

print("Adding sleep stage data to motion data...")

# Add sleep stage labels to motion data
motion_data["label"] = motion_data["timestamp"].apply(
    lambda x: psg_data.loc[psg_data["timestamp"] <= x, "label"].iloc[-1]
    if not psg_data.loc[psg_data["timestamp"] <= x].empty else None
)
print("Sleep stage data added to motion data.")

print("Saving merged data to CSV...")

# Save the combined data to a CSV file
motion_data.to_csv(output_file, index=False)

print(f"Data successfully merged and saved to {output_file}")