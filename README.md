*This project has been created as part of the 42 curriculum by nahecre and relaforg*

# Description
The A-maze-ing project introduces ourselves to graphic programming. We have to implement a maze generation algorithm, a maze solver and a graphical interface in order to display the generated maze. The bonuses are really free, we choose to push on all aspects of the project. We now support 6 differents maze's shapes (rectabgle, square, circle, donut, diamond, ellipse). The solver is an A* algorithm for fast and efficient solving. On the display side, we choose to separate the app on two window, the main one displaying the maze and the seed and the second one with the buttons. The main window is resizeable with the '-' and '=' keys, you can also zoom onto the maze and moving into the maze with mouse draging.

# Insctructions
> [!WARNING]
> You must have the mlx installed onto your machine or virtual environment
### Dependencies
```bash
make install
```
### Usage
> [!TIP]
> You can modify the config.txt file
```bash
make run
```

# Ressources
 - Mlx documentation and exemples
 - ChatGPT to explain the left over questions
 - Wikipedia

# Config file
## Format

| Clé | Obligatoire | Format | Exemple | Description |
|----|------------|--------|---------|-------------|
| `WIDTH` | Yes | int | `129` | Maze width |
| `HEIGHT` | Yes | int | `97` | Maze height |
| `ENTRY` | Yes | `x, y` | `10, 18` | Entry coordinates |
| `EXIT` | Yes | `x, y` | `94, 67` | Exit coordinates |
| `OUTPUT_FILE` | Yes | str | `maze.txt` | output file |
| `PERFECT` | Yes | boolean | `True` | Indicate if the maze is perfect or not |
| `SEED` | Optional | int | `3377218501` | The seed used by random |
| `SHAPE` | Optional | str | `donut` | Maze shape (`rectangle`, `square`, `circle`, `donut`, `diamond`, `ellipse`). |

## Example

```ini
# Mandatory
WIDTH=129
HEIGHT=97
ENTRY=10, 18
EXIT=94, 67
OUTPUT_FILE=maze.txt
PERFECT=True

# Optional
SEED=3377218501
SHAPE=donut
```

## Remarks

- If `SEED` is not given, a random one will get used.
- If `SHAPE` is not given, the default shape is `rectangle`.
- The `ENTRY` and `EXIT` coordinates must be inside the maze and must not be the same.

# Maze generation
## Maze algorithm
ICI LEQUEL ET POURQUOI ET CE QUI EST REUTILISABLE ET COMMENT

# Team and Management
## Team
- Rémi LAFORGUE (relaforg): Data Analyst and Data Visualizer
- Nathan HECRE (nahecre): Computer whisperer

We worked in parallel, discussing implementations and features every days

