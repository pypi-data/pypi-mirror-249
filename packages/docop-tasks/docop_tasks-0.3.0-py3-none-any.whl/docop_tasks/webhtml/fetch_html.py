"""fetch and store HTML from source URLs.
input: a source with some resources
output: documents with 'reference', 'title' and 'html' fields
"""

import asyncio
from playwright.async_api import async_playwright
from rich import print
from rich.progress import track
from yamlstore import Document


if not source:
   raise Exception("no source given")

if not source["resources"]:
   raise Exception("no resources given")


async def main():

    urls = source["resources"]

    async with async_playwright() as pw:

        browser = await pw.webkit.launch()
        page = await browser.new_page()
        titles = []
        
        for url in track(urls, description=f" ↳ fetching, rendering and extracting HTML from {len(urls)} urls", transient=True):
            await page.goto(url)
            title = await page.title()
            titles.append(title)
            #await page.screenshot(path=f'{title}.png')
            html = await page.content()
            doc = Document(title=title)
            doc["reference"] = url
            doc["title"] = title
            doc["html"] = html
            global collection
            collection += doc

        for title in titles:
            print(f" ↳ '{title}' ✅")

    await browser.close()

asyncio.run(main())
