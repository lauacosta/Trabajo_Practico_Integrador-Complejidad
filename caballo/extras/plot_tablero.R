# Function to draw a chessboard
draw_chessboard <- function() {
  # Create an empty plot with appropriate limits
  plot(NA, xlim = c(0, 8), ylim = c(-8, 0), xlab = "", ylab = "", asp = 1, axes = FALSE)
  
  # Draw the chessboard grid
  for (i in 0:8) {
    lines(c(i, i), c(0, -8), col = "black")
    lines(c(0, 8), c(-i, -i), col = "black")
  }
  
  # Create the chessboard
  for (i in 0:7) {
    for (j in 0:7) {
      if ((i + j) %% 2 == 0) {
        rect(i, -j, i + 1, -(j + 1), col = "white", border = "black")
      } else {
        rect(i, -j, i + 1, -(j + 1), col = "black", border = "black")
      }
    }
  }
}

# Function to draw a vector representing movement
draw_vector <- function(x1, y1, x2, y2) {
  # Calculate center of start and end tile
  x_start <- x1 + 0.5
  y_start <- -y1 - 0.5
  x_end <- x2 + 0.5
  y_end <- -y2 - 0.5
  
  # Draw vector from center of start tile to center of end tile
  arrows(x_start, y_start, x_end, y_end, col = "blue", length = 0.1, lwd = 2)
}

# Read movements from CSV file
movements <- read.csv("movements.csv")

# Plot the chessboard
draw_chessboard()

# Plot the movements
for (i in 1:nrow(movements)) {
  draw_vector(movements[i, "x1"], movements[i, "y1"], movements[i, "x2"], movements[i, "y2"])
}

# Mark the starting point with a yellow circle
points(movements[1, "x1"] + 0.5, -movements[1, "y1"] - 0.5, col = "yellow", pch = 16, cex = 2)
