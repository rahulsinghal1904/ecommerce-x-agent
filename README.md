# E-commerce Agent Automation Script

 The script, contained in `agent.py`, implements multiple automation approaches and advanced features including:

- **Level 1: Playwright Automation** for browser-based tasks (login, product search, cart interaction).
- **Level 2: Native Browser Integration** using AppleScript on macOS and the DevTools Protocol on Windows/Linux.
- **Level 3: Interactive & Scheduled Modes** offering a command-line interface for manual commands and a scheduling mechanism for periodic execution.
- **Bonus Enhancements** such as CAPTCHA detection, session management, dynamic content waiting, and graceful error recovery.
- **Proxy & Extension Support** to allow routing traffic through a proxy and loading custom Chrome extensions.

## Table of Contents

- [Overview](#overview)
- [Functionalities](#functionalities)
  - [Level 1: Playwright Automation](#level-1-playwright-automation)
  - [Level 2: Native Browser Integration](#level-2-native-browser-integration)
  - [Level 3: Interactive & Scheduled Modes](#level-3-interactive--scheduled-modes)
  - [Bonus Enhancements](#bonus-enhancements)
  - [Proxy and Extension Support](#proxy-and-extension-support)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [How to Test](#how-to-test)
  - [Playwright Mode (Level 1)](#playwright-mode-level-1)
  - [Native Mode (Level 2)](#native-mode-level-2)
  - [Interactive & Scheduled Mode (Level 3)](#interactive--scheduled-mode-level-3)
  - [Testing Bonus Features](#testing-bonus-features)
- [Reference to CRUSTDATA Assignment](#reference-to-crustdata-assignment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The `agent.py` script automates tasks on the Demoblaze website including:

- **Login:** Automates user login using credentials loaded from a configuration file.
- **Product Search & Cart Interaction:** Searches for a product in the "Phones" category based on a configurable search term and adds it to the cart.
- **Cross-Platform Automation:** Supports both browser automation (via Playwright) and native automation (using AppleScript/DevTools).
- **Interactive & Scheduled Modes:** Offers an interactive CLI for manual testing and a scheduling mechanism for periodic execution.
- **Bonus Features:** Integrates CAPTCHA detection, session management, dynamic content waiting, and graceful error recovery.
- **Proxy & Extension Support:** Provides options to route traffic through a proxy and load custom Chrome extensions.

## Functionalities

### Level 1: Playwright Automation
- **Browser Automation:**  
  Uses Playwright to launch a Chromium browser, navigate to Demoblaze, and perform login, product search, and cart interactions.
- **Dynamic Content & Recovery:**  
  Waits for essential page elements to load and attempts graceful recovery from errors.
- **Session Management:**  
  Saves session cookies for reuse.

### Level 2: Native Browser Integration
- **AppleScript (macOS):**  
  Launches Chrome via AppleScript to handle login, search, and product detail extraction.
- **DevTools Protocol (Windows/Linux):**  
  Uses remote debugging via WebSocket to control Chrome for login and product search.

### Level 3: Interactive & Scheduled Modes
- **Interactive Conversation:**  
  Provides a CLI where you can type commands such as `login` or `search iPhone` to execute specific actions.
- **Scheduled Execution:**  
  Uses the `schedule` module to run automation tasks at regular intervals (default: every minute).

### Bonus Enhancements
- **CAPTCHA Detection:**  
  Checks for CAPTCHA keywords on the page and prompts for manual resolution.
- **Session Management:**  
  Saves and loads session cookies to maintain login sessions.
- **Dynamic Content Waiting:**  
  Waits for specific page elements to load before proceeding.
- **Graceful Recovery:**  
  Attempts to reload the page in case of errors.

### Proxy and Extension Support
- **Proxy:**  
  Use the `--proxy` command-line argument to specify a proxy server (e.g., `http://my-proxy.example:8080`).
- **Extension:**  
  Use the `--extension` argument to provide a path to an unpacked Chrome extension that will be loaded by the browser.

## Installation and Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Install Required Dependencies:**
    
```bash
    pip install playwright websocket-client python-dotenv schedule beautifulsoup4
    playwright install
```

## Configuration

Create a .env file in the project root with the following content:

```bash
    DEMOBLAZE_USER=your_username
    DEMOBLAZE_PASS=your_password
    DEMOBLAZE_SEARCH=search_name
```

Replace your_username and your_password with your actual Demoblaze credentials. Modify DEMOBLAZE_SEARCH as needed.

## Usage

The script is contained in agent.py and accepts several command-line arguments:

--mode: Select the automation mode. Options: level1 (Level 1), level2 (Level 2), level3 (Level 3, interactive/scheduled).

--proxy: (Optional) Specify a proxy server (e.g., http://my-proxy.example:8080).

--extension: (Optional) Provide the path to an unpacked Chrome extension.

--schedule-only: (For level3 mode) Run only the periodic task scheduling loop.

Example Commands

```bash
    #Playwright Mode (Level1):
    python3 agent.py --mode=level1

    #Native Mode (Level 2):
    python3 agent.py --mode=level2

    #Interactive Conversation Mode (Level 3):
    python3 agent.py --mode=level3

    #Scheduled Execution (Level 3):
    python3 agent.py --mode=level3 --schedule-only

    #Using Proxy and Extension:
    python3 agent.py --mode=playwright --proxy="http://my-proxy.example:8080" --extension="/path/to/extension"
```

## How to Test

### Playwright Mode (Level 1)

Run the Script:

```bash
    python3 agent.py --mode=level1
```

Expected Behavior:

A Chromium browser window opens.

The script navigates to Demoblaze and checks for a CAPTCHA. If detected, you will be prompted to solve it.

The script logs in using credentials from your .env file.

It waits for dynamic content (e.g., the user's name) to confirm login.

The product specified by DEMOBLAZE_SEARCH is searched and added to the cart.

Session cookies are saved to session.json.

### Native Mode (Level 2)

```bash
    For macOS (AppleScript):

    python3 agent.py --mode=level2

    #For Windows/Linux (DevTools Protocol):

    python3 agent.py --mode=level2
```

Expected Behavior:

On macOS, Chrome is launched via AppleScript.

On Windows/Linux, Chrome launches with remote debugging enabled.

The script logs in and searches for the specified product using credentials from your .env file.

### Interactive & Scheduled Mode (Level 3)

Interactive Conversation
Run:

```bash
    python3 agent.py --mode=level3
```
Expected Behavior:

A command-line prompt appears.

Type login to execute the login steps.

Type search iPhone to search for a product named "iPhone".

Type exit to terminate the conversation.

Scheduled Execution
Run:

```bash
python3 agent.py --mode=level3 --schedule-only
```

Expected Behavior:

The Playwright automation flow runs periodically (default every minute).

Console messages indicate each periodic execution.

### Testing Bonus Features

CAPTCHA Detection:
The script automatically checks for CAPTCHA keywords on page load. To test, simulate a CAPTCHA (or modify page content to include "captcha") and observe the prompt.

Session Management:
After a successful login, verify that session.json is created and contains session cookies.

Dynamic Content Waiting:
Test under conditions where elements load slowly (e.g., by throttling your network) to ensure the script waits for key selectors.

Graceful Recovery:
Force an error (e.g., by temporarily disconnecting your network) and check that the script attempts to reload the page.

## Reference to CRUSTDATA Assignment

This project was developed to meet the requirements of the CRUSTDATA assignment, which specified:

A multi-level automation solution combining both browser-based (Playwright) and native (AppleScript/DevTools) integrations.

An interactive command-line interface for manual testing.

A scheduling mechanism for periodic execution.

Robustness features including CAPTCHA detection, session management, dynamic content handling, and graceful error recovery.

Support for proxy routing and loading custom browser extensions.

All functionalities have been implemented to meet these requirements.

## Troubleshooting

Environment Variables Not Loaded:
Ensure the .env file is in the same directory as agent.py and that you run the script from that directory.

Dependency Issues:
Verify installation with:

Browser Launch Problems:
If Chrome fails to launch, check its installation path or update the script configuration accordingly.

Proxy/Extension Issues:
Confirm that the proxy URL and extension path provided with --proxy and --extension are correct.

Error Messages:
Check console output and any generated screenshots (e.g., login_failure.png) for troubleshooting details.

## License
This project is licensed under the MIT License.


