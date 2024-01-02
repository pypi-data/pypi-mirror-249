from simplaza.api import manager

from rich.prompt import Prompt, Confirm
from rich.console import Console

from os.path import exists
from sys import exit

import click

@click.command()
@click.option("--magnet", is_flag=True, help="Opens magnet link")
@click.option("--json", is_flag=True, help="Returns search results")
@click.option("--default", is_flag=True, help="Gets first option automatically")
@click.argument('query', required=False)

def main(**kwargs):
    """
    SimPlaza CLI - Query and download files from SimPlaza directly from your terminal
    \n
    GitHub:\n
            https://github.com/Jayy001/SimPlaza\n
    Usage:
    \n
            simplaza <query> 
    """

    sp = manager()  # Initialize the SimPlaza class
    console = Console()

    queryPrompt = kwargs['query']
    
    if not kwargs['query']:
        queryPrompt = Prompt.ask("Enter your search query")
    
    elif exists(kwargs['query']): # File input
        with open(kwargs['query'], 'r') as file:
            while (line := file.readline().rstrip()):
                query_results = sp.search(line)

                RequestedAddonLink = False

                if kwargs['default']:
                    try:
                        RequestedAddonLink = query_results[0]['link']
                        console.print(query_results[0]['name'])
                    except:
                        console.print("No results for " + line, style="red")
                        continue
                else:
                    for option in query_results:
                        if Confirm.ask(f"Select {option['name']}"):
                            RequestedAddonLink = option['link']
                            break

                if RequestedAddonLink:
                    torrent_data = sp.get_torrent_data(RequestedAddonLink)

                    if not torrent_data:
                        console.print("Could not get torrent for " + line, style="red")
                        continue 

                    if kwargs['magnet']:
                        sp.open_torrent(torrent_data) # Single function?
                    else:
                        with open(f"{line}.torrent", "wb") as torrent_file:
                            torrent_file.write(torrent_data)
        return

    query_results = sp.search(queryPrompt)  # Search SimPlaza for your input

    if kwargs['json']:
        console.print(query_results)

        return

    sp.output_table(query_results)  # Output the results as a table

    if not query_results:
        return

    RequestedAddonLink = query_results[0]['link']

    if not kwargs['default']:
        AddonQueryID = Prompt.ask(
            "What addon would you like to download?",
            choices=[addon["id"] for addon in query_results],
        )
        RequestedAddonLink = sp.match_id_to_link(
            query_results, AddonQueryID
        )  # Get the addons link

    torrent_data = sp.get_torrent_data(RequestedAddonLink)

    if not torrent_data:
        console.print("Could not get torrent for " + queryPrompt, style="red")

        return 
        
    if kwargs['magnet']:
        sp.open_torrent(torrent_data) # Open torrent in client of your choice
    else:
        with open(f"{queryPrompt}.torrent", "wb") as torrent_file:
            torrent_file.write(torrent_data)

    exit(0)

if __name__ == "__main__":
    main()  # pragma: no covers