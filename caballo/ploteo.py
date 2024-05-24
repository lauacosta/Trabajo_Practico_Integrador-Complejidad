import matplotlib.pyplot as plt


# Function to draw a chessboard
def generar_tablero():
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(0, 8)
    plt.ylim(-8, 0)

    for i in range(9):
        plt.plot([i, i], [0, -8], color="black")
        plt.plot([0, 8], [-i, -i], color="black")

    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                plt.fill(
                    [i, i + 1, i + 1, i],
                    [-j, -j, -(j + 1), -(j + 1)],
                    color="white",
                    edgecolor="black",
                )
            else:
                plt.fill(
                    [i, i + 1, i + 1, i],
                    [-j, -j, -(j + 1), -(j + 1)],
                    color="black",
                    edgecolor="black",
                )


def dibujar_vector(x1, y1, x2, y2):
    plt.arrow(
        x1 + 0.5,
        -y1 - 0.5,
        x2 - x1,
        -(y2 - y1),
        color="blue",
        head_width=0.1,
        length_includes_head=True,
    )


def generar_imagen():
    import csv

    movements = []
    with open("movimientos.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            movements.append([int(x) for x in row])

    # Plot the chessboard
    generar_tablero()

    # Plot the movements
    for move in movements:
        dibujar_vector(move[0], move[1], move[2], move[3])

    # Mark the starting point with a yellow circle
    plt.plot(
        movements[0][0] + 0.5,
        -movements[0][1] - 0.5,
        "o",
        color="yellow",
        markersize=10,
    )

    plt.gca().invert_yaxis()  # Invert y-axis to match the chessboard orientation
    plt.show()
