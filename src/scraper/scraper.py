from bs4 import BeautifulSoup
import httpx
from typing import Literal, List, Dict, Annotated
from util.cacher import Cacher

cache = Cacher(ttl=24*60*60)

class Scraper:
    def __init__(self, 
                analytics_version: Annotated[str, "The version of the analytics platform to scrape"] = "19"
                ) -> None:

        self.analytics_version = analytics_version
        self.URL_BASE = f"https://help.diligentoneplatform.com/helpdocs/analytics-{analytics_version}/en-us/Content/analytics/scripting"

    async def command_list(self, command_type: Annotated[Literal["commands", "functions"], "The type of commands to list"]) -> List[Dict[str, str]]:

        if command_type == "commands":
            url = f"{self.URL_BASE}/commands/commands.htm"
        elif command_type == "functions":
            url = f"{self.URL_BASE}/functions/functions.htm"
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
            url = f"{self.URL_BASE}/commands/{href}"
        elif command_type == "functions":
            url = f"{self.URL_BASE}/functions/{href}"
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
                "details_html": bs.find("div", {"role": "main"})
            }
        }

        cache.set(data=result, url=url)
        return result

if __name__ == "__main__":
    ...