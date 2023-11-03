import os, requests, re
from rich import print
from rich.console import Console
from rich.table import Table

if os.path.exists("env.py"):
    import env

API_KEY = os.environ.get("API_KEY")
console = Console()
endpoint = "http://www.omdbapi.com/?apikey=" + API_KEY + "&"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    console.rule("Welcome to the IMDB Movie Lookup Tool!")
    print("1. Get Data By Movie Name")
    print("2. Get Data By IMBD ID")
    print("3. Search for movie by name")
    print("4. Exit")

def option_one():
    clear_screen()
    console.rule("IMDB Movie Lookup Tool - Lookup By Name")
    query = input("Please enter the name of the movie you wish to lookup: ")
    response = requests.get(endpoint + "t=" + query)
    data = response.json()
    if data.get('Response') == 'True':
        display_data_table(data)
    else:
        input("Movie not found! Press Enter to return to the menu...")

def option_two():
    clear_screen()
    console.rule("IMDB Movie Lookup Tool - Lookup By ID")
    while True:
            query = input("Please enter the ID of the movie you wish to lookup (Format: tt#######): ")
            if re.match(r'^tt\d{7,9}$', query):
                response = requests.get(endpoint + "i=" + query)
                data = response.json()
                if data.get('Response') == 'True':
                    display_data_table(data)
                    break
                else:
                    input("Movie not found! Press Enter to return to the menu...")
            else:
                input("Invalid format! Please enter a valid ID in the format 'tt########'. Press Enter to try again...")

def option_three():
    clear_screen()
    console.rule("IMDB Movie Lookup Tool - Search By Name")
    query = input("Please enter the name of the movie you wish to search for: ")
    response = requests.get(endpoint + "s=" + query)
    data = response.json()
    if data.get('Response') == 'True':
        display_search_table(data, query)
    else:
        input("Movie not found! Press Enter to return to the menu...")

def display_data_table(response):
    table_1 = Table(title=response.get('Title'), min_width=200)
    table_1.add_column("Year", justify="center", style="cyan", no_wrap=True)
    table_1.add_column("Rating", justify="center", style="magenta")
    table_1.add_column("Runtime", justify="center", style="green")
    table_1.add_column("Genre", justify="center", style="green")
    table_1.add_column("Released", justify="center", style="green")
    table_1.add_row(
        response.get('Year'),
        response.get('Rated'),
        response.get('Runtime'),
        response.get('Genre'),
        response.get('Released'))
    table_2 = Table(min_width=200)
    table_2.add_column("Actors", justify="center", style="cyan")
    table_2.add_column("Director", justify="center", style="magenta")
    table_2.add_column("Box Office", justify="center", style="green")
    table_2.add_row(
        response.get('Actors'),
        response.get('Director'),
        response.get('BoxOffice'))
    table_3 = Table(min_width=200)
    table_3.add_column("Plot", justify="center", style="cyan")
    table_3.add_row(
        response.get('Plot'))
    console.print(table_1)
    console.print(table_2)
    console.print(table_3)
    input("Press Enter to return to the menu...")


def display_search_table(response, query):
    clear_screen()
    search_results = response.get('Search')
    table = Table(title="Search Results for " + query)
    table.add_column("Title", justify="center", style="cyan", no_wrap=True)
    table.add_column("Year", justify="center", style="magenta", no_wrap=True)
    table.add_column("Type", justify="left", style="magenta", no_wrap=True)
    table.add_column("IMDb ID", justify="center", style="green", no_wrap=True)

    for result in search_results:
        title = result.get('Title')
        year = result.get('Year')
        type = result.get('Type').strip().capitalize()
        imdb_id = result.get('imdbID')
        table.add_row(title, year, type, imdb_id)

    console.print(table)
    input("Press Enter to return to the menu...")


while True:
    clear_screen()
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        option_one()
    elif choice == "2":
        option_two()
    elif choice == "3":
        option_three()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        input("Invalid choice! Press Enter to continue...")
