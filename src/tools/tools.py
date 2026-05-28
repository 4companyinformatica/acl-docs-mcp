from typing import Annotated, Literal, Dict, Optional
from src.scraper.scraper import Scraper


scraper = Scraper(analytics_version="19")

async def command_list_tool(
    command_type: Annotated[Literal["commands", "functions"], "Defines wheter to fetch the list of commands or functions"],
    filter_command: Optional[Annotated[str, "A string to filter the commands or functions by name (optional)"]] = None,
    filter_description: Optional[Annotated[str, "A string to filter the commands or functions by description (optional)"]] = None
) -> Dict[str, str]:
    
    command_list = await scraper.command_list(command_type=command_type)
    if filter_command:
        command_list["data"] = [
            command for command 
            in command_list["data"] 
            if filter_command.lower() in command["command"].lower()
        ]
    if filter_description:
        command_list["data"] = [
            command for command 
            in command_list["data"] 
            if filter_description.lower() in command["description"].lower()
        ]
    return command_list

async def command_details_tool(
    command_href: Annotated[str, "The href of the command or function to fetch details for"],
    command_type: Annotated[Literal["commands", "functions"], "Defines whether the command is a command or a function"]
) -> Dict[str, str]:
    
    return await scraper.command_details(command_type=command_type, href=command_href)