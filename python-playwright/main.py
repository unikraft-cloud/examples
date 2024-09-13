from fastapi import FastAPI, Response
from playwright.async_api import async_playwright

app = FastAPI()


@app.get("/")
async def screenshot_page(page: str | None = None):
    if not page:
        return {"message": "Nothing to do"}

    try:
        url = f"{page}"
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        buffer = await page.screenshot()
        await browser.close()
        await playwright.stop()

        return Response(content=buffer, media_type="image/png")
    except Exception as err:
        return {"message": "An error occured: " + str(err)}
