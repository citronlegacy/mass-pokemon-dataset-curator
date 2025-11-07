# Pokémon Dataset Curator

A Python CLI tool for curating Pokémon dataset folders in preparation for LoRA training. This app cleans and standardizes tag files, renames folders, and reports any issues, making your datasets ready for machine learning workflows.

## Features

- **Interactive CLI**: Prompts for dataset directory paths and processes multiple folders in one run.
- **Tag Cleaning**: Cleans and modifies tags in each `.txt` file according to strict rules.
- **Trigger Tag**: Adds a unique trigger tag to each tag file for LoRA training.
- **Folder Renaming**: Renames dataset folders to a standardized format if needed.
- **Error Reporting**: Reports any folders that could not be processed due to invalid naming or missing Pokémon names.
- **Progress Bar**: Displays progress using `tqdm` for a smooth user experience.

## How It Works

1. **Prompt for Directory**: When you run the app, it asks for the path to your dataset directory.
2. **Recognized Folder Formats**:
   - `PokemonNamePokedex_IXL` (e.g., `PikachuPokedex_IXL`)
   - `pokemon_name_(pokemon)` (e.g., `eevee_(pokemon)`)
   - `pokemon_name` (e.g., `eevee`)
   - `pokemon_name_pokemon` (e.g., `Samurott_pokemon`)
   - Other formats are skipped and reported.
3. **Tag Processing**:
   - Removes tags matching the Pokémon name in the format `pokemon_name_(pokemon)`.
   - Removes tags listed in the config file's `tags_to_absorb` field.
    - Adds a trigger tag at the beginning: `zz{PokemonNameCapitalized}C1tr0n` (e.g., `zzPikachuC1tr0n`).
     
       **Note:** The trigger uses the code `C1tr0n` by default. You should update the trigger code in the script to match your own owner or project standards if needed.
   - Cleans tags: trims spaces, converts to lowercase (except the trigger), removes duplicates and empty entries.
   - Overwrites `.txt` files in place.
4. **Folder Renaming**: Acceptable alternate formats are renamed to the standard format.
5. **Error Reporting**: Unrecognized folders are reported in the terminal with the reason (unrecognized format or name not in database).

## Example Usage

```bash
python mass_pokemon_dataset_curator.py
```

**Terminal Output:**
```
Pokemon Dataset Curator
--------------------------------------------------
Enter path to dataset directory (or press Enter to quit): datasets
Found 12 dataset folders.
Renamed: eevee_(pokemon) -> EeveePokedex_IXL
Processing 12 folders...
100%|███████████████████████████████████████| 12/12 [00:04<00:00,  3.00it/s]
Curated 11 folders successfully.
1 unprocessed folder(s):
Could not process: pikachu-test_v2 (unrecognized format)
```

## Configuration

Create a `config.json` file in the project directory:

```json
{
    "tags_to_absorb": ["pokemon", "pokemon (creature)", "no humans"]
}
```

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Required packages:
- tqdm
- (Standard Python libraries: os, pathlib, json, re)

## License

This project is licensed under the MIT License.

## Repository

GitHub: https://github.com/citronlegacy/mass-pokemon-dataset-curator
