import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://bulbapedia.bulbagarden.net"
LIST_URL = BASE_URL + "/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_pokemon_list():
    resp = requests.get(LIST_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "lxml")

    pokemons = []
    
    tables = soup.select("table.roundy")

    for table in tables:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            
            number = cols[0].get_text(strip=True).lstrip("#")

            
            a_name = cols[2].find("a")
            if not a_name or not a_name.get("href"):
                continue
            name = a_name.get_text(strip=True)
            link = BASE_URL + a_name["href"]

            
            types = []
            for cell in cols[3:]:
                a_type = cell.find("a")
                if a_type:
                    types.append(a_type.get_text(strip=True))
                    
                    if cell.get("colspan") == "2":
                        break
                if len(types) == 2:
                    break

            type1 = types[0] if len(types) > 0 else None
            type2 = types[1] if len(types) > 1 else None

            pokemons.append({
                "Number": number,
                "Name": name,
                "Link": link,
                "Type1": type1,
                "Type2": type2
            })

    return pokemons

def main():
    data = fetch_pokemon_list()
    if not data:
        print("Could not retrieve any data.")
        return

    df = pd.DataFrame(data)

    
    pokemon_types = {
        "Normal","Fire","Water","Electric","Grass","Ice","Fighting",
        "Poison","Ground","Flying","Psychic","Bug","Rock","Ghost",
        "Dragon","Dark","Steel","Fairy"
    }
    df = df[df["Number"].str.isdigit()]
    df = df[~df["Name"].isin(pokemon_types)]

    print(f"Total amount of Pokemons added: {len(df)}")
    df.to_csv("pokemons.csv", index=False, encoding="utf-8-sig")
    print("Saved pokemons.csv")

if __name__ == "__main__":
    main()
