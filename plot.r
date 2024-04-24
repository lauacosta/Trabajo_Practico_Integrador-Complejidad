library("ggplot2")
t <- read.table('data.dat', header=TRUE)
ggplot(t, aes(tamaño, tiempo, colour = nombre)) + geom_point() + geom_smooth()
