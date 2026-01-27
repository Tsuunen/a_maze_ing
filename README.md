*This project has been created as part of the 42 curriculum by nahecre and relaforg*

# Description
The A-maze-ing project introduces ourselves to graphic programming. We have to implement a maze generation algorithm, a maze solver and a graphical interface in order to display the generated maze. The bonuses are really free, we chose to push on all aspects of the project. We now support 6 differents maze's shapes (rectabgle, square, circle, donut, diamond, ellipse). The solver is an A* algorithm for fast and efficient solving. On the display side, we chose to separate the app on two window, the main one displaying the maze and the seed and the second one with the buttons. The main window is resizeable with the '-' and '=' keys, you can also zoom onto the maze and moving into the maze with mouse draging.

# Insctructions
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

| Key | Mandatory | Format | Example | Description |
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
For maze generation we used a randomized dfs algorithm, wich always creates a perfect maze, so a scramble function has been implemented to remove random walls inside the maze, for the solving part, we could have got it when generating but we thought it would be more interesting to implement the A* algorithm.

# MazeGen Module

Standalone maze generation module using DFS algorithm with A* pathfinding solver.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

```python
from mazegen import MazeGen
from mazegen.config_parser import Config

# Create configuration
config = Config(
    width=20,
    height=20,
    entry=(0, 0),
    exit=(19, 19),
    shape="rectangle",
    perfect=True,
    output_file="maze.txt"
)

# Generate maze
generator = MazeGen(config)
generator. dfs()

# Export to file
generator.export_maze_file()

# Or get as object
maze = generator.export_maze_obj()
print(f"Solution:  {maze.path}")
```## Custom Parameters

### Size
```python
config = Config(width=50, height=30, entry=(0,0), exit=(49,29), 
                shape="rectangle", perfect=True, output_file="out.txt")
```

### Seed (for reproducibility)
```python
config = Config(... , seed=42)      # Fixed seed
config = Config(..., seed=None)    # Random seed
```

### Shapes
Available shapes:  `rectangle`, `square`, `circle`, `ellipse`, `diamond`, `donut`

```python
config = Config(... , shape="circle")
```

### Perfect vs Imperfect Mazes
```python
config = Config(..., perfect=True)   # One unique solution
config = Config(..., perfect=False)  # Multiple paths possible
```

## Accessing the Generated Structure

### As a Maze object
```python
maze = generator.export_maze_obj()

# Access properties: 
print(maze.maze)       # Hexadecimal string representation
print(maze.entry)      # Entry coordinates (x, y)
print(maze.exit)       # Exit coordinates (x, y)
print(maze.path)       # Solution path:  "NESW..." format
print(maze.nbr_cols)   # Width
print(maze.nbr_rows)   # Height
print(maze.seed)       # Seed used for generation
```

### Solution Format
The `path` attribute contains the solution as a string of directions:
- `N` = North (up)
- `S` = South (down)
- `E` = East (right)
- `W` = West (left)
#### `MazeGen(config:  Config)`
Main maze generator class.

**Methods:**
- `dfs()` - Generate the maze using depth-first search algorithm
- `export_maze_file()` - Export maze to file specified in config
- `export_maze_obj()` - Return Maze object
- `solve()` - Get solution path as string

#### `Maze`
Pydantic model representing a generated maze.

**Attributes:**
- `maze: str` - Hexadecimal representation of the maze
- `entry: tuple[int, int]` - Entry coordinates
- `exit: tuple[int, int]` - Exit coordinates
- `path: str` - Solution path
- `nbr_cols: int` - Number of columns (width)
- `nbr_rows: int` - Number of rows (height)
- `seed: int | None` - Seed used for generation

#### `Config`
Configuration object for maze generation.

**Parameters:**
- `width: int` - Maze width
- `height: int` - Maze height
- `entry: tuple[int, int] | str` - Entry coordinates
- `exit: tuple[int, int] | str` - Exit coordinates
- `shape: str` - Maze shape
- `perfect: bool` - Perfect maze flag
- `output_file: str` - Output file path
- `seed: int | None` - Random seed (optional)

## Examples

### Simple rectangular maze
```python
from mazegen import MazeGen
from mazegen.config_parser import Config

config = Config(
    width=10, 
    height=10, 
    entry=(0, 0), 
    exit=(9, 9),
    shape="rectangle",
    perfect=True,
    output_file="simple_maze.txt"
)

gen = MazeGen(config)
gen.dfs()
gen.export_maze_file()
```

# Team and Management
## Team
- Rémi LAFORGUE (relaforg): Data Analyst and Data Visualizer
- Nathan HECRE (nahecre): Computer whisperer

We worked in parallel, discussing implementations and features every days

