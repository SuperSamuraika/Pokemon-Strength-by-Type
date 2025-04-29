import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://bulbapedia.bulbagarden.net"
LIST_URL = BASE_URL + "/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
HEADERS = {"User-Agent": "Mozilla/5.0"}

type_strength_values = {
    'Normal':   16.0,
    'Fire':     20.0,
    'Water':    19.5,
    'Electric': 17.5,
    'Grass':    17.5,
    'Ice':      20.0,
    'Fighting': 19.5,
    'Poison':   17.0,
    'Ground':   21.0,
    'Flying':   19.5,
    'Psychic':  18.0,
    'Bug':      17.5,
    'Rock':     20.5,
    'Ghost':    18.5,
    'Dragon':   17.5,
    'Dark':     18.5,
    'Steel':    19.0,
    'Fairy':    19.5,
}

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

def save_pokemons_csv(pokemons, filename="pokemons.csv"):
    df = pd.DataFrame(pokemons)

    pokemon_types = set(type_strength_values.keys())
    df = df[df["Number"].str.isdigit()]
    df = df[~df["Name"].isin(pokemon_types)]

    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Total Pokemons saved: {len(df)}")
    return filename

def calc_strength(row):
    strength = 0.0
    if pd.notna(row['Type1']):
        strength += type_strength_values.get(row['Type1'], 0)
    if pd.notna(row['Type2']):
        strength += type_strength_values.get(row['Type2'], 0)
    return strength

def rank_pokemons_by_strength(input_csv="pokemons.csv", output_csv="pokemon_strength_ranking.csv"):
    df = pd.read_csv(input_csv, dtype=str)
    df['Strength by Type'] = df.apply(calc_strength, axis=1)
    df = df.sort_values('Strength by Type', ascending=False).reset_index(drop=True)
    df.to_csv(output_csv, index=False)
    print(f"Strength ranking saved to: {output_csv}")
    print(df[['Name', 'Type1', 'Type2', 'Strength by Type']].head(10))

def main():
    pokemons = fetch_pokemon_list()
    if not pokemons:
        print("Failed to fetch any pokemons.")
        return
    csv_file = save_pokemons_csv(pokemons)
    rank_pokemons_by_strength(csv_file)

if __name__ == "__main__":
    main()
