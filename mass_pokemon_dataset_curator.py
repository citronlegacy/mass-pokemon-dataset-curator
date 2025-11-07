#!/usr/bin/env python3
"""
Pokemon Dataset Curator CLI
Processes Pokemon dataset folders and curates their tag files for LoRA training.
"""

import os
import json
import re
from pathlib import Path
from typing import Set, List, Tuple, Optional
from tqdm import tqdm
from pokedex_citron_db import ispokemon


def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {config_path} not found. Using empty config.")
        return {"tags_to_absorb": []}
    except json.JSONDecodeError as e:
        print(f"Error parsing {config_path}: {e}")
        return {"tags_to_absorb": []}


def extract_pokemon_name(folder_name: str) -> Optional[str]:
    """
    Extract Pokemon name from folder name and determine if it's a valid format.
    Returns the Pokemon name in lowercase if recognized, None otherwise.
    
    Recognized formats:
    - pokemon_namePokedex_IXL
    - pokemon_name_(pokemon)
    - pokemon_name_pokemon
    - pokemon_name (no special characters except _ and -)
    """
    # Format 1: pokemon_namePokedex_IXL
    match = re.match(r'^([a-zA-Z0-9_-]+)Pokedex_IXL$', folder_name, re.IGNORECASE)
    if match:
        return match.group(1).lower()

    # Format 2: pokemon_name_(pokemon)
    match = re.match(r'^([a-zA-Z0-9_-]+)_\(pokemon\)$', folder_name, re.IGNORECASE)
    if match:
        return match.group(1).lower()

    # Format 3: pokemon_name_pokemon (acceptable alternate)
    match = re.match(r'^([a-zA-Z0-9_-]+)_pokemon$', folder_name, re.IGNORECASE)
    if match:
        return match.group(1).lower()

    # Format 4: pokemon_name (only letters, numbers, underscores, and hyphens)
    match = re.match(r'^([a-zA-Z0-9_-]+)$', folder_name)
    if match:
        # Check if it contains Pokedex or (pokemon) - if so, it's not this format
        if 'pokedex' not in folder_name.lower() and '(pokemon)' not in folder_name.lower():
            return match.group(1).lower()

    return None


def get_standard_folder_name(pokemon_name: str) -> str:
    """
    Convert Pokemon name to standard folder format.
    Returns: PokemonNamePokedex_IXL
    """
    # Capitalize first letter of each word separated by _ or -
    parts = re.split(r'[_-]', pokemon_name)
    capitalized = ''.join(part.capitalize() for part in parts)
    return f"{capitalized}Pokedex_IXL"


def should_rename_folder(folder_name: str, pokemon_name: str) -> bool:
    """Check if folder needs to be renamed to standard format."""
    standard_name = get_standard_folder_name(pokemon_name)
    return folder_name != standard_name


def process_tags(
    tags_str: str,
    pokemon_name: str,
    tags_to_absorb: Set[str]
) -> str:
    """
    Process tags according to the rules:
    1. Remove pokemon_name_(pokemon) format tags
    2. Remove tags in tags_to_absorb
    3. Add trigger tag at the beginning
    4. Clean and deduplicate tags
    """
    # Split and clean tags
    tags = [tag.strip().lower() for tag in tags_str.split(',')]
    
    # Remove empty tags
    tags = [tag for tag in tags if tag]
    
    # Remove pokemon_name_(pokemon) format
    pokemon_tag = f"{pokemon_name}_(pokemon)"
    tags = [tag for tag in tags if tag != pokemon_tag]
    
    # Remove tags to absorb
    tags = [tag for tag in tags if tag not in tags_to_absorb]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
    
    # Create trigger tag
    parts = re.split(r'[_-]', pokemon_name)
    capitalized = ''.join(part.capitalize() for part in parts)
    trigger_tag = f"zz{capitalized}C1tr0n"

    # Check if trigger already present (case-insensitive)
    trigger_tag_lower = trigger_tag.lower()
    if any(tag == trigger_tag_lower for tag in unique_tags):
        final_tags = unique_tags
    else:
        final_tags = [trigger_tag] + unique_tags

    return ', '.join(final_tags)


