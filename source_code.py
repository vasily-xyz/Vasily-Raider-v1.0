import asyncio
import aiofiles
import aiohttp
import websockets
import json
import os
from time import sleep
from pystyle import Colors, Colorate
import tls_client
from datetime import datetime


def Spinner():
    pass


def setTitle(title):
    pass


def display_logo():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    os.system(f'title ^| • Vasily Raider ^| • Discord.gg/vasily ^| • Version : 1.0 ^|')
    print(Colorate.Horizontal(Colors.red_to_blue, r"""
                                       ██╗   ██╗ █████╗ ███████╗██╗██╗  ██╗   ██╗
                                       ██║   ██║██╔══██╗██╔════╝██║██║  ╚██╗ ██╔╝
                                       ██║   ██║███████║███████╗██║██║   ╚████╔╝ 
                                       ╚██╗ ██╔╝██╔══██║╚════██║██║██║    ╚██╔╝  
                                        ╚████╔╝ ██║  ██║███████║██║███████╗██║   
                                         ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  
                                    ════════════════════════════════════════════════
                                ╔═══════════════════════════════════════════════════════╗
                                ║                                                       ║
                                ║ Developed By vasily.v Discord.gg/vasily Version: 1.0  ║
                                ║                                                       ║                     
                                ╚═══════════════════════════════════════════════════════╝
    """))

def display_help_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    os.system(f'title ^| • Vasily Raider ^| • Discord.gg/vasily ^| • Version : 1.0 ^| • Commands Page ^| ')
    print(Colorate.Horizontal(Colors.red_to_blue, r"""
                                       ██╗   ██╗ █████╗ ███████╗██╗██╗  ██╗   ██╗
                                       ██║   ██║██╔══██╗██╔════╝██║██║  ╚██╗ ██╔╝
                                       ██║   ██║███████║███████╗██║██║   ╚████╔╝ 
                                       ╚██╗ ██╔╝██╔══██║╚════██║██║██║    ╚██╔╝  
                                        ╚████╔╝ ██║  ██║███████║██║███████╗██║   
                                         ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  
                                    ════════════════════════════════════════════════
                                ╔═══════════════════════════════════════════════════════╗
                                ║                          ║                            ║
                                ║   1 Channel Spammer      ║      3 Token Checker       ║
                                ║                          ║                            ║
                                ║═══════════════════════════════════════════════════════║
                                ║                          ║                            ║ 
                                ║   2 Thread Spammer       ║      4 VC Joiner           ║
                                ║                          ║                            ║                     
                                ╚═══════════════════════════════════════════════════════╝
    """))


async def channel_spammer():
    CHANNEL_ID = input(Colorate.Horizontal(Colors.red_to_blue, " Enter your channel ID>> "))
    MESSAGES = input(Colorate.Horizontal(Colors.red_to_blue, " Enter your message to spam>> "))
    MESSAGE_COUNT = int(input(Colorate.Horizontal(Colors.red_to_blue, " Enter how many messages>> ")))


    async with aiofiles.open('input/tokens.txt', 'r') as file:
        tokens = [line.strip() for line in await file.readlines() if line.strip()]


    async def send_message(token):
        url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
        headers = {'Authorization': token}
        async with aiohttp.ClientSession() as session:
            for _ in range(MESSAGE_COUNT):
                for message in MESSAGES.split('\n'):
                    data = {'content': message}
                    async with session.post(url, json=data, headers=headers) as response:
                        current_time = datetime.now().strftime("%H:%M:%S")
                        if response.status == 200:
                            print(Colorate.Horizontal(Colors.red_to_blue, f" [{current_time}] Sent Message Successfully"))
                        elif response.status == 429:  # Rate-limited
                            print(Colorate.Horizontal(Colors.red_to_white, f" [{current_time}] Rate limited!"))
                            await asyncio.sleep(1)  # Short wait to prevent spam
                        else:
                            print(Colorate.Horizontal(Colors.red_to_white, f" Failed: {response.status}"))

    tasks = [send_message(token) for token in tokens]
    await asyncio.gather(*tasks)


async def token_checker():
    try:
        async with aiofiles.open('input/tokens.txt', 'r') as file:
            tokens = [line.strip() for line in await file.readlines() if line.strip()]

        async def check_token(token):
            url = "https://discord.com/api/v9/users/@me"
            headers = {"Authorization": token}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    masked_token = f"{token[:-6]}{Colorate.Horizontal(Colors.red_to_blue, '******')}"
                    token_label = Colorate.Horizontal(Colors.red_to_blue, "Token")
                    if response.status == 200:
                        print(f" {token_label} {masked_token} is {Colorate.Horizontal(Colors.green_to_white, 'VALID')}")
                    else:
                        print(f" {token_label} {masked_token} is {Colorate.Horizontal(Colors.red_to_white, 'INVALID')}")

        tasks = [check_token(token) for token in tokens]
        await asyncio.gather(*tasks)


        input(Colorate.Horizontal(Colors.red_to_blue, "\n Press Enter to return to the menu..."))
        display_logo()

    except FileNotFoundError:
        print(Colorate.Horizontal(Colors.red_to_white, " tokens.txt file not found"))
        input(Colorate.Horizontal(Colors.blue_to_white, "\n Press Enter to return to the menu..."))
        display_logo()


