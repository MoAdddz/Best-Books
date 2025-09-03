import matplotlib.pyplot as plt
import numpy as np

# Grid size
grid_size = 20
grid = np.zeros((grid_size, grid_size))

# Create plot
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='Greys', origin='lower')

# Set major ticks
ax.set_xticks(np.arange(grid_size))
ax.set_yticks(np.arange(grid_size))
ax.set_xticklabels(np.arange(grid_size))
ax.set_yticklabels(np.arange(grid_size))

# Draw grid lines
ax.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
ax.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
ax.grid(which='minor', color='black', linewidth=0.5)
ax.tick_params(which='minor', bottom=False, left=False)

# Set aspect ratio
ax.set_aspect('equal')

# Show window
plt.show()
