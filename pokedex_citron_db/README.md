# Pokedex Citron DB

A lightweight Python library for querying Pokémon data from a CSV database.

## Installation

Place the `pokedex_citron_db` folder in your project directory or Python path.

## Usage

```python
from pokedex_citron_db import (
    search_by_name,
    ispokemon,
    get_by_primary_type,
    get_by_secondary_type,
    get_all_megas,
    get_all_regional_forms,
    get_all_legendaries
)

# Search for a Pokémon by name
pikachu = search_by_name("Pikachu")
print(pikachu)  # {'number': '25', 'name': 'Pikachu', 'primary_type': 'Electric', 'generation': '1'}

# Check if a name is a valid Pokémon
print(ispokemon("Charizard"))  # True
print(ispokemon("Fakemon"))    # False

# Get Pokémon by type
fire_types = get_by_primary_type("Fire")
flying_types = get_by_secondary_type("Flying")

# Get special categories
megas = get_all_megas()
legendaries = get_all_legendaries()
regional_forms = get_all_regional_forms()
```

## API Reference

### `search_by_name(name: str) -> dict | None`
Returns a dictionary with Pokémon metadata. Only includes truthy values (false/0 values are omitted).

### `ispokemon(name: str) -> bool`
Returns True if the name is a valid Pokémon in the database.

### `get_by_primary_type(primary_type: str) -> list`
Returns a list of Pokémon names with the specified primary type.

### `get_by_secondary_type(secondary_type: str) -> list`
Returns a list of Pokémon names with the specified secondary type.

### `get_all_megas() -> list`
Returns a list of all Pokémon that have a mega evolution.

### `get_all_regional_forms() -> list`
Returns a list of all Pokémon that have regional forms.

### `get_all_legendaries() -> list`
Returns a list of all legendary Pokémon.

## Database Structure

The CSV file (`pokedex_db.csv`) contains the following columns:
- `number`: Pokédex number
- `name`: Pokémon name
- `primary_type`: Primary type
- `secondary_type`: Secondary type (if any)
- `generation`: Generation number
- `mega_evolution`: 1 if has mega evolution, 0 otherwise
- `legendary`: 1 if legendary, 0 otherwise
- `final_stage`: 1 if final evolution stage, 0 otherwise
- `regional_form`: Regional form name (if any)

## Testing

Run the test script to verify all functions:

```bash
python test_pokedex.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This Pokédex list may not be up to date with Pokémon Legends ZA or later games. 