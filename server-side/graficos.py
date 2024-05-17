import seaborn as sns
import matplotlib.pyplot as plt


# Scatter Plot - Gráfico de Dispersão
def scatter_plot(x, y, filename):
    sns.scatterplot(x=x, y=y)
    plt.savefig(filename)
    plt.show()


# Line Chart - Gráfico de Linhas
def line_chart(x, y, filename):
    sns.lineplot(x=x, y=y)
    plt.savefig(filename)
    plt.show()


# Bar Chart - Gráfico de Barras
def bar_chart(x, y, filename):
    sns.barplot(x=x, y=y)
    plt.savefig(filename)
    plt.show()


# Bubble Chart - Gráfico de Bolhas
def bubble_chart(x, y, size, filename):
    sns.scatterplot(x=x, y=y, size=size)
    plt.savefig(filename)
    plt.show()


# Dot Plot - Gráfico de Pontos
def dot_plot(x, y, filename):
    sns.stripplot(x=x, y=y)
    plt.savefig(filename)
    plt.show()
