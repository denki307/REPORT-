import os
import asyncio
import re
import sys
from pyrogram import Client
from pyrogram.raw import functions, types
from termcolor import colored

# --- Config Vars ---
API_ID = int(os.environ.get("API_ID", 29282829))
API_HASH = os.environ.get("API_HASH", 'bj7285v7766828999167f46288')
STRING_SESSION = os.environ.get("STRING_SESSION")
TARGET_LINK = os.environ.get("TARGET_LINK")
REASON_INPUT = os.environ.get("REASON", "drugs")

REASONS = {
    "spam": types.InputReportReasonSpam(),
    "violence": types.InputReportReasonViolence(),
    "pornography": types.InputReportReasonPornography(),
    "childabuse": types.InputReportReasonChildAbuse(),
    "copyright": types.InputReportReasonCopyright(),
    "fake": types.InputReportReasonFake(),
    "drugs": types.InputReportReasonIllegalDrugs(),
    "other": types.InputReportReasonOther()
}

async def main():
    if not STRING_SESSION or not TARGET_LINK:
        print(colored("❌ Error: STRING_SESSION or TARGET_LINK missing!", "red"))
        return

    app = Client("fast_reporter", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

    async with app:
        print(colored("🚀 1-Minute Fast Reporting Started...", "green"))
        
        while True:
            try:
                # Extracting details from link
                pattern = r"t\.me\/(?:c\/)?([^\/]+)\/(\d+)"
                match = re.search(pattern, TARGET_LINK)
                
                if not match:
                    print(colored("❌ Invalid Link Format!", "red"))
                    break 

                peer_raw = match.group(1)
                msg_id = int(match.group(2))
                peer = await app.resolve_peer(peer_raw)
                selected_reason = REASONS.get(REASON_INPUT.lower(), types.InputReportReasonOther())

                # Sending the Report
                await app.invoke(
                    functions.messages.Report(
                        peer=peer,
                        id=[msg_id],
                        reason=selected_reason,
                        message="NDPS Act / Illegal Drugs Violation"
                    )
                )
                print(colored(f"✅ Report Sent Successfully! (Msg: {msg_id})", "green"))
                
                # 1 Minute Gap (60 seconds)
                print(colored("⏳ Waiting 60 seconds for next report...", "yellow"))
                await asyncio.sleep(60) 

            except Exception as e:
                # Flood wait or other errors handle panna
                print(colored(f"⚠️ Error: {e}", "red"))
                print(colored("🔄 Retrying in 60 seconds...", "cyan"))
                await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
