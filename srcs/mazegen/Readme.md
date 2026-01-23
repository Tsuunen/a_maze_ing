# MazeGen Module

Standalone maze generation module using DFS algorithm with A* pathfinding solver.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

```python
from mazegen import MazeGen
from mazegen.parser import Config

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
from mazegen.parser import Config

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
