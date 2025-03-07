# Show-Saved-WiFi 🌐🔑

**Extract and manage saved Wi-Fi profiles on Windows with ease!**

Welcome to **Show-Saved-WiFi**, a simple yet powerful Python tool designed to retrieve saved Wi-Fi profile information on Windows systems, including SSIDs and passwords (if available). It also supports saving to a file and sending results to Telegram (optional), all with a colorful, user-friendly interface!

📌 **Repository**: [Show-Saved-WiFi](https://github.com/Mysteriza/Show-Saved-WiFi) 

---

## ✨ Key Features

| Icon | Feature              | Description                                                                 |
|------|----------------------|-----------------------------------------------------------------------------|
| 🌐   | **Extract Wi-Fi Profiles** | Retrieves a list of all saved Wi-Fi profiles on Windows using `netsh wlan`. |
| 🔑   | **Show Passwords**       | Displays Wi-Fi passwords (if available) in clear text with `key=clear`.    |
| 🎨   | **Colored Display**      | Uses `colorama` for an attractive and readable console output.             |
| 💾   | **Save to File**         | Saves results to a text file with a timestamp (e.g., `wifi_profiles_1430.txt`). |
| 📤   | **Send to Telegram**     | Sends results to Telegram via a bot (optional, with token and chat ID setup). |
| ✂️   | **Message Splitting**    | Splits long messages to fit Telegram’s 2000-character limit.               |
| 🛡️   | **Windows Compatibility** | Built specifically for Windows with platform checking.                    |
| 🚀   | **Error Handling**       | Handles errors like subprocess failures or Telegram issues with clear messages. |

---

## 🛠️ How to Use

1. **Prerequisites**  
   Ensure you have Python 3.x installed and the following dependencies:
   ```bash
   pip install colorama telebot
   ```
2. Run the program
   Clone this repo and run:
   ```
   git clone https://github.com/Mysteriza/Show-Saved-WiFi.git && cd Show-Saved-WiFi
   ```
   Run wifiRecovery.exe file.
## Example Output
```
Wi-Fi Profiles
========================================
SSID: MyHomeWiFi
Password: Secret123
----------------------------------------
SSID: OfficeNet
Password: None
----------------------------------------
```
