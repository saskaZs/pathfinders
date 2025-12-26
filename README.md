# ⚡ Pathfinding Visualizer: Dijkstra vs. A*

> A real-time, interactive study of pathfinding algorithms and data structures using Python.

## 🎮 Overview

This project visualizes the "race" between two of the most fundamental pathfinding algorithms in Computer Science: **Dijkstra's Algorithm** and **A* (A-Star)**.

Unlike standard visualizers, this tool focuses on the **underlying data structures**. It renders a live, dynamic bar chart of the **Min-Heap (Priority Queue)**, allowing you to see exactly how each algorithm prioritizes which nodes to explore next.

![Demo Screenshot](https://github.com/user-attachments/assets/3375004b-0795-413d-b13a-40c209d6658a) **

## 📦 Installation & Run

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/pathfinding-viz.git](https://github.com/YOUR_USERNAME/pathfinding-viz.git)
    cd pathfinding-viz
    ```

2.  **Install dependencies**
    ```bash
    pip install matplotlib numpy
    ```

3.  **Run the visualization**
    ```bash
    python pathfinding_viz_final.py
    ```

---

## 🧠 Theoretical Background

### 1. The Engine: `heapq` (Binary Heap)
At the heart of both algorithms is the **Priority Queue**. In Python, this is implemented via the `heapq` module, which structures data as a **Binary Min-Heap**.



**How it works:**
* A Min-Heap is a binary tree where every parent node is **smaller or equal** to its children.
* The smallest element (highest priority) is *always* at the root (index 0).
* **Time Complexity:**
    * **Find Minimum:** $O(1)$ (Instant access to the "best" node).
    * **Push/Pop:** $O(\log N)$ (Very fast re-ordering).

**In this Visualizer:**
The bar charts at the bottom of the screen represent the heap.
* **Left bars (Short):** Nodes with low cost (High Priority). The algorithm will visit these next.
* **Right bars (Tall):** Nodes with high cost (Low Priority). These are in the queue but "far away."

### 2. Dijkstra's Algorithm
*The "Cautious Explorer"*

Invented by Edsger W. Dijkstra in 1956, this algorithm guarantees the shortest path by exploring outward in all directions evenly, like water spilling on the floor.

**The Math:**
It selects the next node based on **Cost so far**:
$$f(n) = g(n)$$
* $g(n)$: The exact distance traveled from the Start Node to node $n$.

**Behavior:**
Because it doesn't know where the goal is, it explores in a perfect circle (or diamond on a grid). It is thorough but computationally expensive because it visits many unnecessary nodes.

### 3. A* (A-Star) Algorithm
*The "Smart Seeker"*

A* is an extension of Dijkstra that uses a **Heuristic** to guide the search. It is "informed search"—it guesses which direction is correct.

**The Math:**
It selects the next node based on **Total Estimated Cost**:
$$f(n) = g(n) + h(n)$$
* $g(n)$: The exact distance traveled so far.
* $h(n)$: The **Heuristic** (Estimated distance to the Goal).



**The Heuristic used ($h(n)$):**
We use **Manhattan Distance** (Taxicab geometry), which is ideal for grid-based movement where diagonal moves are not allowed:
$$h(n) = |x_{current} - x_{goal}| + |y_{current} - y_{goal}|$$

**Behavior:**
By adding $h(n)$, the algorithm penalizes nodes that move away from the target. This forces the Priority Queue (`heapq`) to sort nodes that are physically closer to the goal to the front of the line.

---

## 📊 Comparison Summary

| Feature | Dijkstra | A* (A-Star) |
| :--- | :--- | :--- |
| **Strategy** | Uninformed (Brute Force) | Informed (Heuristic) |
| **Equation** | $f(n) = g(n)$ | $f(n) = g(n) + h(n)$ |
| **Guarantee** | Always finds shortest path | Always finds shortest path (if heuristic is admissible) |
| **Speed** | Slower (Visits more nodes) | Faster (Visits fewer nodes) |
| **Visual Shape** | Expands in a Diamond/Circle | Expands like a Spear/Beam |

## 🛠️ Tech Stack
* **Python 3**
* **Matplotlib:** For rendering the grid and live data charts.
* **NumPy:** For efficient grid management.
* **Heapq:** Standard Python library for the priority queue implementation.
