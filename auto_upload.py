from dotenv import load_dotenv
load_dotenv()

import json
import os
import pymysql
from db_utils import normalize_state, categorize_central_job, save_jobs_to_db

# ============================================
# 1. Combine all state files
# ============================================
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
        print(f"Skipping {filename} (not found)")

print(f"✅ Loaded {len(all_jobs)} total jobs from state files.")

# ============================================
# 2. Normalize states, assign central_category, remove duplicates
# ============================================
unique_jobs = []
seen_jobs = set()

for job in all_jobs:
    raw_state = job.get("state", "")
    norm_state = normalize_state(raw_state)
    job["state"] = norm_state

    if norm_state == "All India":
        job["centralCategory"] = categorize_central_job(
            job.get("organization", ""),
            job.get("title", "")
        )
    else:
        job["centralCategory"] = None

    job_key = f"{job.get('title', '').strip().lower()}|{job.get('organization', '').strip().lower()}|{norm_state}"

    if job_key not in seen_jobs:
        seen_jobs.add(job_key)
        unique_jobs.append(job)

print(f"✅ Combined {len(all_jobs)} jobs → {len(unique_jobs)} unique jobs after removing duplicates.")

# ============================================
# 3. Save combined data to master_jobs.json
# ============================================
output_path = "master_jobs.json"
with open(output_path, "w") as f:
    json.dump(unique_jobs, f, indent=4)

print(f"✅ Saved {len(unique_jobs)} unique jobs into master_jobs.json")

# ============================================
# 4. Direct upload to TiDB Cloud
# ============================================
try:
    print("Connecting to TiDB Cloud...")

    db_host = os.environ.get("DB_HOST")
    db_port = int(os.environ.get("DB_PORT", 4000))
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")

    if not all([db_host, db_user, db_password, db_name]):
        print("❌ Missing DB environment variables.")
        exit(1)

    connection = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        ssl={"ssl": {}},
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    print("✅ Connected to TiDB Cloud")

    inserted, skipped = save_jobs_to_db(unique_jobs, cursor)
    connection.commit()
    cursor.close()
    connection.close()

    print(f"━━━ Direct upload complete: {inserted} inserted, {skipped} skipped ━━━")

except Exception as e:
    print(f"❌ Error uploading to TiDB: {e}")
    exit(1)