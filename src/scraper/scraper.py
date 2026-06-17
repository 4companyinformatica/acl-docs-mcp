from bs4 import BeautifulSoup
import httpx
from typing import Literal, List, Dict, Annotated
from util.cacher import Cacher
from settings import settings

cache = Cacher(ttl=settings.cache_ttl)

class Scraper:
    def __init__(self, 
                analytics_version: Annotated[str, "The version of the analytics platform to scrape"] = settings.acl_version
                ) -> None:

        self.analytics_version = analytics_version
        self.C_F_BASE_URL = f"https://help.diligentoneplatform.com/helpdocs/analytics-{analytics_version}/en-us/Content/analytics/scripting"
        self.H_BASE_URL = f"https://help.diligentoneplatform.com/helpdocs/analytics-{analytics_version}/en-us/Content/analytics/scripting/analytic_development/analytic_tags"

    async def command_list(self, command_type: Annotated[Literal["commands", "functions"], "The type of commands to list"]) -> List[Dict[str, str]]:

        if command_type == "commands":
            url = f"{self.C_F_BASE_URL}/commands/commands.htm"
        elif command_type == "functions":
            url = f"{self.C_F_BASE_URL}/functions/functions.htm"
        else:
            raise ValueError("Invalid list selector. Use 'commands' or 'functions'.")
        
        cached = cache.get(url=url)
        if cached:
            return cached
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        bs = BeautifulSoup(response.content, "html.parser")
        tables = bs.find("table").find("tbody").find_all("tr")
        result = {"data": []}

        for table in tables:
            
            href = table.findAll("td")[0].find("a")["href"]
            command = (
                table
                .findAll("td")[0]
                .find("a")
                .text
                .strip()
                .replace("\xa0", "")
            )
            
            description = (
                table
                .findAll("td")[1]
                .find("p")
                .text
                .strip()
                .replace("\r\n", " ")
            )
            result["data"].append({"command": command, "description": description, "href": href})
        
        cache.set(data=result, url=url)
        return result

    async def command_details(
            self, 
            command_type: Annotated[Literal["commands", "functions"], "The type of command for which to fetch details"], 
            href: Annotated[str, "The href of the command for which to fetch details"]
        ) -> Dict[str, str]:

        if command_type == "commands":
            url = f"{self.C_F_BASE_URL}/commands/{href}"
        elif command_type == "functions":
            url = f"{self.C_F_BASE_URL}/functions/{href}"
        else:
            raise ValueError("The user has to specify if it's a command or a function. Tip: if it has a parenthesis at the end, it's probably a function.")
        
        cached = cache.get(url=url)
        if cached:
            return cached
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        bs = BeautifulSoup(response.content, "html.parser")

        result = {
            "data": {
                "href": href,
                "details_html": bs.find("div", {"role": "main"}).decode_contents()
            }
        }

        cache.set(data=result, url=url)
        return result

    async def tag_list(self) -> Dict:

        url = f"{self.H_BASE_URL}/analytic_header_syntax.htm"

        cached = cache.get(url=url)
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        bs = BeautifulSoup(response.content, "html.parser")
        table = bs.find_all("table")[1]  # Table 0 = Tag conventions; Table 1 = Tag list
        result = {"data": []}
        current_tag_type = "ANALYTIC"  # First tag (ANALYTIC) has no preceding <th>

        for row in table.find("tbody").find_all("tr"):
            # <th colspan="2"> inside tbody = tag type section header
            th = row.find("th")
            if th:
                current_tag_type = th.get_text(strip=True)
                continue

            tds = row.find_all("td")
            if len(tds) < 2:
                continue

            anchor = tds[0].find("a")
            if not anchor:
                continue

            href = anchor.get("href", "")
            tag_name = anchor.get_text(strip=True).replace(" tag", "").strip()
            description = tds[1].get_text(separator=" ", strip=True).replace("\r\n", " ")

            result["data"].append({
                "tag_type": current_tag_type,
                "tag_name": tag_name,
                "description": description,
                "href": href
            })

        cache.set(data=result, url=url)
        return result

    async def tag_details(
            self,
            href: Annotated[str, "The href of the analytic header tag to fetch details for"]
        ) -> Dict:

        url = f"{self.H_BASE_URL}/{href}"

        cached = cache.get(url=url)
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        bs = BeautifulSoup(response.content, "html.parser")

        result = {
            "data": {
                "href": href,
                "details_html": bs.find("div", {"role": "main"}).decode_contents()
            }
        }

        cache.set(data=result, url=url)
        return result


if __name__ == "__main__":
    import asyncio
    # def test_scraper_tag_func_1():
    #     sc = Scraper()
        
    #     test = asyncio.run(sc.tag_list())
    #     assert isinstance(test['data'], list)

    # def test_scraper_tag_func_2():
    #     sc = Scraper()
        
    #     test = asyncio.run(sc.tag_list())
    #     assert bool(test['data'])

    # test_scraper_tag_func_1()
    # test_scraper_tag_func_2()
    sc = Scraper()
    
    test = asyncio.run(sc.tag_list())
    print(test)