import matplotlib.pyplot as plt
from caballo import FILAS

DIMENSION = FILAS


def generar_tablero():
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(0, DIMENSION)
    plt.ylim(0, DIMENSION)

    for i in range(DIMENSION + 1):
        plt.plot([i, i], [0, DIMENSION], color="black")
        plt.plot([0, DIMENSION], [i, i], color="black")
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if (i + j) % 2 == 0:
                    plt.fill(
                        [i, i + 1, i + 1, i],
                        [j, j, j + 1, j + 1],
                        color="white",
                        edgecolor="black",
                    )
                else:
                    plt.fill(
                        [i, i + 1, i + 1, i],
                        [j, j, j + 1, j + 1],
                        color="black",
                        edgecolor="black",
                    )


def dibujar_vector(x1, y1, x2, y2):
    plt.arrow(
        x1 + 0.5,
        y1 + 0.5,
        x2 - x1,
        y2 - y1,
        color="#D81E5B",
        head_width=0.1,
        length_includes_head=True,
    )


def generar_imagen(path: str, show: bool):
    import csv

    movimientos = []
    with open("movimientos.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            movimientos.append([int(x) for x in row])

    generar_tablero()

    # Plotea los vectores de acuerdo a los movimientos.
    for mov in movimientos:
        dibujar_vector(mov[0], mov[1], mov[2], mov[3])

    # Marco el punto de inicio.
    plt.plot(
        movimientos[0][0] + 0.5,
        movimientos[0][1] + 0.5,
        "o",
        color="#2374AB",
        markersize=20,
    )

    plt.plot(
        movimientos[-1][2] + 0.5,
        movimientos[-1][3] + 0.5,
        "X",
        color="#FA9F42",
        markersize=20,
    )

    plt.gca()
    try:
        plt.savefig(path)
        if show:
            plt.show()
    except KeyboardInterrupt:
        exit()