def process_txt_files(folder_path: Path, pokemon_name: str, tags_to_absorb: Set[str]) -> int:
    """
    Process all .txt files in the folder.
    Returns the number of files processed.
    """
    txt_files = list(folder_path.glob("*.txt"))
    processed_count = 0
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Process tags
            new_content = process_tags(content, pokemon_name, tags_to_absorb)
            
            # Write back
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            processed_count += 1
        except Exception as e:
            print(f"Error processing {txt_file}: {e}")
    
    return processed_count


def main():
    """Main entry point for the CLI app."""
    print("Pokemon Dataset Curator")
    print("-" * 50)

    config = load_config()
    tags_to_absorb = set(tag.lower().strip() for tag in config.get("tags_to_absorb", []))

    while True:
        dataset_dir = input("\nEnter path to dataset directory (or press Enter to quit): ").strip()
        if not dataset_dir:
            print("Exiting.")
            break
        if not os.path.exists(dataset_dir):
            print(f"Error: Directory '{dataset_dir}' does not exist.")
            continue
        if not os.path.isdir(dataset_dir):
            print(f"Error: '{dataset_dir}' is not a directory.")
            continue

        dataset_path = Path(dataset_dir)
        all_folders = [f for f in dataset_path.iterdir() if f.is_dir()]

        if not all_folders:
            print("No folders found in the specified directory.")
            continue

        print(f"Found {len(all_folders)} dataset folders.")

        folders_to_process = []
        folders_to_rename = []
        unprocessed_folders = []

        for folder in all_folders:
            pokemon_name = extract_pokemon_name(folder.name)
            # Validate with ispokemon from pokedex_citron_db
            if pokemon_name is None:
                unprocessed_folders.append(f"{folder.name} (unrecognized format)")
            elif not ispokemon(pokemon_name.capitalize()):
                unprocessed_folders.append(f"{folder.name} (Pokemon name not in database)")
            else:
                folders_to_process.append((folder, pokemon_name))
                if should_rename_folder(folder.name, pokemon_name):
                    standard_name = get_standard_folder_name(pokemon_name)
                    folders_to_rename.append((folder, standard_name))

        # Rename folders first
        rename_map = {}
        for old_folder, new_name in folders_to_rename:
            new_path = old_folder.parent / new_name
            if new_path.exists():
                print(f"Warning: Cannot rename {old_folder.name} to {new_name} - target already exists.")
                continue
            try:
                old_folder.rename(new_path)
                rename_map[old_folder] = new_path
                print(f"Renamed: {old_folder.name} -> {new_name}")
            except Exception as e:
                print(f"Error renaming {old_folder.name}: {e}")

        # Update folders_to_process with new paths
        updated_folders = []
        for folder, pokemon_name in folders_to_process:
            if folder in rename_map:
                updated_folders.append((rename_map[folder], pokemon_name))
            else:
                updated_folders.append((folder, pokemon_name))
        folders_to_process = updated_folders

        # Process folders
        if folders_to_process:
            print(f"Processing {len(folders_to_process)} folders...")
            successful_count = 0

            for folder, pokemon_name in tqdm(folders_to_process, unit="folder"):
                try:
                    process_txt_files(folder, pokemon_name, tags_to_absorb)
                    successful_count += 1
                except Exception as e:
                    print(f"\nError processing {folder.name}: {e}")
                    unprocessed_folders.append(folder.name)

            print(f"Curated {successful_count} folders successfully.")

        # Display unprocessed folders report in terminal
        if unprocessed_folders:
            print(f"\n{len(unprocessed_folders)} unprocessed folder(s):")
            for folder_name in unprocessed_folders:
                print(f"Could not process: {folder_name}")
        else:
            print("All folders processed successfully.")


if __name__ == "__main__":
    main()
