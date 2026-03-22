import os
import asyncio
import re
from pyrogram import Client, enums
from pyrogram.raw import functions
from pyrogram.raw.types import *
from termcolor import colored

# --- Config Vars ---
API_ID = int(os.environ.get("API_ID", 29282829))
API_HASH = os.environ.get("API_HASH", 'bj7285v7766828999167f46288')
STRING_SESSION = os.environ.get("STRING_SESSION")
TARGET_LINK = os.environ.get("TARGET_LINK")
REASON_INPUT = os.environ.get("REASON", "spam")

# Pyrogram Reasons Mapping
REASONS = {
    "spam": InputReportReasonSpam(),
    "violence": InputReportReasonViolence(),
    "pornography": InputReportReasonPornography(),
    "childabuse": InputReportReasonChildAbuse(),
    "copyright": InputReportReasonCopyright(),
    "fake": InputReportReasonFake(),
    "drugs": InputReportReasonIllegalDrugs(),
    "other": InputReportReasonOther()
}

async def main():
    if not STRING_SESSION or not TARGET_LINK:
        print(colored("Error: Vars missing!", "red"))
        return

    # Pyrogram Client Setup
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

    async with app:
        try:
            # Regex to extract username/ID and Message ID
            pattern = r"t\.me\/(?:c\/)?([^\/]+)\/(\d+)"
            match = re.search(pattern, TARGET_LINK)
            
            if not match:
                print(colored("Invalid Link!", "red"))
                return

            peer_raw = match.group(1)
            msg_id = int(match.group(2))

            # Resolve Peer (User/Channel/Group)
            peer = await app.resolve_peer(peer_raw)
            selected_reason = REASONS.get(REASON_INPUT.lower(), InputReportReasonSpam())

            print(colored(f"Reporting Message {msg_id} in {peer_raw} for {REASON_INPUT}...", "cyan"))

            # Pyrogram Raw API call for reporting
            await app.invoke(
                functions.messages.ReportPeer(
                    peer=peer,
                    id=[msg_id],
                    reason=selected_reason,
                    message=f"Reporting for {REASON_INPUT}"
                )
            )

            print(colored("Report successfully submitted via Pyrogram!", "green"))

        except Exception as e:
            print(colored(f"Error: {e}", "red"))

if __name__ == "__main__":
    asyncio.run(main())
