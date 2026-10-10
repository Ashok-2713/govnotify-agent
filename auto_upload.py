import json
import os
import requests
from db_utils import normalize_state, categorize_central_job

# 1. Combine all state files
files = [
    "Karnataka_jobs.json",
    "Tamil_Nadu_jobs.json",
    "Kerala_jobs.json",
    "Andhra_Pradesh_jobs.json",
    "Telangana_jobs.json",
    "SSC_jobs.json",
    "UPSC_jobs.json",
    "Railways_jobs.json",
    "Banking_jobs.json",
    "India_Post_jobs.json",
    "Central_Government_jobs.json"
]

all_jobs = []

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                all_jobs.extend(data)
            else:
                all_jobs.append(data)
    else:
        print(f"Skipping {filename}")

# 2. Normalize states, assign central_category, and remove duplicates
unique_jobs = []
seen_jobs = set()

for job in all_jobs:
    raw_state = job.get("state", "")
    norm_state = normalize_state(raw_state)
    job["state"] = norm_state

    # Compute central category only for All India jobs
    if norm_state == "All India":
        job["centralCategory"] = categorize_central_job(job.get("organization", ""), job.get("title", ""))
    else:
        job["centralCategory"] = None

    # Create a unique key based on the job details
    job_key = f"{job.get('title', '').strip().lower()}|{job.get('organization', '').strip().lower()}|{norm_state}"
    
    if job_key not in seen_jobs:
        seen_jobs.add(job_key)
        unique_jobs.append(job)

print(f"✅ Combined {len(all_jobs)} jobs, but found {len(unique_jobs)} unique jobs after removing duplicates.")

# 3. Save to the folder where Spring Boot looks for it
output_path = "C:/Users/Ashok P/Downloads/govnotify_agent/master_jobs.json"
with open(output_path, "w") as f:
    json.dump(unique_jobs, f, indent=4)

print(f"✅ Saved {len(unique_jobs)} unique jobs into master_jobs.json")

# 4. Automatically trigger the Spring Boot Import
try:
    print("Connecting to Spring Boot backend...")
    response = requests.post("http://localhost:8080/api/import-jobs", timeout=10)
    print(response.text)
except Exception as e:
    print("❌ Could not reach the backend. Make sure your Spring Boot server is running first!")
    print(e)