import os
import asyncio
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ReportPeerRequest
from telethon.tl.types import *
from termcolor import colored

# --- Config Vars from Heroku ---
API_ID = int(os.environ.get("API_ID", 29282829))
API_HASH = os.environ.get("API_HASH", 'bj7285v7766828999167f46288')
STRING_SESSION = os.environ.get("STRING_SESSION")

# Important: Heroku-la intha 2 variables-ah update panni "Run" pannu
TARGET_LINK = os.environ.get("TARGET_LINK") # Example: https://t.me/c/12345/678 or https://t.me/username/678
REASON_INPUT = os.environ.get("REASON", "spam") # spam, violence, pornography, childabuse, copyright, fake, drugs

# Reason Mapping
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
        print(colored("Error: STRING_SESSION or TARGET_LINK missing in Heroku Config Vars!", "red"))
        return

    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.connect()

    try:
        # Link-la irunthu Username and Message ID eduka (Regex)
        # Format: https://t.me/username/123
        pattern = r"t\.me\/(?:c\/)?([^\/]+)\/(\d+)"
        match = re.search(pattern, TARGET_LINK)
        
        if not match:
            print(colored("Invalid Link Format!", "red"))
            return

        peer_input = match.group(1)
        msg_id = int(match.group(2))

        # Private channel-ah இருந்தா ID convert பண்ணனும்
        if peer_input.isdigit():
            peer = int(f"-100{peer_input}")
        else:
            peer = peer_input

        # Reason select panna
        selected_reason = REASONS.get(REASON_INPUT.lower(), InputReportReasonSpam())

        print(colored(f"Reporting Message {msg_id} in {peer} for {REASON_INPUT}...", "cyan"))

        # Specific Message Report Logic
        await client(ReportPeerRequest(
            peer=peer,
            id=[msg_id], # Ithu thaan specific message-ah report pannum
            reason=selected_reason,
            message=f"Reporting specific content for {REASON_INPUT}"
        ))

        print(colored("Successfully reported the specific message!", "green"))

    except Exception as e:
        print(colored(f"Error: {e}", "red"))
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
