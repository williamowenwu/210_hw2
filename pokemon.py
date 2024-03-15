import csv
from collections import defaultdict
def get_num_of_pokemon_levels(reader, poke_type: str, level: int):
    with open('pokemon1.txt', 'w') as p:
        pokemon_types = [pokemon for pokemon in reader if pokemon['type'] == poke_type]
        valid_pokemons = [pokemon for pokemon in pokemon_types if float(pokemon['level']) > level]
        
        print(len(pokemon_types))
        print(len(valid_pokemons))
        p.write(f"Percentage of fire type Pokemons at or above level 40 = {round((len(valid_pokemons)/len(pokemon_types))*100)}")
        # print(f'after: {list(reader)}')


def fill_in_missing_values(pokemon_dict, level_cap: int = 40):
    weaknesses = defaultdict(lambda: defaultdict(int))
    stats = ['atk', 'def', 'hp']
    # Initialize dictionaries for sums and counts
    above_cap_sums = defaultdict(float, {stat: 0 for stat in stats})
    above_cap_counts = defaultdict(int, {stat: 0 for stat in stats})
    below_cap_sums = defaultdict(float, {stat: 0 for stat in stats})
    below_cap_counts = defaultdict(int, {stat: 0 for stat in stats})

    # First pass: Fill weaknesses and sum stats for calculating averages
    for pokemon in pokemon_dict:
        if pokemon['type'] != 'NaN':
            weaknesses[pokemon['weakness']][pokemon['type']] += 1

        level = float(pokemon['level'])
        cap_dict_sums = above_cap_sums if level > level_cap else below_cap_sums
        cap_dict_counts = above_cap_counts if level > level_cap else below_cap_counts

        for stat in stats:
            if pokemon[stat] != 'NaN':
                value = float(pokemon[stat])
                cap_dict_sums[stat] += value
                cap_dict_counts[stat] += 1

    # Determine the most common type for each weakness
    most_common_type = {
        weakness: max(types, key=lambda x: (types[x], x))
        for weakness, types in weaknesses.items()
    }

    # Second pass: Fill missing values with averages
    for pokemon in pokemon_dict:
        if pokemon['type'] == 'NaN':
            pokemon['type'] = most_common_type.get(pokemon['weakness'], 'Unknown')

        level = float(pokemon['level'])
        cap_dict_sums = above_cap_sums if level > level_cap else below_cap_sums
        cap_dict_counts = above_cap_counts if level > level_cap else below_cap_counts

        for stat in stats:
            if pokemon[stat] == 'NaN' and cap_dict_counts[stat] > 0:
                avg = cap_dict_sums[stat] / cap_dict_counts[stat]
                pokemon[stat] = round(avg, 1)

    
    with open("pokemonResult.csv", 'w') as f:
        fieldnames = pokemon_dict[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for pokemon in pokemon_dict:
            writer.writerow(pokemon)

# stupid thing has to be sorted
def assign_personality(filled_dict):
    types_dict = defaultdict(list)
    
    for pokemon in filled_dict:
        if pokemon['personality'] not in types_dict[pokemon['type']]:
            types_dict[pokemon['type']].append(pokemon['personality'])
    
    sorted_type_names = {k: types_dict[k] for k in sorted(types_dict)}
    
    for k in sorted_type_names:
        sorted_type_names[k].sort()
    print(sorted_type_names)

    with open('pokemon4.txt', 'w') as f:
        for type_, personalities in sorted_type_names.items():
            f.write(f"{type_}: {', '.join(personalities)}\n")


def find_avg_hp(filled_dict, stage: float = 3.0):
    sum_ = 0
    amt = 0
    for pokemon in filled_dict:
        if float(pokemon['stage']) == stage:
            sum_ += float(pokemon['hp'])
            amt += 1
    
    with open('pokemon5.txt', 'w') as f:
        f.write(f"Average hit point for Pokemons of stage 3.0 = {round((sum_/amt), 1)}")

if __name__ == "__main__":
    with open('pokemonTrain.csv', 'r') as f:
        reader = csv.DictReader(f)
        pokemon_dict = list(reader)
        # 1. 
        get_num_of_pokemon_levels(pokemon_dict, 'fire', 40)
        # 2. Fills in the missing values
        fill_in_missing_values(pokemon_dict)
        
        with open('pokemonResult.csv', 'r') as result:
            result_reader = csv.DictReader(result)
            filled_dict = list(result_reader)
            
            # 3. Assigns personality to pokemon types
            assign_personality(filled_dict)
            
            # 4. avg hp
            find_avg_hp(filled_dict)
        