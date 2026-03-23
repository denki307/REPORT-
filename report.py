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

    app = Client("ultra_fast_reporter", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

    async with app:
        print(colored("🔥 1-Second Ultra-Fast Reporting Mode Active!", "red", attrs=['bold']))
        
        while True:
            try:
                # Link parsing
                pattern = r"t\.me\/(?:c\/)?([^\/]+)\/(\d+)"
                match = re.search(pattern, TARGET_LINK)
                
                if not match:
                    print(colored("❌ Invalid Link!", "red"))
                    break 

                peer_raw = match.group(1)
                msg_id = int(match.group(2))
                peer = await app.resolve_peer(peer_raw)
                selected_reason = REASONS.get(REASON_INPUT.lower(), types.InputReportReasonOther())

                # The Report Action
                await app.invoke(
                    functions.messages.Report(
                        peer=peer,
                        id=[msg_id],
                        reason=selected_reason,
                        message="NDPS Act / Illegal Drugs Violation"
                    )
                )
                print(colored(f"✅ [1s] Report Sent! (Msg: {msg_id})", "green"))
                
                # 1 Second Gap
                await asyncio.sleep(1) 

            except Exception as e:
                # Flood Wait vandha script hang aagaama handle panna
                print(colored(f"⚠️ Warning/Error: {e}", "yellow"))
                # Telegram block panna, un account safe-ah irukka oru 30s pause kudukkuradhu nalladhu
                await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
