import os
import asyncio
import re
import sys
from pyrogram import Client
from pyrogram.raw import functions, types
from termcolor import colored

# --- Config Vars from Heroku ---
API_ID = int(os.environ.get("API_ID", 29282829))
API_HASH = os.environ.get("API_HASH", 'bj7285v7766828999167f46288')
STRING_SESSION = os.environ.get("STRING_SESSION")
TARGET_LINK = os.environ.get("TARGET_LINK")
REASON_INPUT = os.environ.get("REASON", "drugs") # Default set to drugs based on your log

# Mapping Reasons to Pyrogram Raw Types
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
        print(colored("Error: Missing STRING_SESSION or TARGET_LINK in Heroku Config Vars!", "red"))
        return

    # Initialize Pyrogram Client
    app = Client("report_bot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

    async with app:
        try:
            # Regex to extract Peer (username/ID) and Message ID
            # Handles https://t.me/username/123 or https://t.me/c/12345/123
            pattern = r"t\.me\/(?:c\/)?([^\/]+)\/(\d+)"
            match = re.search(pattern, TARGET_LINK)
            
            if not match:
                print(colored("Invalid Link Format! Use https://t.me/chat/123", "red"))
                return

            peer_raw = match.group(1)
            msg_id = int(match.group(2))

            # Resolve the peer (Group/Channel/User)
            peer = await app.resolve_peer(peer_raw)
            
            # Select the reason
            selected_reason = REASONS.get(REASON_INPUT.lower(), types.InputReportReasonOther())

            print(colored(f"Reporting Message {msg_id} in {peer_raw}...", "cyan"))
            print(colored(f"Reason: {REASON_INPUT}", "yellow"))

            # THE FIX: Using functions.messages.Report
            await app.invoke(
                functions.messages.Report(
                    peer=peer,
                    id=[msg_id], # Must be a list of IDs
                    reason=selected_reason,
                    message="Controlled substances/NDPS Act violation."
                )
            )

            print(colored("✅ Report successfully submitted to Telegram!", "green"))

        except Exception as e:
            print(colored(f"❌ Error: {e}", "red"))
        finally:
            print(colored("Stopping worker to prevent Heroku restart loop...", "magenta"))
            # This stops the Heroku worker from looping
            sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
