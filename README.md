# Lattice
- Maple Leaf Lattice
- Kagome Lattice


## Installation
```bash
pip install -r ./requirements.txt
```
- Note: create python virtual environment tutorial (.venv)
    ```bash
    python -m venv .venv
    ```
- Activate the virtual environment
    for linux or MacOS:
    ```bash
    source .venv/bin/activate
    ```
    for windows:
    ```bash
    ./.venv/Scripts/Activate.ps1
    ```

## Parameter Usage
- `-L`: Length
- `-W`: Width
- **(optional Parameters :arrow_down:)** 
- `--inputFile`: read graph from dwave results (files are in `./results/` folder)
- `--saveFig`: add this param to save Figure
- `--saveLattice`: add this param to save lattice file
- `--displayType`: choose the Figure type ( `plain`, `spinfile`, `orderP` )
  - `plain`: no color for nodes
  - `spinfile`: separate color for spins up and down in dwave results
  - `orderP`: order parameters triangular node hint mark

## Run Examples
- Triangular Script Example:
    ```bash
    python ./triangular/main.py -L 12 -W 12 --inputFile ./results/triangular/HYBRID/tri_L12_JL_1.0_HYBRID_sam1_.txt
    ```
- Kagome Script Example:
    ```bash
    python ./kagome/main.py -L 12 -W 12 --inputFile ./results/kagome/HYBRID/kagome_L_12_12_HYBRID_sam1_.txt --displayType spinfile
    ```
- MapleLeaf Script Example::
    ```bash
    python ./maple-leaf/main.py -L 14 -W 14 --inputFile ./results/mapleleaf/HYBRID/mapleleaf_L_14_14_HYBRID_sam1_.txt --displayType orderP
    ```

> [!Note]
> add `--saveFig` if want to save Figure
> add `--saveLattice` if want to save Lattice File

> [!Note]
> if not giving `--displayType` params, 
> default will be `spinfile` when **using** `inputFile`, 
> and `plain` for **not using** `inputFile`


## Regulation of Lattice 
### Triangular
- Total Energy:  L^2
### Kagome 
- Total Energy:  $\dfrac{L^2}{2}$
- Total Nodes
    - $L^2 - (L/2) ^2$
    - ex: L: 120 = 14400 - 3600 = 10800
### Maple Leaf
- Total Energy:  L^2
    - Dwave Hybrid do well until L 77
    - L84：
        - Hybrid：-7052
        - **Answer**：-7056
- Total Nodes
    - $L^2 - L * (L/7)$
    - $L^2 - \dfrac{L^2}{7} = \dfrac{6}{7}L^2$
    - ex: L 42: 42 * 42 - 42 * 6
    - ex: L 119: 119^2 - 119 * 17 = 14161 - 2023 = 12138
    - ex: L 140: 19600 - 140 * 20 = 19600 - 2800 = 16800