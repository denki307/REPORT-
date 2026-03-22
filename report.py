import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ReportPeerRequest
from telethon.tl.types import InputReportReasonSpam
from termcolor import colored

# Heroku Settings -> Config Vars-la intha names-ah add pannu
API_ID = int(os.environ.get("API_ID", 29282829))
API_HASH = os.environ.get("API_HASH", 'bj7285v7766828999167f46288')
STRING_SESSION = os.environ.get("STRING_SESSION") # Step 1-la kedacha code
TARGET = os.environ.get("TARGET", "@example_channel") # Report panna vendiya username

async def main():
    if not STRING_SESSION:
        print(colored("Error: STRING_SESSION variable miss aaguthu!", "red"))
        return

    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    await client.connect()
    if not await client.is_user_authorized():
        print(colored("Session expired! Login again on PC.", "red"))
        return

    print(colored(f"Reporting {TARGET}...", "cyan"))
    
    try:
        # Simple Loop for 3 reports (Safe limit)
        for i in range(3):
            await client(ReportPeerRequest(
                peer=TARGET,
                reason=InputReportReasonSpam(),
                message="Reporting for spam activity."
            ))
            print(colored(f"Report {i+1} sent!", "green"))
            await asyncio.sleep(5) # Delay to avoid flood
            
    except Exception as e:
        print(colored(f"Error: {e}", "red"))
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

