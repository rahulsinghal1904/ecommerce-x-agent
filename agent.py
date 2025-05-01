#!/usr/bin/env python3


import asyncio
import os
import random
import subprocess
import time
import sys
import tempfile
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
from security import safe_requests

load_dotenv()

# For scheduling (Level 3 periodic tasks)
import schedule

# For cross-platform checks
import platform

# For DevTools approach on Windows/Linux
import websocket  # pip install websocket-client

from playwright.async_api import async_playwright

# Bonus Enhancements for the Automation Challenge

class BonusAutomationFeatures:
    @staticmethod
    async def detect_captcha(page):
        """Detect if a CAPTCHA is present on the page."""
        try:
            content = await page.content()
            if "captcha" in content.lower():
                print("⚠️ CAPTCHA detected on the page. Please solve it manually.")
                return True
            return False
        except Exception as e:
            print(f"Error detecting CAPTCHA: {e}")
            return False

    @staticmethod
    def save_session(cookies, session_file="session.json"):
        """Save session cookies to a file."""
        try:
            with open(session_file, "w") as f:
                json.dump(cookies, f)
            print(f"Session cookies saved to {session_file}")
        except Exception as e:
            print(f"Failed to save session cookies: {e}")

    @staticmethod
    def load_session(session_file="session.json"):
        """Load session cookies from a file, if available."""
        if os.path.exists(session_file):
            try:
                with open(session_file, "r") as f:
                    cookies = json.load(f)
                print(f"Session cookies loaded from {session_file}")
                return cookies
            except Exception as e:
                print(f"Failed to load session cookies: {e}")
        return None

    @staticmethod
    async def wait_for_dynamic_content(page, selector, timeout=30000):
        """Wait for dynamic content to load based on a selector."""
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            print(f"Dynamic content loaded for selector: {selector}")
        except Exception as e:
            print(f"Timeout waiting for dynamic content for selector '{selector}': {e}")

    @staticmethod
    async def graceful_recovery(page, recovery_message="Attempting graceful recovery..."):
        """Attempt graceful recovery from an unexpected page state."""
        print(recovery_message)
        try:
            await page.reload(wait_until="domcontentloaded")
            print("Page reloaded successfully.")
        except Exception as e:
            print(f"Graceful recovery failed: {e}")

