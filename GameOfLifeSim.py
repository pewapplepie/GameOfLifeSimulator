from matplotlib import style
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time
from typing import Set, Tuple
from lifeLogic import updateBoard, place_pattern
import matplotlib.patches as patches

style.use("seaborn-v0_8")

# Streamlit app
st.title("Conway's Game of Life Streamlit")
st.sidebar.subheader("Introduction")
st.sidebar.write(
    "I came across this interesting topic when I was doing leetcode. I found it fascinating so I decided to delve deeper. "
    "This project primarily served as a learning and exploring exercise for me, so feel free to provide any suggestion. The Game of Life has been extensively studied, and many impressive examples are already available. "
    "However, I believe it is a perfect topic to explore building an algorithm simulation with Streamlit! 😎"
)

st.sidebar.write(
    "If this is the first time you heard of *The Game of Life*, it is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively)"
)
st.sidebar.write(
    "Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent."
)
st.sidebar.markdown(
    """
    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""
)
st.sidebar.write(
    "With the above rules on the board, let's set the initial state and watch it evolve!"
)
st.sidebar.divider()
# Sidebar controls
st.sidebar.title("Controls")
update_interval = st.sidebar.slider("Update interval (seconds)", 0.1, 2.0, 0.5)
cols = rows = st.sidebar.slider("Grid size", 10, 100, 50)
if "Rows" not in st.session_state:
    st.session_state.Cols = cols
    st.session_state.Rows = rows
# Initialize the board with an empty pattern
if "live_cells" not in st.session_state:
    st.session_state.live_cells = set()
    st.session_state.run_simulation = False
    st.session_state.step_count = 0
    st.session_state.population = []


def start_simulation():
    st.session_state.run_simulation = True


def stop_simulation():
    st.session_state.run_simulation = False


def reset_simulation():
    st.session_state.live_cells = set()
    st.session_state.step_count = 0
    st.session_state.population = []


def add_random_lives(nlives):
    st.session_state.live_cells |= {
        (np.random.randint(rows), np.random.randint(cols)) for _ in range(nlives)
    }


def add_pattern(pattern_name):
    if pattern_name == "Gosper glider gun" and st.session_state.Rows < 50:
        st.session_state.Rows = 50
        st.session_state.Cols = 50
        fig = plot_grid(
            st.session_state.live_cells, st.session_state.Rows, st.session_state.Cols
        )
        placeholder.pyplot(fig)
        plt.close(fig)

    st.session_state.live_cells = place_pattern(
        pattern_name,
        st.session_state.live_cells,
        (st.session_state.Rows, st.session_state.Cols),
    )


# Sidebar buttons
st.sidebar.button("Start Simulation", on_click=start_simulation)
st.sidebar.button("Stop Simulation", on_click=stop_simulation)
st.sidebar.button("Reset Simulation", on_click=reset_simulation)

st.sidebar.subheader("Random Lives")
nlives = st.sidebar.number_input("Number of lives", value=10, step=10)
st.sidebar.button("Add Random Lives", on_click=lambda: add_random_lives(nlives))

st.sidebar.subheader("Still Lives")
st.sidebar.write(
    "The lives in next generation will be the same state as the current and so on"
)
st.sidebar.button("Add Tub", on_click=lambda: add_pattern("Tub"))
st.sidebar.button("Add Block", on_click=lambda: add_pattern("Block"))
st.sidebar.button("Add Loaf", on_click=lambda: add_pattern("Loaf"))
st.sidebar.subheader("Oscillators")
st.sidebar.write(
    "The lives will return to their initial state after a finite number of generations"
)
st.sidebar.button("Add Blinker", on_click=lambda: add_pattern("Blinker"))
st.sidebar.button("Add Toad", on_click=lambda: add_pattern("Toad"))
st.sidebar.subheader("SpaceShips")
st.sidebar.write("The patterns will translate themselves across the grid.")
st.sidebar.button("Add Glider", on_click=lambda: add_pattern("Glider"))
st.sidebar.button(
    "Add Light-weight spaceship", on_click=lambda: add_pattern("Light-weight spaceship")
)
st.sidebar.button(
    "Add Middle-weight spaceship",
    on_click=lambda: add_pattern("Middle-weight spaceship"),
)
st.sidebar.button(
    "Add Heavy-weight spaceship", on_click=lambda: add_pattern("Heavy-weight spaceship")
)

st.sidebar.subheader("Indefinetly Growth")
st.sidebar.write(
    "With a finite number of living cells, the population grow beyond some finite upper limit"
)
st.sidebar.button(
    "Add Gosper glider gun", on_click=lambda: add_pattern("Gosper glider gun")
)
st.sidebar.warning("make sure the matrix view has size over 50x50")

placeholder = st.empty()


def plot_grid(live_cells, rows, cols):

    grid = np.zeros((rows, cols))
    for i, j in live_cells:
        if 0 <= i < rows and 0 <= j < cols:
            grid[i, j] = 1

    fig, ax = plt.subplots()
    cmap = mcolors.ListedColormap(["white", "black"])
    bounds = [0, 0.5, 1]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(grid, cmap=cmap, norm=norm)

    # Draw grid lines
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="grey", linestyle="--", linewidth=0.5)

    ax.tick_params(which="minor", size=0)
    ax.set_xticks([])
    ax.set_yticks([])

    return fig


# (f"Debugging - Rows: {st.session_state.Rows} Cols: {st.session_state.Cols}")
# Display initial grid

fig = plot_grid(
    st.session_state.live_cells, st.session_state.Rows, st.session_state.Cols
)
placeholder.pyplot(fig)
plt.close(fig)

# Run simulation
while st.session_state.run_simulation:
    if len(st.session_state.live_cells) == 0:
        st.subheader("Oops! All lives are dead! 😢")
        st.session_state.run_simulation = False
        break
    live_cells = st.session_state.live_cells
    live_cells = updateBoard(live_cells)
    st.session_state.live_cells = live_cells
    st.session_state.step_count += 1
    st.session_state.population.append(len(live_cells))

    fig = plot_grid(live_cells, st.session_state.Rows, st.session_state.Cols)
    placeholder.pyplot(fig)
    plt.close(fig)

    time.sleep(update_interval)

# Display current grid if simulation is stopped
if not st.session_state.run_simulation:
    fig = plot_grid(
        st.session_state.live_cells, st.session_state.Rows, st.session_state.Cols
    )
    placeholder.pyplot(fig)
    plt.close(fig)

# Display population and generation data
st.sidebar.subheader("Simulation Data")
st.sidebar.write(f"Generations: {st.session_state.step_count}")
st.sidebar.write(f"Current Population: {len(st.session_state.live_cells)}")
st.sidebar.line_chart(st.session_state.population)
