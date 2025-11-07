"""
Pokedex Citron DB - A lightweight Pokémon database library using CSV
"""

import csv
import os
from typing import Optional, List, Dict

# Global variable to store the loaded Pokémon data
_pokemon_data = []
_pokemon_by_name = {}

def _load_csv():
    """Load the CSV file into memory when the module is imported."""
    global _pokemon_data, _pokemon_by_name
    
    # Get the directory where this module is located
    module_dir = os.path.dirname(__file__)
    csv_path = os.path.join(module_dir, "pokedex_db.csv")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            _pokemon_data = list(reader)
            
            # Create a lookup dictionary for faster name-based searches
            _pokemon_by_name = {row['name'].lower(): row for row in _pokemon_data}
            
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Please ensure 'pokedex_db.csv' exists in the module directory.")
    except Exception as e:
        raise RuntimeError(f"Error loading CSV file: {str(e)}")


def search_by_name(name: str) -> Optional[Dict]:
    """
    Search for a Pokémon by name and return its metadata.
    Only returns fields that have truthy values (omits false/0 values).
    
    Args:
        name: The Pokémon name to search for
        
    Returns:
        A dictionary with the Pokémon's metadata, or None if not found
    """
    pokemon = _pokemon_by_name.get(name.lower())
    
    if not pokemon:
        return None
    
    # Build result dictionary, excluding false values
    result = {}
    
    # Always include these fields
    for field in ['number', 'name', 'primary_type', 'generation']:
        if field in pokemon and pokemon[field]:
            result[field] = pokemon[field]
    
    # Include secondary_type if it's not empty
    if pokemon.get('secondary_type'):
        result['secondary_type'] = pokemon['secondary_type']
    
    # Include boolean fields only if they are true (1)
    boolean_fields = ['mega_evolution', 'legendary', 'final_stage']
    for field in boolean_fields:
        if pokemon.get(field) == '1':
            result[field] = True
    
    # Include regional_form if it's not empty
    if pokemon.get('regional_form'):
        result['regional_form'] = pokemon['regional_form']
    
    return result


def ispokemon(name: str) -> bool:
    """
    Check if the given name is a valid Pokémon in the database.
    
    Args:
        name: The name to check
        
    Returns:
        True if the name is a valid Pokémon, False otherwise
    """
    return name.lower() in _pokemon_by_name


def get_by_primary_type(primary_type: str) -> List[str]:
    """
    Get all Pokémon with the specified primary type.
    
    Args:
        primary_type: The primary type to search for
        
    Returns:
        A list of Pokémon names with that primary type
    """
    return [
        pokemon['name'] 
        for pokemon in _pokemon_data 
        if pokemon.get('primary_type', '').lower() == primary_type.lower()
    ]


def get_by_secondary_type(secondary_type: str) -> List[str]:
    """
    Get all Pokémon with the specified secondary type.
    
    Args:
        secondary_type: The secondary type to search for
        
    Returns:
        A list of Pokémon names with that secondary type
    """
    return [
        pokemon['name'] 
        for pokemon in _pokemon_data 
        if pokemon.get('secondary_type', '').lower() == secondary_type.lower()
    ]


def get_all_megas() -> List[str]:
    """
    Get all Pokémon that have a mega evolution.
    
    Returns:
        A list of Pokémon names that can mega evolve
    """
    return [
        pokemon['name'] 
        for pokemon in _pokemon_data 
        if pokemon.get('mega_evolution') == '1'
    ]


def get_all_regional_forms() -> List[str]:
    """
    Get all Pokémon that have regional forms.
    
    Returns:
        A list of Pokémon names with regional forms
    """
    # Only count Pokémon where regional_form is not '0', '', or None
    return [
        pokemon['name']
        for pokemon in _pokemon_data
        if 'regional_form' in pokemon and pokemon['regional_form'] not in ('', '0', None)
    ]


def get_all_legendaries() -> List[str]:
    """
    Get all legendary Pokémon.
    
    Returns:
        A list of legendary Pokémon names
    """
    # Count as legendary if either 'legendary' or 'overall_legendary' is '1'
    return [
        pokemon['name']
        for pokemon in _pokemon_data
        if (
            ('legendary' in pokemon and pokemon['legendary'] == '1') 
        )
    ]


# Load the CSV when the module is imported
_load_csv()


# Export public API
__all__ = [
    'search_by_name',
    'ispokemon',
    'get_by_primary_type',
    'get_by_secondary_type',
    'get_all_megas',
    'get_all_regional_forms',
    'get_all_legendaries'
]
