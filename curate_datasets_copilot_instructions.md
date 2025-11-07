## 🧭 `instructions.md` — Build Instructions for Copilot

### 📝 Overview
Create a **Python CLI app** that curates Pokémon dataset folders in preparation for LoRA training.  
Each dataset folder contains `.png` image files and corresponding `.txt` files with comma-separated tags.  
This app will:
1. Clean and modify the tags in each `.txt` file according to specific rules.
2. Add a trigger tag to each `.txt` file.
3. Rename dataset folders to a standardized format if needed.
4. Report any folders that could not be processed.

---

### 📂 Folder Structure
The input directory contains multiple Pokémon dataset folders.  
Example:
```
datasets/
├── pikachuPokedex_IXL/
│   ├── 00001.png
│   ├── 00001.txt
│   ├── 00002.png
│   ├── 00002.txt
├── eevee_(pokemon)/
│   ├── 00001.png
│   ├── 00001.txt
```

---

### ⚙️ Functionality Requirements

#### 1. CLI Behavior
- When run (e.g., `python curate_datasets.py`), the app will:
  - Prompt the user for the **directory path** to process.
  - Display a **progress bar** using `tqdm` while processing files.
- It should **overwrite** the `.txt` files in place (no backups needed).
- No colored output — just clean text logging.

---

#### 2. Recognized Dataset Folder Formats
The app will recognize dataset folders using these rules:

| Format | Description | Example | Action |
|--------|--------------|----------|--------|
| `pokemon_namePokedex_IXL` | Correct format | `PikachuPokedex_IXL` | Process as is |
| `pokemon_name_(pokemon)` | Acceptable alternate | `pikachu_(pokemon)` | Rename to `PikachuPokedex_IXL` |
| `pokemon_name` (no special characters) | Acceptable alternate | `pikachu` | Rename to `PikachuPokedex_IXL` |
| Other / unrecognized | Invalid format | `pikachu-variant` | Skip and report |

**Recognized special characters:** `_`, `-`, `(`, `)`.

If the folder name doesn’t match any recognized pattern, it will not be processed, and the app will record it in a **report file** (e.g., `unprocessed_datasets.txt`).

---

#### 3. Tag Processing Rules

Each `.txt` file contains a comma-separated list of tags.  
Example input:
```
pikachu_(pokemon), 1girl, yellow_theme, standing, pokemon
```

##### The app must:
1. Remove any tag matching the Pokémon’s name in the format `pokemon_name_(pokemon)`.
2. Remove any tags listed in the config file’s `tags_to_absorb` field.
3. Add a **trigger tag** at the **beginning** of each tag list, formatted as:  
   ```
   zz{PokemonNameCapitalized}C1tr0n
   ```
   Example: `zzPikachuC1tr0n`
4. Clean tags:
   - Trim spaces.
   - Convert to lowercase (except the trigger, which should retain its exact capitalization).
   - Remove duplicates.
   - Remove empty entries.
   - Rejoin tags into a comma-separated line.

Example output:
```
zzPikachuC1tr0n, 1girl, yellow_theme, standing
```

---

#### 4. Config File
The app should read a config file named `config.json` in the same directory as the script.  
Example:
```json
{
    "tags_to_absorb": ["pokemon", "blurry", "bad_quality"]
}
```

---

#### 5. Error Reporting
If a dataset folder cannot be recognized (doesn’t match any valid naming format),  
the app must:
- Skip processing that folder.
- Append its name to a report file named:
  ```
  unprocessed_datasets.txt
  ```
  Example contents:
  ```
  Could not process: pikachu-test_v2
  Could not process: bulbasauredit
  ```

---

#### 6. Dependencies
Create a `requirements.txt` file listing all dependencies required by the app.  
It should include at least:
```
tqdm
```
and any other modules used for:
- JSON file handling
- File/directory operations
- Logging or path management

---

### 🧙‍♂️ Implementation Notes
- Use only **standard Python libraries** and `tqdm`.
- Use `os` or `pathlib` to navigate directories.
- Use `json` to read the config file.
- The main script file should be named `curate_datasets.py`.
- Include basic error handling and user-friendly messages (e.g., if directory doesn’t exist or config missing).

---

### ✅ Example Run

**Command:**
```bash
python curate_datasets.py
```

**Terminal Output:**
```
Enter path to dataset directory: datasets
Found 12 dataset folders.
Renamed: eevee_(pokemon) -> EeveePokedex_IXL
Processing 12 folders...
100%|███████████████████████████████████████| 12/12 [00:04<00:00,  3.00it/s]
Curated 11 folders successfully.
1 unprocessed folder recorded in unprocessed_datasets.txt.
```