# Level 1: Playwright Automation (BrowserAgent)
class BrowserAgent:
    def __init__(self, proxy: str = None):
        """Initialize with an optional proxy."""
        self.playwright = None
        self.browser = None
        self.page = None
        self.proxy = proxy

    async def initialize(self):
        """Initialize browser with anti-detection measures."""
        launch_args = [
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage"
        ]
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=launch_args,
            slow_mo=random.randint(100, 500)
        )
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({"width": 1366, "height": 768})

    async def navigate_with_retry(self, url: str, max_retries: int = 3):
        """Navigate to a URL with retry logic."""
        for attempt in range(max_retries):
            try:
                print(f"Navigation attempt {attempt + 1}/{max_retries}")
                await self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                return True
            except Exception as e:
                print(f"Navigation failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        return False

    async def login(self, username: str, password: str):
        """Log into the website using selectors and bonus enhancements."""
        if not username or not password:
            raise ValueError("DEMOBLAZE_USER and DEMOBLAZE_PASS must be set in your environment (.env).")
        try:
            if not await self.navigate_with_retry("https://www.demoblaze.com"):
                raise RuntimeError("Failed to navigate to the website.")

            # BONUS: Check for CAPTCHA presence
            if await BonusAutomationFeatures.detect_captcha(self.page):
                print("CAPTCHA detected. Please solve it manually, then press Enter to continue.")
                input("Press Enter after CAPTCHA is solved...")
            
            # Open login modal and perform login
            await self.page.click("#login2")
            await self.page.wait_for_selector("#logInModal.show", timeout=15000)
            await self.page.fill("#loginusername", username)
            await self.page.fill("#loginpassword", password)
            await self.page.click("button:has-text('Log in')")
            # Wait for dynamic content (i.e., login confirmation)
            await BonusAutomationFeatures.wait_for_dynamic_content(self.page, "#nameofuser")
            print("✓ Login sequence completed successfully (Playwright)")

            # BONUS: Save session cookies after login
            cookies = await self.page.context.cookies()
            BonusAutomationFeatures.save_session(cookies)
        except Exception as e:
            # BONUS: Attempt graceful recovery before re-raising the error
            await BonusAutomationFeatures.graceful_recovery(self.page, "Login error encountered. Reloading page...")
            await self.page.screenshot(path="login_failure.png")
            raise RuntimeError(f"Login failed: {str(e)}")

    async def select_product_and_interact(self, search_term: str):
        """
        Select a product containing `search_term` in its title under the 'Phones' category 
        and interact with it (add to cart), using bonus enhancements.
        """
        try:
            await self.page.click("a#itemc:has-text('Phones')")
            # BONUS: Wait for the product listing to load dynamically.
            await BonusAutomationFeatures.wait_for_dynamic_content(self.page, "#tbodyid")
            product_cards = await self.page.query_selector_all("#tbodyid .card-title")
            for card in product_cards:
                text = await card.inner_text()
                if search_term.lower() in text.lower():
                    parent_card = await card.query_selector("xpath=ancestor::div[contains(@class, 'card')]")
                    await parent_card.click()
                    # Wait for product details to load.
                    await BonusAutomationFeatures.wait_for_dynamic_content(self.page, ".name")
                    product_name = await self.page.inner_text(".name")
                    product_price = await self.page.inner_text(".price-container")
                    print(f"Product Name: {product_name}")
                    print(f"Product Price: {product_price}")
                    await self.page.click("a:has-text('Add to cart')")
                    print("✓ Product added to cart successfully (Playwright)")
                    await asyncio.sleep(2)
                    await self.page.click("a:has-text('Cart')")
                    await self.page.wait_for_selector("#tbodyid .success", timeout=15000)
                    print("✓ Verified item in the cart (Playwright)")
                    return
            raise RuntimeError(f"No product found matching '{search_term}'.")
        except Exception as e:
            # BONUS: Attempt graceful recovery before re-raising the error.
            await BonusAutomationFeatures.graceful_recovery(self.page, "Product interaction error. Reloading page...")
            await self.page.screenshot(path="interaction_error.png")
            raise RuntimeError(f"Interaction failed: {str(e)}")

    async def execute_flow(self):
        """
        Execute the full Playwright automation workflow.
        Accepts a search term from DEMOBLAZE_SEARCH (default "Samsung").
        Integrates bonus features for CAPTCHA detection, session management,
        dynamic content waiting, and graceful recovery.
        """
        try:
            await self.initialize()
            username = os.getenv("DEMOBLAZE_USER")
            password = os.getenv("DEMOBLAZE_PASS")
            await self.login(username, password)
            search_term = os.getenv("DEMOBLAZE_SEARCH", "Samsung")
            await self.select_product_and_interact(search_term)
        except Exception as e:
            print(f"\n❌ CRITICAL FAILURE (Playwright): {str(e)}")
        finally:
            if self.browser:
                await self.browser.close()
                if self.playwright:
                    await self.playwright.stop()


# Level 2: Native Browser Integration (AppleScript/DevTools)
class AppleScriptNativeAgent:
    def __init__(self, browser: str = "chrome", proxy: str = None, extension_path: str = None):
        self.browser = browser.lower()
        self.proxy = proxy
        self.extension_path = extension_path

    def execute_js(self, js_command: str):
        safe_js = js_command.replace('"', '\\"')
        script = f'''tell application "Google Chrome"
    activate
    delay 2
    tell front window to set theTab to active tab
    tell theTab
        execute JavaScript "{safe_js}"
    end tell
end tell'''
        with tempfile.NamedTemporaryFile(mode="w", suffix=".applescript", delete=False) as f:
            script_path = f.name
            f.write(script)
        result = subprocess.run(["osascript", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.remove(script_path)
        if result.returncode != 0:
            raise RuntimeError(f"AppleScript command failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def execute_js_extract(self, js_command: str):
        safe_js = js_command.replace('"', '\\"')
        script = f'''tell application "Google Chrome"
            activate
            delay 2
            tell front window to set theTab to active tab
            tell theTab
                set jsResult to execute JavaScript "({safe_js})"
            end tell
        end tell
        return jsResult'''
        with tempfile.NamedTemporaryFile(mode="w", suffix=".applescript", delete=False) as f:
            script_path = f.name
            f.write(script)
        result = subprocess.run(["osascript", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.remove(script_path)
        if result.returncode != 0:
            raise RuntimeError(f"AppleScript command failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def wait_for_element(self, js_selector: str, timeout=2):
        check_js = f"(function() {{ return !!document.querySelector('{js_selector}'); }})()"
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                output = self.execute_js(check_js)
                if "true" in output.lower():
                    return True
            except RuntimeError as e:
                print(f"Waiting for element error: {e}")
            time.sleep(1)
        return False

    def launch_browser(self, url: str):
        print("Launching Chrome in native mode (macOS)...")
        executable = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cmd = [executable, "--new-window", url]
        if self.proxy:
            proxy_clean = self.proxy.replace("http://", "").replace("https://", "")
            cmd.extend([f"--proxy-server=http={proxy_clean};https={proxy_clean}",
                        "--user-data-dir=/tmp/chrome-proxy-test",
                        "--proxy-bypass-list=<-loopback>"])
        if self.extension_path:
            cmd.append(f"--load-extension={self.extension_path}")
        print(f"Using command: {' '.join(cmd)}")
        subprocess.Popen(cmd)
        print("Waiting for Chrome to open...")
        time.sleep(10)
        subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to activate'])
        time.sleep(3)
        print("Browser window should now be in focus (macOS).")

    def login_only(self, url: str, username: str, password: str):
        self.launch_browser(url)
        print("Attempting to click the login button (login_only)...")
        if not self.wait_for_element("#login2", timeout=5):
            print("Error: Login button (#login2) not found within timeout.")
            return
        self.execute_js('document.querySelector("#login2").click();')
        time.sleep(3)
        print("Filling credentials (login_only)...")
        if not self.wait_for_element("#loginusername", timeout=5):
            print("Login modal (#loginusername) not found within timeout.")
            return
        self.execute_js(f'document.getElementById("loginusername").value = "{username}";')
        self.execute_js(f'document.getElementById("loginpassword").value = "{password}";')
        self.execute_js("""
            var loginButton = document.querySelector('button.btn.btn-primary[onclick="logIn()"]');
            if (loginButton) { loginButton.click(); }
        """)
        print("✓ AppleScript: Completed login_only steps.")

    def search_only(self, search_term: str):
        self.launch_browser("https://www.demoblaze.com")
        time.sleep(3)
        print("Navigating to phones category (search_only)...")
        self.execute_js("""
            var phonesLink = document.querySelector('#itemc');
            if (phonesLink) { phonesLink.click(); }
        """)
        time.sleep(3)
        print(f"Searching for {search_term} (search_only)...")
        self.execute_js(f"""
            var elems = document.querySelectorAll('#tbodyid .card-title a');
            for (var i = 0; i < elems.length; i++) {{
                if (elems[i].innerText.toLowerCase().includes('{search_term.lower()}')) {{
                    elems[i].click();
                    break;
                }}
            }}
        """)
        time.sleep(3)
        print("Extracting product details (search_only) ...")
        result = self.execute_js_extract("""
            (function() {
                var name = document.querySelector('.name') ? document.querySelector('.name').innerText : 'No name found';
                var price = document.querySelector('.price-container') ? document.querySelector('.price-container').innerText : 'No price found';
                var description = document.querySelector('#more-information p') ? document.querySelector('#more-information p').innerText : 'No description found';
                return JSON.stringify({name: name, price: price, description: description});
            })()
        """)
        if result:
            try:
                data = json.loads(result)
                print("AppleScript: search_only extracted data:", data)
            except json.JSONDecodeError:
                print("Failed to parse product data in search_only.")
        else:
            print("No data extracted in search_only.")

    def complete_flow(self, url: str, username: str, password: str, search_term: str):
        self.launch_browser(url)
        print("Attempting to click the login button...")
        if not self.wait_for_element("#login2", timeout=2):
            print("Error: Login button (#login2) not found within timeout.")
            return
        self.execute_js('document.querySelector("#login2").click();')
        time.sleep(3)
        print("Performing native login using AppleScript and JavaScript...")
        if not self.wait_for_element("#loginusername", timeout=2):
            print("Login modal (#loginusername) not found within timeout.")
            return
        self.execute_js(f'document.getElementById("loginusername").value = "{username}";')
        self.execute_js(f'document.getElementById("loginpassword").value = "{password}";')
        self.execute_js("""
            var loginButton = document.querySelector('button.btn.btn-primary[onclick="logIn()"]');
            if (loginButton) { loginButton.click(); }
        """)
        time.sleep(3)
        print("Navigating to phones category...")
        self.execute_js("""
            var phonesLink = document.querySelector('#itemc');
            if (phonesLink) { phonesLink.click(); }
        """)
        time.sleep(2)
        print(f"Searching for {search_term} product...")
        self.execute_js(f"""
            var elems = document.querySelectorAll('#tbodyid .card-title a');
            for (var i = 0; i < elems.length; i++) {{
                if (elems[i].innerText.toLowerCase().includes('{search_term.lower()}')) {{
                    elems[i].click();
                    break;
                }}
            }}
        """)
        time.sleep(3)
        print("Extracting product details (AppleScript JS) ...")
        result = self.execute_js_extract("""
            (function() {
                var name = document.querySelector('.name') ? document.querySelector('.name').innerText : 'No name found';
                var price = document.querySelector('.price-container') ? document.querySelector('.price-container').innerText : 'No price found';
                var description = document.querySelector('#more-information p') ? document.querySelector('#more-information p').innerText : 'No description found';
                return JSON.stringify({name: name, price: price, description: description});
            })()
        """)
        if result:
            try:
                data = json.loads(result)
                print("Extracted Data (macOS AppleScript):", data)
            except json.JSONDecodeError:
                print("Failed to parse product data.")
        else:
            print("No data extracted.")


class WindowsLinuxNativeAgent:
    def __init__(self, browser: str = "chrome", proxy: str = None, extension_path: str = None):
        self.browser = browser.lower()
        self.proxy = proxy
        self.extension_path = extension_path
        self.chrome_process = None
        self.debug_port = 9222
        self.ws = None

    def launch_browser(self, url: str):
        if platform.system().lower() == "windows":
            executable = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        else:
            executable = "google-chrome"
        cmd = [
            executable,
            f"--remote-debugging-port={self.debug_port}",
            "--new-window",
            url
        ]
        if self.proxy:
            proxy_clean = self.proxy.replace("http://", "").replace("https://", "")
            cmd.extend([f"--proxy-server=http={proxy_clean};https={proxy_clean}",
                        "--user-data-dir=/tmp/chrome-proxy-test",
                        "--proxy-bypass-list=<-loopback>"])
        if self.extension_path:
            cmd.append(f"--load-extension={self.extension_path}")
        print(f"Launching Chrome for Windows/Linux with command: {' '.join(cmd)}")
        self.chrome_process = subprocess.Popen(cmd)
        time.sleep(5)
        try:
            resp = safe_requests.get(f"http://127.0.0.1:{self.debug_port}/json")
            targets = resp.json()
            if targets:
                ws_url = targets[0].get("webSocketDebuggerUrl", None)
                if ws_url:
                    self.ws = websocket.create_connection(ws_url)
                    print("Connected to DevTools WebSocket.")
                else:
                    print("No webSocketDebuggerUrl found in /json response.")
            else:
                print("No targets returned from /json endpoint.")
        except Exception as e:
            print(f"Could not connect to DevTools: {e}")

    def devtools_send(self, method: str, params: dict = None):
        if not self.ws:
            print("No WebSocket connection to DevTools available.")
            return
        if params is None:
            params = {}
        msg_id = int(time.time())
        payload = {
            "id": msg_id,
            "method": method,
            "params": params
        }
        self.ws.send(json.dumps(payload))
        response = self.ws.recv()
        return response

    def devtools_evaluate(self, expression: str):
        params = {
            "expression": expression,
            "returnByValue": True
        }
        resp = self.devtools_send("Runtime.evaluate", params)
        return resp

    def close_browser(self):
        if self.ws:
            self.ws.close()
        if self.chrome_process:
            self.chrome_process.terminate()
            print("Closed Chrome (Windows/Linux remote debugging).")

    def login_only(self, url: str, username: str, password: str):
        self.launch_browser(url)
        time.sleep(2)
        self.devtools_evaluate("document.querySelector('#login2')?.click();")
        time.sleep(2)
        fill_js = f"""
            document.getElementById('loginusername').value = '{username}';
            document.getElementById('loginpassword').value = '{password}';
            let btn = document.querySelector('button.btn.btn-primary[onclick="logIn()"]');
            if (btn) btn.click();
        """
        self.devtools_evaluate(fill_js)
        print("✓ WindowsLinuxNativeAgent: login_only steps done.")

    def search_only(self, search_term: str):
        self.launch_browser("https://www.demoblaze.com")
        time.sleep(2)
        self.devtools_evaluate("document.querySelector('#itemc')?.click();")
        time.sleep(2)
        search_js = f"""
            let items = document.querySelectorAll('#tbodyid .card-title a');
            for (let i=0; i < items.length; i++) {{
                if (items[i].innerText.toLowerCase().includes('{search_term.lower()}')) {{
                    items[i].click();
                    break;
                }}
            }}
        """
        self.devtools_evaluate(search_js)
        time.sleep(3)
        extract_js = """
        JSON.stringify({
            name: document.querySelector('.name')?.innerText || 'No name',
            price: document.querySelector('.price-container')?.innerText || 'No price',
            description: document.querySelector('#more-information p')?.innerText || 'No description'
        })
        """
        resp = self.devtools_evaluate(extract_js)
        print("WindowsLinuxNativeAgent search_only response:", resp)
        self.close_browser()

    def complete_flow(self, url: str, username: str, password: str, search_term: str):
        print(f"Starting native flow for {platform.system().lower()} ...")
        self.launch_browser(url)
        time.sleep(2)
        self.devtools_evaluate("document.querySelector('#login2')?.click();")
        time.sleep(2)
        fill_creds_js = f"""
            document.getElementById('loginusername').value = '{username}';
            document.getElementById('loginpassword').value = '{password}';
            let btn = document.querySelector('button.btn.btn-primary[onclick="logIn()"]');
            if (btn) btn.click();
        """
        self.devtools_evaluate(fill_creds_js)
        time.sleep(3)
        self.devtools_evaluate("document.querySelector('#itemc').click();")
        time.sleep(2)
        search_js = f"""
            var items = document.querySelectorAll('#tbodyid .card-title a');
            for (var i=0; i<items.length; i++) {{
                if (items[i].innerText.toLowerCase().includes('{search_term.lower()}')) {{
                    items[i].click();
                    break;
                }}
            }}
        """
        self.devtools_evaluate(search_js)
        time.sleep(3)
        extract_js = """
        JSON.stringify({
            name: document.querySelector('.name')?.innerText || 'No name',
            price: document.querySelector('.price-container')?.innerText || 'No price',
            description: document.querySelector('#more-information p')?.innerText || 'No description'
        })
        """
        extract_resp = self.devtools_evaluate(extract_js)
        print("DevTools Evaluate Response:", extract_resp)
        self.close_browser()


# LEVEL 3: CROSS-PLATFORM + SCHEDULING + CONVERSATION
class ConversationAgent:
    def __init__(self):
        self.context = {}
        self.history = []

    def handle_command(self, command: str) -> str:
        self.history.append(command)
        lower_cmd = command.lower()
        if "login" in lower_cmd:
            self.context["action"] = "login"
            return "Understood, I'll just do login steps next."
        elif "search" in lower_cmd:
            parts = command.split("search", 1)
            if len(parts) > 1:
                term = parts[1].strip()
                self.context["search_term"] = term
                self.context["action"] = "search"
                return f"Okay, I'll just search for '{term}' next."
            else:
                return "Could not parse a search term, e.g. 'search Samsung'."
        elif "exit" in lower_cmd:
            return "exit"
        else:
            return "I didn't understand. Try 'login', 'search <something>', or 'exit'."

    def get_context(self):
        return self.context

    def clear_context(self):
        self.context.clear()
        self.history.clear()

class Level3Agent:
    def __init__(self):
        self.conv_agent = ConversationAgent()
        self.os_type = platform.system().lower()

    def pick_native_agent(self, proxy=None, extension_path=None):
        if self.os_type == "darwin":
            return AppleScriptNativeAgent(proxy=proxy, extension_path=extension_path)
        elif self.os_type in ["windows", "linux"]:
            return WindowsLinuxNativeAgent(proxy=proxy, extension_path=extension_path)
        else:
            print("Unsupported OS for native integration.")
            return None

    def run_conversation_loop(self, proxy=None, extension_path=None):
        agent = self.pick_native_agent(proxy, extension_path)
        if not agent:
            print("No suitable native agent found for your OS.")
            return
        print("\nEnter commands:\n - 'login' => do only the login steps\n - 'search Samsung' => do only the search steps\n - 'exit' => quit\n")
        while True:
            user_input = input("You> ")
            resp = self.conv_agent.handle_command(user_input)
            if resp == "exit":
                print("Conversation ended.")
                break
            print("Agent:", resp)
            ctx = self.conv_agent.get_context()
            if ctx.get("action") == "login":
                username = os.getenv("DEMOBLAZE_USER")
                password = os.getenv("DEMOBLAZE_PASS")
                if not username or not password:
                    print("Error: DEMOBLAZE_USER and DEMOBLAZE_PASS must be set in your environment (.env).")
                    break
                agent.login_only("https://www.demoblaze.com", username, password)
                self.conv_agent.clear_context()
            elif ctx.get("action") == "search":
                term = ctx.get("search_term", "Samsung")
                agent.search_only(term)
                self.conv_agent.clear_context()

    def run_periodic_task(self):
        print("\n[Periodic Task] Running Level 1 (Playwright) flow.\n")
        agent = BrowserAgent()
        asyncio.run(agent.execute_flow())

    def schedule_periodic_tasks(self, interval_minutes=1):
        schedule.every(interval_minutes).minutes.do(self.run_periodic_task)
        print(f"Scheduling periodic tasks every {interval_minutes} minute(s).")
        while True:
            schedule.run_pending()
            time.sleep(1)


# ===============================
# Main Entry Point
# ===============================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Choose automation mode.")
    parser.add_argument("--mode", choices=["level1", "level2", "level3"], default="level1",
                        help=("Select 'level1' for Playwright automation (Level 1), "
                              "'level2' for native integration (Level 2), or "
                              "'level3' for conversation & scheduling (Level 3)."))
    parser.add_argument("--proxy", default=None, help="Proxy server to use, e.g. http://my-proxy.example:8080")
    parser.add_argument("--extension", default=None, help="Path to an unpacked Chrome extension folder (for native mode).")
    parser.add_argument("--schedule-only", action="store_true",
                        help="If passed with --mode=level3, runs only the periodic task scheduling loop.")
    args = parser.parse_args()
    if args.mode == "level1":
        print("Running Level 1: Playwright Automation Flow")
        agent = BrowserAgent(proxy=args.proxy)
        asyncio.run(agent.execute_flow())
    elif args.mode == "level2":
        print("Running Level 2: Native Browser Integration")
        sys_os = platform.system().lower()
        if sys_os == "darwin":
            print(" -> Using AppleScriptNativeAgent (macOS)")
            native_agent = AppleScriptNativeAgent(browser="chrome", proxy=args.proxy, extension_path=args.extension)
        elif sys_os in ["windows", "linux"]:
            print(f" -> Using WindowsLinuxNativeAgent on {sys_os}")
            native_agent = WindowsLinuxNativeAgent(browser="chrome", proxy=args.proxy, extension_path=args.extension)
        else:
            print(f"Unsupported OS: {sys_os}")
            sys.exit(1)
        username = os.getenv("DEMOBLAZE_USER")
        password = os.getenv("DEMOBLAZE_PASS")
        if not username or not password:
            print("Error: DEMOBLAZE_USER and DEMOBLAZE_PASS must be set in your environment (.env).")
            sys.exit(1)
        search_term = os.getenv("DEMOBLAZE_SEARCH", "Samsung")
        native_agent.complete_flow(url="https://www.demoblaze.com", username=username,
                                     password=password, search_term=search_term)
    elif args.mode == "level3":
        print("Running Level 3: Cross-Platform + Periodic + Conversational")
        level3 = Level3Agent()
        if args.schedule_only:
            level3.schedule_periodic_tasks(interval_minutes=1)
        else:
            level3.run_conversation_loop(proxy=args.proxy, extension_path=args.extension)
