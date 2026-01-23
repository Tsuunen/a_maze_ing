"""Maze generation module using DFS algorithm with A* pathfinding solver"""

from .maze_gen import Maze, MazeGen, AStar
from .parser import Config

__version__ = "1.0.0"
__all__ = ["Maze", "MazeGen", "AStar", "Config"]
