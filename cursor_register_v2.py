import os
import re
import csv
import copy
import queue
import argparse
import threading
import concurrent.futures
from faker import Faker
from datetime import datetime
from DrissionPage import ChromiumOptions, Chromium

from helper.cursor_register import CursorRegister
from helper.email.gmail_pm import Gmailpm
from helper.email import EmailServer

# Parameters for debugging purpose
hide_account_info = os.getenv('HIDE_ACCOUNT_INFO', 'false').lower() == 'true'
enable_headless = os.getenv('ENABLE_HEADLESS', 'false').lower() == 'true'
enable_browser_log = os.getenv('ENABLE_BROWSER_LOG', 'true').lower() == 'true' or not enable_headless

def register_cursor_core(options):

    try:
        # Maybe fail to open the browser
        browser = Chromium(options)
    except Exception as e:
        print(e)
        return None

    # Use gmail.pm as email server
    email_server = Gmailpm(browser)

    # Get email address
    email = email_server.get_email_address()

    register = CursorRegister(browser, email_server)
    #tab_signin, status = register.sign_in(email)
    tab_signin, status, password = register.sign_up(email)

    token = register.get_cursor_cookie(tab_signin)

    if status or not enable_browser_log:
        register.browser.quit(force=True, del_data=True)

    if status and not hide_account_info:
        print(f"[Kayıt] Cursor E-posta: {email}")
        print(f"[Kayıt] Cursor Şifre: {password}")
        print(f"[Kayıt] Cursor Token: {token}")

    ret = {
        "email": email,
        "password": password,
        "token": token
    }

    return ret

def register_cursor(number, max_workers):

    options = ChromiumOptions()
    options.auto_port()
    options.new_env()
    # Linux için ek ayarlar
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    options.set_argument('--headless=new')
    # Snap paketi için ek ayarlar
    options.set_argument('--disable-setuid-sandbox')
    options.set_argument('--disable-gpu')
    options.binary_location = '/snap/bin/chromium'
    
    # Use turnstilePatch from https://github.com/TheFalloutOf76/CDP-bug-MouseEvent-.screenX-.screenY-patcher
    options.add_extension("turnstilePatch")

    # If fail to pass the cloudflare in headless mode, try to align the user agent with your real browser
    if enable_headless:
        import platform
        system = platform.system().lower()
        
        # Set default platform identifier for Linux
        platformIdentifier = "X11; Linux x86_64"
        
        if system == "darwin":
            platformIdentifier = "Macintosh; Intel Mac OS X 10_15_7"
        elif system == "windows":
            platformIdentifier = "Windows NT 10.0; Win64; x64"
            
        # Align version with installed Chromium
        chrome_version = "133.0.6943.53"        
        options.set_user_agent(f"Mozilla/5.0 ({platformIdentifier}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36")
        options.headless()

    print(f"[Kayıt] {number} hesap {max_workers} iş parçacığında oluşturuluyor")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(register_cursor_core, copy.deepcopy(options)) for _ in range(number)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)

    results = [result for result in results if result["token"] is not None]

    if len(results) > 0:
        formatted_date = datetime.now().strftime("%Y-%m-%d")

        csv_file = f"./hesaplar_{formatted_date}.csv"
        token_file = f"./tokenler_{formatted_date}.csv"

        fieldnames = ["email", "password", "token"]
        # CSV dosyasına e-posta, şifre ve token bilgilerini yaz
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Dosya boşsa başlıkları ekle
                writer.writeheader()
            writer.writerows(results)
        # Sadece token'ları ayrı bir dosyaya yaz
        tokens = [{'token': row['token']} for row in results]
        with open(token_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['token'])
            writer.writerows(tokens)

    print(f"[Kayıt] {len(results)} hesap başarıyla oluşturuldu")
    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cursor Hesap Oluşturucu')
    parser.add_argument('--number', type=int, default=2, help="Kaç hesap oluşturulacak")
    parser.add_argument('--max_workers', type=int, default=1, help="Kaç iş parçacığı kullanılacak")
    
    # The parameters with name starts with oneapi are used to uploead the cookie token to one-api, new-api, chat-api server.
    parser.add_argument('--oneapi', action='store_true', help='One-API kullanılsın mı')
    parser.add_argument('--oneapi_url', type=str, required=False, help='One-API websitesi URL')
    parser.add_argument('--oneapi_token', type=str, required=False, help='One-API token')
    parser.add_argument('--oneapi_channel_url', type=str, required=False, help='One-API kanal URL')

    args = parser.parse_args()
    number = args.number
    max_workers = args.max_workers
    use_oneapi = args.oneapi
    oneapi_url = args.oneapi_url
    oneapi_token = args.oneapi_token
    oneapi_channel_url = args.oneapi_channel_url

    account_infos = register_cursor(number, max_workers)
    tokens = list(set([row['token'] for row in account_infos]))
    
    if use_oneapi and len(account_infos) > 0:
        from tokenManager.oneapi_manager import OneAPIManager
        from tokenManager.cursor import Cursor
        oneapi = OneAPIManager(oneapi_url, oneapi_token)

        # Send request by batch to avoid "Too many SQL variables" error in SQLite.
        batch_size = 10
        for idx, i in enumerate(range(0, len(tokens), batch_size), start=1):
            batch = tokens[i:i + batch_size]
            response = oneapi.add_channel("Cursor",
                                          oneapi_channel_url,
                                          '\n'.join(batch),
                                          Cursor.models,
                                          tags = "Cursor")
            print(f'[OneAPI] {idx}. Grup Eklendi. Durum Kodu: {response.status_code}, Yanıt: {response.json()}')
