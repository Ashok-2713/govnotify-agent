import json
import os

# List of all state files
files = [
    "Karnataka_jobs.json",
    "Tamil_Nadu_jobs.json",
    "Kerala_jobs.json",
    "Andhra_Pradesh_jobs.json",
    "Telangana_jobs.json",
    "Central_Government_jobs.json"
]

all_jobs = []

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            
            # If it's a list, add all jobs
            if isinstance(data, list):
                all_jobs.extend(data)
            # If it's a dictionary (single job), add it as one item
            else:
                all_jobs.append(data)
    else:
        print(f"Skipping {filename} - file not found")

# Save the combined data into a single file
with open("master_jobs.json", "w") as f:
    json.dump(all_jobs, f, indent=4)

print(f"✅ Successfully combined {len(all_jobs)} jobs into master_jobs.json")