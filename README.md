# Lattice
- Maple Leaf Lattice
- Kagome Lattice


## Installation
```bash
pip install -r ./requirements.txt
```

## Usage
- `-L`: Length
- `-W`: Width
- `--saveFig`: store the Figure
- `--inputFile`: **not necessary** read graph from dwave results (files are in `./results/` folder)
- `--saveLattice`: **not necessary**, add if want to save lattice file

## Run Examples
- Triangular Script Example:
    ```bash
    python ./triangular/main.py -L 3 -W 3 --inputFile ./results/triangular/HYBRID/tri_L102_JL_1.0_HYBRID_sam1_.txt
    ```
- Kagome Script Example:
    ```bash
    python ./kagome/main.py -L 12 -W 12 --inputFile ./results/kagome/HYBRID/kagome_L_12_12_HYBRID_sam1_.txt
    ```
- MapleLeaf Script Example::
    ```bash
    python ./maple-leaf/main.py -L 7 -W 7 --inputFile ./results/mapleleaf/HYBRID/mapleleaf_L_7_7_HYBRID_sam1_.txt
    ```

> [!Note]
> add `--saveFig` if want to save Figure


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
    - Dwave Hybrid 做好到 L 77
    - L84：
        - Hybrid：-7052
        - **Answer**：-7056
- Total Nodes
    - $L^2 - L * (L/7)$
    - $L^2 - \dfrac{L^2}{7}$
    - ex: L 42: 42 * 42 - 42 * 6
    - ex: L 119: 119^2 - 119 * 17 = 14161 - 2023 = 12138
    - ex: L 140: 19600 - 140 * 20 = 19600 - 2800 = 16800