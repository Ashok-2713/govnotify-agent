import os

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

import time
import json
import re
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Load your API keys
load_dotenv()

# ==========================================
# 1. API KEY FAILOVER LOGIC (3 Keys)
# ==========================================
api_keys = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# ==========================================
# 2. LINK VERIFICATION TOOL
# ==========================================
def verify_link(url):
    """Checks if a URL is valid and reachable."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return 200 <= response.status_code < 400
    except:
        return False

# ==========================================
# 3. SETUP TOOLS AND AGENT
# ==========================================
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

agent = Agent(
    role="Government Job Data Scout",
    goal="Find all currently open and upcoming government jobs in India.",
    backstory="You are a meticulous and accurate web researcher. You must only report data from official government portals. Do not make up job information.",
    llm="gemini/gemini-3.5-flash-lite",
    tools=[search_tool, scrape_tool],
    verbose=False,
    allow_delegation=False
)

# ==========================================
# 4. TASK CREATION
# ==========================================
def create_task(state_name, search_query):
    return Task(
        description=f"""Search for government jobs in {state_name}. You are an expert scout. 

**CRITICAL INSTRUCTIONS:**
1. MANDATORY: Search for ALL major Central Government departments (SSC, UPSC, Railways, Banking, India Post, Army, Navy, Airforce, etc.).
2. **LOOK FOR EVERYTHING:** Do not limit yourself to just one portal. Search multiple portals and bring back everything you find.
3. **OPEN JOBS:** Find jobs where the 'Last Date to Apply' is in the FUTURE (after today's date).
4. **UPCOMING JOBS:** Look for the **OFFICIAL JOB CALENDAR** and list upcoming jobs with 'status': 'UPCOMING'.
5. **OUTPUT FORMAT:** You MUST output the data as a **JSON array**. Do NOT output any text, bullets, or commentary. ONLY output JSON.
6. If a specific field is missing, leave it as null or empty.
""",
        expected_output=f"""Output ONLY a valid JSON array. You MUST output a MINIMUM of 5 jobs (if they exist). Each object must strictly have these exact keys: 'title', 'state', 'organization', 'lastDate', 'registrationStartDate', 'officialApplyUrl', 'officialPdfUrl', 'status'. If a job is upcoming, set 'status' to 'UPCOMING' and 'lastDate' to null. Do not output any text before or after the JSON.""",
        agent=agent
    )

# ==========================================
# 5. RUN THE FAILOVER LOOP
# ==========================================
states = [
    ("SSC", "SSC CGL CHSL MTS Steno JE upcoming recruitment official"),
    ("UPSC", "UPSC Civil Services NDA CDS IES upcoming recruitment official"),
    ("Railways", "RRB Group D NTPC ALP Technician upcoming recruitment official"),
    ("Banking", "IBPS SBI RBI Clerk PO SO upcoming recruitment official"),
    ("India Post", "India Post GDS Postman MTS upcoming recruitment official"),
    ("Central Government", "All Central Government job notifications 2026 SSC UPSC RRB IBPS SBI RBI India Post Army Navy Airforce upcoming official")
]

# FORCE CLEAR THE PROGRESS LOG AT THE VERY START
with open("progress_log.txt", "w") as f:
    f.write("")

for state_name, query in states:
    print(f"\n{'='*60}")
    print(f"🔍 SEARCHING FOR: {state_name.upper()} JOBS")
    print(f"{'='*60}\n")

    # Try each API key until one works
    for key_index, key in enumerate(api_keys):
        try:
            os.environ["GEMINI_API_KEY"] = key
            print(f"🔑 Trying {state_name} with Key {key_index + 1}...")

            task = create_task(state_name, query)
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )

            result = crew.kickoff(inputs={"search_query": query})

            raw_result = str(result)
            json_match = re.search(r'\[.*\]', raw_result, re.DOTALL)

            if json_match:
                clean_json = json_match.group()
            else:
                clean_json = "[]"

            with open(f"{state_name.replace(' ', '_')}_jobs.json", "w") as f:
                json.dump(json.loads(clean_json), f, indent=4)

            with open("progress_log.txt", "a") as f:
                f.write(f"{state_name}\n")

            print(f"\n📋 RESULT FOR {state_name.upper()}:\n")
            print(clean_json)
            print("\n" + "-"*60)

            if state_name != "Central Government":
                print(f"⏳ Waiting 60 seconds to avoid rate limits...")
                time.sleep(60)

            break

        except Exception as e:
            error_str = str(e)
            # 1. Quota error (429) — switch to next key
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"\n⚠️ Key {key_index + 1} exhausted. Switching to Key {key_index + 2}...")
                time.sleep(10)
                continue
            # 2. Server busy (503) — wait and retry
            elif "503" in error_str or "UNAVAILABLE" in error_str:
                print(f"\n⚠️ Google server busy. Waiting 30s before retry...")
                time.sleep(30)
                continue
            # 3. Network hiccup — wait and retry
            elif any(x in error_str for x in ["getaddrinfo", "Connection aborted", "RemoteDisconnected", "timed out"]):
                print(f"\n⚠️ Network hiccup. Waiting 20s before retry...")
                time.sleep(20)
                continue
            # 4. Any other error — skip this state
            else:
                print(f"\n❌ Error on {state_name}: {e}")
                break

print("\n✅ ALL STATES COMPLETED!")