import os

# ===============================================================
# TELEMETRY AND TRACING SUPPRESSION (Suppress OpenTelemetry noise)
# ===============================================================
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_DISABLE_TRACING"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["OTEL_TRACES_EXPORTER"] = "none"
os.environ["OTEL_METRICS_EXPORTER"] = "none"
os.environ["OTEL_LOGS_EXPORTER"] = "none"

import logging
logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)
logging.getLogger("opentelemetry.exporter").setLevel(logging.CRITICAL)
logging.getLogger("crewai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def categorize_central_job(organization, title):
    """Categorize Central Government jobs by department."""
    org = (organization or "").lower()
    ttl = (title or "").lower()
    combined = org + " " + ttl

    if any(x in combined for x in ["railway", "rrb", "rrc", "irctc"]):
        return "Railways"
    if any(x in combined for x in ["ssc", "staff selection"]):
        return "SSC"
    if any(x in combined for x in ["bank", "ibps", "sbi", "rbi", "nabard"]):
        return "Banking"
    if any(x in combined for x in ["india post", "postal", "gds", "post office"]):
        return "India Post"
    if any(x in combined for x in ["upsc", "union public service"]):
        return "UPSC"
    return "Other Central"


def normalize_state(raw_state):
    """Normalize state names to allowed values."""
    if not raw_state:
        return "All India"
    s = str(raw_state).strip().lower()
    all_india_aliases = ["national", "all states", "various states", "all states/uts", "central", "all india", "india", "central government"]
    if any(alias in s for alias in all_india_aliases):
        return "All India"
    state_map = {
        "karnataka": "Karnataka",
        "tamil nadu": "Tamil Nadu",
        "tamilnadu": "Tamil Nadu",
        "kerala": "Kerala",
        "andhra pradesh": "Andhra Pradesh",
        "ap": "Andhra Pradesh",
        "telangana": "Telangana",
        "ts": "Telangana"
    }
    for key, value in state_map.items():
        if key in s:
            return value
    return "All India"  # Default for unknown states


def save_jobs_to_db(jobs, cursor):
    """Save jobs to MySQL with categorization and duplicate prevention."""
    inserted_count = 0
    skipped_count = 0

    for job in jobs:
        try:
            title = (job.get("title") or "").strip()
            organization = (job.get("organization") or "").strip()
            state = normalize_state(job.get("state", ""))

            # Compute central category only for All India jobs
            central_category = None
            if state == "All India":
                central_category = categorize_central_job(organization, title)

            last_date = job.get("lastDate") or job.get("last_date") or None
            reg_start = job.get("registrationStartDate") or job.get("registration_start_date") or None
            apply_url = job.get("officialApplyUrl") or job.get("official_apply_url") or None
            pdf_url = job.get("officialPdfUrl") or job.get("official_pdf_url") or None
            status = job.get("status") or "OPEN"

            # Skip if title is empty
            if not title:
                skipped_count += 1
                continue

            cursor.execute("""
                INSERT IGNORE INTO job_notifications
                (title, organization, state, central_category, last_date, registration_start_date, official_apply_url, official_pdf_url, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, organization, state, central_category, last_date, reg_start, apply_url, pdf_url, status))

            if cursor.rowcount > 0:
                inserted_count += 1
                logging.info(f"✅ Inserted: {title[:50]} | State: {state} | Category: {central_category}")
            else:
                skipped_count += 1
                logging.info(f"⏭️  Skipped (duplicate): {title[:50]}")

        except Exception as e:
            logging.error(f"❌ Error inserting job '{job.get('title', 'Unknown')}': {e}")
            skipped_count += 1
            continue

    logging.info(f"━━━ Agent run complete: {inserted_count} inserted, {skipped_count} skipped ━━━")
    return inserted_count, skipped_count
