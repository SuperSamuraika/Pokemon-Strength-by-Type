import pandas as pd


INPUT_CSV   = "pokemons.csv"   # Входной CSV файл с данными покемонов
OUTPUT_CSV  = "pokemon_strength_ranking.csv"  # Выходной CSV файл с результатами


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

def calc_strength(row):
    strength = 0.0
    if pd.notna(row['Type1']):
        strength += type_strength_values.get(row['Type1'], 0)
    if pd.notna(row['Type2']):
        strength += type_strength_values.get(row['Type2'], 0)
    return strength


def main():
    df = pd.read_csv(INPUT_CSV, dtype=str)
    df['Strength by Type'] = df.apply(calc_strength, axis=1)
    df = df.sort_values('Strength by Type', ascending=False).reset_index(drop=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print("Done.", OUTPUT_CSV)
    print(df[['Name', 'Type1', 'Type2', 'Strength by Type']].head(10))


if __name__ == "__main__":
    main()
