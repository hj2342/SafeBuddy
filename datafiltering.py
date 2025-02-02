import pandas as pd

# Use the full path if needed
file_path = "/Users/hariharanjanardhanan/Desktop/2__.Hackathon Slush/NYPD_Complaint_Data_Current__Year_To_Date__20250202.csv"


# Read the CSV file
df = pd.read_csv(file_path)


# Drop rows with missing latitude or longitude
df = df.dropna(subset=["Latitude", "Longitude"])

# Round latitude and longitude to 3 decimal places (groups locations ~100m radius)
df["Rounded_Lat"] = df["Latitude"].round(3)
df["Rounded_Lon"] = df["Longitude"].round(3)

# Group by rounded coordinates and count crimes
crime_counts = df.groupby(["Rounded_Lat", "Rounded_Lon"]).size().reset_index(name="Crime_Count")

# Define threshold for unsafe areas (top 25% crime-prone locations)
threshold = crime_counts["Crime_Count"].quantile(0.75)

# Classify areas as Safe or Unsafe
crime_counts["Safety_Status"] = crime_counts["Crime_Count"].apply(
    lambda x: "Unsafe" if x > threshold else "Safe"
)

# Get separate lists of Safe and Unsafe locations
safe_locations = crime_counts[crime_counts["Safety_Status"] == "Safe"]
unsafe_locations = crime_counts[crime_counts["Safety_Status"] == "Unsafe"]

# Save lists to CSV files
safe_locations.to_csv("/Users/hariharanjanardhanan/Desktop/2__.Hackathon Slush/data/safe_locations.csv", index=False)
unsafe_locations.to_csv("/Users/hariharanjanardhanan/Desktop/2__.Hackathon Slush/data/unsafe_locations.csv", index=False)

print("\nLists of Safe and Unsafe locations have been saved as CSV files!")
print("\nTop 5 Safe Locations:\n", safe_locations.head())
print("\nTop 5 Unsafe Locations:\n", unsafe_locations.head())