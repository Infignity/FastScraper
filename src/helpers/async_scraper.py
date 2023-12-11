'''scrapper '''
import ssl
from typing import Dict
import asyncio
import re
import httpx
import anyio
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
from beanie import PydanticObjectId
from src.core.database import init_db
from src.core.models import Task, TaskResult
from src.core.config import get_random_ua
from src.core.exceptions import MaxretriesError, InvalidUrlError
from src.helpers.scrapper import ScrapperHelper

MAX_RETRIES = 3


async def send_until_ok(
        session: httpx.AsyncClient,
        url,
        random_ua=get_random_ua(),
        retries=0) -> HTMLParser:
    '''scrappers'''
    if not isinstance(url, str):
        print(f"URL TYPE {type(str)}")
        raise InvalidUrlError("Invalid Url")
    
    try:
        resp = await session.get(
            url,
            headers={"user-agent": random_ua},
            follow_redirects=True
        )
        if resp.status_code in [200, 301, 302]:
            return HTMLParser(resp.content)
    except (TypeError, ssl.SSLCertVerificationError) as e:
        raise InvalidUrlError(f"Invalid Url")
    except (
        httpx.ReadTimeout,
        httpx.ReadError,
        UnicodeEncodeError,
        httpx.ConnectError,
        httpx.ConnectTimeout,
        httpx.RemoteProtocolError,
        httpx.PoolTimeout,
        TimeoutError,
        anyio.EndOfStream
    ) as e:
        pass
    
    if retries > MAX_RETRIES:
        raise MaxretriesError("Max retries reached")
    
    print(f"Retrying -> {url}")
    return await send_until_ok(session, url, retries=retries+1)


async def play_wright(url):
    """using playwright for data scrapping"""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        await page.wait_for_selector('p')
        data = await page.content()
        bss4 = ScrapperHelper()
        scrapped_data = bss4.bs4(data)
        # clear empty white space
        cleaned_text = re.sub('\n\s*\n', '\n\n', scrapped_data)
        cleaned_text = re.sub(' +', ' ', cleaned_text)
        print(f"data === {cleaned_text}")
        await browser.close()
        return cleaned_text


def format_url(url):
    '''format urls'''
    f_url = url
    if not url.startswith("https") and not url.startswith("http"):
        f_url = f"https://{url}"
    return f_url


async def scrape_url(
        session: httpx.AsyncClient,
        datalist: Dict, task_id: PydanticObjectId
):
    '''scrap urls'''
    if isinstance(datalist['Website'], str):
        url = format_url(datalist['Website'])
        try:
            # parser = await send_until_ok(session, url)
            parser = await play_wright(url)
            # print(parser)
            # p_tags = parser.css('p')
            # texts = [p.text(strip=True) for p in p_tags]
            # texts = [p.text(strip=True) for p in parser]
            # print(f'scrapped data: {texts}')
            # landing_page_text = (".".join(parser)).replace("..", ".")
            print(f'the url is {url}')
            new_task_result = TaskResult(
                landing_page_text=parser,
                task_id=task_id,
                website=url,
                linkedin_url=datalist.get('Linkedin', ''),
                first_name=datalist.get('first_name', ''),
                last_name=datalist.get('last_name', ''),
                seniority=datalist.get('Seniority', ''),
                organization_name=datalist.get('organization_name', ''),
                industry=datalist.get('Industry', ''),
                department=datalist.get('Departments', ''),
                email=str(datalist.get('email', '')),
                phone=str(datalist.get('Phone', '')),
                headline=datalist.get('Headline', ''),
                domain=datalist.get('domain', ''),
                keywords=str(datalist.get('Keywords', '')),
                company_address=datalist.get('Company Address', ''),
                num_employee=str(datalist.get('Number of Employees', '')),
                city=datalist.get('City', ''),
                state=datalist.get('State', ''),
                country=datalist.get('Country', ''),
                person_linkedin=datalist.get('Person Linkedin Url', ''),
                company_linkedin=datalist.get('Company Linked In', ''),
                apolo_email=datalist.get('Apollo email', ''),
                company_name=datalist.get('Company', ''),
                entity_id=datalist.get('Entity_id', ''),
            )
            await new_task_result.create()
            
        except Exception as e:
            print(e)
        

async def update_task_state(task_id, state):
    '''update task'''
    task = await Task.get(task_id)
    if task:
        task.state = state
        await task.save_changes()


async def run(task_id_str, datalist, start_n: int = 0):
    '''run scrapper'''
    total_urls = len(datalist)
    task_id = PydanticObjectId(task_id_str)
    await init_db([Task, TaskResult])
    await update_task_state(task_id, "running")
    
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as session:
        for i in range(total_urls):
            url = datalist[i]['Website']
            print(f"Scraping url [{task_id_str}] -> {url} -> {i}")
            await scrape_url(session, datalist[i], task_id)
            
    task = await Task.get(task_id)
    task_results = await TaskResult.find(
        TaskResult.task_id == task_id).to_list()
    task.results = task_results
    task.state = "completed"
    await task.save_changes()