async def thread_spammer():
    client = tls_client.Session()

    with open('input/tokens.txt') as f:
        tokens = f.read().splitlines()

    if not tokens:
        print(Colorate.Horizontal(Colors.red_to_white, " No tokens found in 'tokens.txt'."))
        return

    channel_id = input(Colorate.Horizontal(Colors.red_to_blue, " Enter the channel ID>>"))
    num_threads = int(input(Colorate.Horizontal(Colors.red_to_blue, " Enter the Amount>>")))
    thread_name = input(Colorate.Horizontal(Colors.red_to_blue, " Enter the Name>"))
    message_content = input(Colorate.Horizontal(Colors.red_to_blue, " Enter the Message>>"))
    delay = float(input(Colorate.Horizontal(Colors.red_to_blue, " Enter the Delay>>")))

    headers_template = {'Content-Type': 'application/json'}

    async def create_thread_with_message(token, token_index):
        headers = headers_template.copy()
        headers['Authorization'] = token

        for i in range(num_threads):
            url_create_thread = f"https://discord.com/api/v10/channels/{channel_id}/threads"
            thread_data = {"name": f"{thread_name} #{i+1}", "auto_archive_duration": 1440, "type": 11}
            try:
                response_create_thread = await asyncio.to_thread(client.post, url_create_thread, headers=headers, json=thread_data)

                if response_create_thread.status_code == 429:
                    retry_after = json.loads(response_create_thread.text).get('retry_after', 1)
                    print(Colorate.Horizontal(Colors.red_to_white, f" Rate limited. Retrying after {retry_after} seconds"))
                    await asyncio.sleep(retry_after)
                    return await create_thread_with_message(token, token_index)

                if response_create_thread.status_code == 201:
                    thread_id = json.loads(response_create_thread.text)['id']
                    print(Colorate.Horizontal(Colors.red_to_blue, f" [{i+1}] Created Thread Successfully"))

                    url_send_message = f"https://discord.com/api/v10/channels/{thread_id}/messages"
                    msg_data = {"content": message_content}
                    response_send_message = await asyncio.to_thread(client.post, url_send_message, headers=headers, json=msg_data)

                    if response_send_message.status_code in [200, 201]:
                        print(Colorate.Horizontal(Colors.red_to_blue, f" [{i+1}] Message Sent Successfully"))
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, f" Failed to send message in thread [{thread_name} #{i+1}]"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f" Failed to create thread [{thread_name} #{i+1}]"))

                await asyncio.sleep(delay)

            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, f" Error creating thread '{thread_name} #{i+1}': {e}"))

    tasks = []
    for token_index, token in enumerate(tokens):
        task = create_thread_with_message(token, token_index)
        tasks.append(task)

    await asyncio.gather(*tasks)




async def vc_joiner():
    try:

        if not os.path.exists("input/tokens.txt"):
            print(Colorate.Horizontal(Colors.red_to_white, " tokens.txt file not found in the 'input' folder"))
            return

        with open("input/tokens.txt", "r") as file:
            tokenlist = file.read().splitlines()


        channel = input(Colorate.Horizontal(Colors.red_to_blue, " Voice Channel ID>>")).strip()
        server = input(Colorate.Horizontal(Colors.red_to_blue, " Server ID>>")).strip()
        deaf = input(Colorate.Horizontal(Colors.red_to_blue, " Deafen (y/n)>>")).strip().lower() == "y"
        mute = input(Colorate.Horizontal(Colors.red_to_blue, " Mute (y/n)>>")).strip().lower() == "y"


        async def join_vc(token):
            try:
                async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json") as ws:

                    await ws.send(json.dumps({
                        "op": 2,
                        "d": {
                            "token": token,
                            "properties": {
                                "$os": "windows",
                                "$browser": "discord",
                                "$device": "desktop"
                            }
                        }
                    }))

                    # Join the voice channel
                    await ws.send(json.dumps({
                        "op": 4,
                        "d": {
                            "guild_id": server,
                            "channel_id": channel,
                            "self_mute": mute,
                            "self_deaf": deaf
                        }
                    }))


                    print(Colorate.Horizontal(Colors.red_to_blue, f" [+] Token {token[-6:]} joined VC successfully"))
                    await asyncio.sleep(10)

            except websockets.exceptions.ConnectionClosed as e:
                print(Colorate.Horizontal(Colors.red_to_white, f" [-] Token {token[-6:]} disconnected: {e}"))
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, f" [-] Token {token[-6:]} error joining VC: {e}"))


        tasks = [join_vc(token) for token in tokenlist]
        await asyncio.gather(*tasks)

    except FileNotFoundError:
        print(Colorate.Horizontal(Colors.red_to_white, " tokens.txt file not found"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f" An error occurred: {e}"))




async def main_menu():
    while True:
        display_logo()
        choice = input(Colorate.Horizontal(Colors.red_to_blue, " Vasily@User>>")).strip().lower()

        if choice == "help":
            display_help_menu()
            option = input(Colorate.Horizontal(Colors.red_to_blue, " Vasily@User>>"))

            if option == "1":
                display_logo()
                print(Colorate.Horizontal(Colors.blue_to_purple, " Starting Channel Spammer..."))
                await channel_spammer()
            elif option == "2":
                print(Colorate.Horizontal(Colors.blue_to_purple, " Starting Thread Spammer..."))
                await thread_spammer()
            elif option == "3":
                print(Colorate.Horizontal(Colors.blue_to_purple, " Starting Token Checker..."))
                await token_checker()
            elif option == "4":
                print(Colorate.Horizontal(Colors.blue_to_purple, " Starting VC Joiner..."))
                await vc_joiner()
            else:
                print(Colorate.Horizontal(Colors.red_to_white, " Invalid option! Returning to main menu..."))
                await asyncio.sleep(1)
        elif choice == "exit":
            print(Colorate.Horizontal(Colors.red_to_blue, " Goodbye!"))
            break
        else:
            print(Colorate.Horizontal(Colors.red_to_white, " Invalid input! Try again."))


if __name__ == "__main__":
    asyncio.run(main_menu())

