"""
Advanced Pathfinding Visualizer (Dijkstra vs A*)
================================================
"""

import heapq
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.colors import ListedColormap
from typing import List, Tuple, Generator, Dict

# --- CONFIGURATION ---
GRID_SIZE = 30
OBSTACLE_DENSITY = 0.3  # 30% of the map is walls
START_NODE = (2, 2)
END_NODE = (27, 27)
ANIMATION_SPEED = 0.001  # Lower = Faster

# --- COLOR PALETTE ---

COLORS = {
    'background': '#0f0f12', # Almost black
    'wall':       '#2d2d3a', # Dark Grey
    'visited':    '#240046', # Deep Purple (Closed Set)
    'queued':     '#00b4d8', # Neon Blue (Open Set)
    'path':       '#39ff14', # Neon Green (Final Path)
    'start':      '#ffffff', # White
    'end':        '#ff006e', # Neon Pink
    'heap_bar':   '#7209b7'  # Purple for heap bars
}

# Map grid values to colors
# 0:Empty, 1:Wall, 2:Queued, 3:Visited, 4:Path
CMAP_LIST = [COLORS['background'], COLORS['wall'], COLORS['queued'], COLORS['visited'], COLORS['path']]
CMAP = ListedColormap(CMAP_LIST)

class PathfindingEngine:
    """Core logic for pathfinding algorithms."""
    
    def __init__(self, size: int, density: float):
        self.size = size
        # Generate fixed grid
        self.grid = np.random.choice([0, 1], size=(size, size), p=[1-density, density])
        self.grid[START_NODE] = 0
        self.grid[END_NODE] = 0
        self.visual_grid = self.grid.copy()
        
        # Stats
        self.nodes_explored = 0

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """Manhattan Distance Heuristic for A*."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for dx, dy in directions:
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < self.size and 0 <= y < self.size and self.grid[x, y] == 0:
                neighbors.append((x, y))
        return neighbors

    def run(self, algo_type: str) -> Generator:
        """
        Main algorithm loop.
        Yields: (Grid State, Heap Priority List)
        """
        # Priority Queue stores: (Priority_Score, Node_Coordinates)
        pq = []
        heapq.heappush(pq, (0, START_NODE))
        
        came_from = {START_NODE: None}
        cost_so_far = {START_NODE: 0}
        self.nodes_explored = 0

        while pq:
            # --- HEAP VISUALIZATION DATA ---
            # Extract the 'Priority Score' from the top 50 items in the heap.
            # We sort them for the bar chart to show the "Slope" of the heap.
            # A flattened slope = broad search. A steep slope = focused search.
            raw_heap = heapq.nsmallest(50, pq)
            heap_priorities = [item[0] for item in raw_heap]

            # --- ALGORITHM STEP ---
            current_prio, current = heapq.heappop(pq)

            if current == END_NODE:
                break

            if current != START_NODE:
                self.visual_grid[current] = 3 # Mark Visited
                self.nodes_explored += 1

            for next_node in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    
                    # PRIORITY CALCULATION
                    priority = new_cost
                    if algo_type == "astar":
                        priority += self.heuristic(next_node, END_NODE) * 1.5 # 1.5 is a tie-breaker weight
                    
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current
                    
                    if next_node != END_NODE:
                        self.visual_grid[next_node] = 2 # Mark Queued
            
            yield self.visual_grid, heap_priorities

        # Path Reconstruction
        curr = END_NODE
        path_found = False
        if END_NODE in came_from:
            path_found = True
            while curr != START_NODE:
                self.visual_grid[curr] = 4
                curr = came_from[curr]
                yield self.visual_grid, [] # Yield to animate the path drawing
            self.visual_grid[START_NODE] = 4

        yield self.visual_grid, ["DONE"]


def run_dashboard():
    plt.style.use('dark_background')
    
    # 1. Setup Grid Layout (2 Rows, 2 Columns)
    # Row 0: The Maps
    # Row 1: The Heap Visualizations
    fig = plt.figure(figsize=(14, 8))
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1.5])
    fig.canvas.manager.set_window_title('Pathfinding Algorithms & Data Structures')

    # 2. Initialize Engines
    engine_dijkstra = PathfindingEngine(GRID_SIZE, OBSTACLE_DENSITY)
    
    # Clone grid for fairness
    engine_astar = PathfindingEngine(GRID_SIZE, 0)
    engine_astar.grid = engine_dijkstra.grid.copy()
    engine_astar.visual_grid = engine_dijkstra.visual_grid.copy()

    # 3. Create Subplots
    ax_map_d = fig.add_subplot(gs[0, 0])
    ax_map_a = fig.add_subplot(gs[0, 1])
    ax_heap_d = fig.add_subplot(gs[1, 0])
    ax_heap_a = fig.add_subplot(gs[1, 1])

    # 4. Config Maps
    img_d = ax_map_d.imshow(engine_dijkstra.visual_grid, cmap=CMAP, vmin=0, vmax=4)
    img_a = ax_map_a.imshow(engine_astar.visual_grid, cmap=CMAP, vmin=0, vmax=4)
    
    for ax, title in zip([ax_map_d, ax_map_a], ["Dijkstra's Algorithm", "A* (A-Star) Algorithm"]):
        ax.set_title(title, fontsize=14, color=COLORS['queued'], fontweight='bold', pad=10)
        ax.axis('off')
        # Markers
        ax.text(START_NODE[1], START_NODE[0], 'S', ha='center', va='center', color='black', fontweight='bold')
        ax.text(END_NODE[1], END_NODE[0], 'E', ha='center', va='center', color='black', fontweight='bold')

    # 5. Config Heap Charts
    bar_d = ax_heap_d.bar(range(50), [0]*50, color=COLORS['heap_bar'], alpha=0.8)
    bar_a = ax_heap_a.bar(range(50), [0]*50, color=COLORS['heap_bar'], alpha=0.8)

    for ax in [ax_heap_d, ax_heap_a]:
        ax.set_ylim(0, GRID_SIZE * 2.5)
        ax.set_facecolor(COLORS['background'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_color('gray')
        ax.tick_params(axis='x', colors='gray')
        ax.tick_params(axis='y', colors='gray')
        ax.set_xlabel("Queue Position (First 50 Nodes)", fontsize=9, color='gray')
        ax.set_ylabel("Priority Score (Lower = Better)", fontsize=9, color='gray')
        
    ax_heap_d.set_title("Dijkstra Heap Structure", fontsize=10, color='white')
    ax_heap_a.set_title("A* Heap Structure", fontsize=10, color='white')

    # 6. Generators
    gen_d = engine_dijkstra.run("dijkstra")
    gen_a = engine_astar.run("astar")

    print("Running simulation...")

    finished_d = False
    finished_a = False

    def update_bars(bars, data):
        for rect, h in zip(bars, data):
            rect.set_height(h)
        # Clear unused bars
        for i in range(len(data), len(bars)):
            bars[i].set_height(0)

    while not (finished_d and finished_a):
        # Update Dijkstra
        if not finished_d:
            try:
                grid, heap = next(gen_d)
                if heap == ["DONE"]: 
                    finished_d = True
                else:
                    img_d.set_data(grid)
                    if heap: update_bars(bar_d, heap)
                    ax_map_d.set_xlabel(f"Nodes Explored: {engine_dijkstra.nodes_explored}", color='white')
            except StopIteration:
                finished_d = True

        # Update A*
        if not finished_a:
            try:
                grid, heap = next(gen_a)
                if heap == ["DONE"]: 
                    finished_a = True
                else:
                    img_a.set_data(grid)
                    if heap: update_bars(bar_a, heap)
                    ax_map_a.set_xlabel(f"Nodes Explored: {engine_astar.nodes_explored}", color='white')
            except StopIteration:
                finished_a = True

        plt.pause(ANIMATION_SPEED)

    plt.show()

if __name__ == "__main__":
    run_dashboard()