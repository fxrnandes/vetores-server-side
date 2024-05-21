import random
import seaborn as sns
import matplotlib.pyplot as plt
import os


def save_plot(plot_func, filename, **kwargs):
    plot_func(**kwargs)
    plt.savefig(filename)
    plt.close()


def create_all_charts(vetor_embaralhado, vetor_gerado):
    os.makedirs('static/images', exist_ok=True)

    scatter_path = 'static/images/scatter_plot.png'
    line_path = 'static/images/line_chart.png'
    bar_path = 'static/images/bar_chart.png'
    bubble_path = 'static/images/bubble_chart.png'
    dot_path = 'static/images/dot_plot.png'

    save_plot(sns.scatterplot, scatter_path, x=range(len(vetor_embaralhado)), y=vetor_embaralhado)
    save_plot(sns.lineplot, line_path, x=range(len(vetor_gerado)), y=vetor_gerado)
    save_plot(sns.barplot, bar_path, x=range(len(vetor_gerado)), y=vetor_gerado)
    save_plot(sns.scatterplot, bubble_path, x=range(len(vetor_embaralhado)), y=vetor_embaralhado,
              size=[random.randint(1, 100) for _ in range(len(vetor_embaralhado))])
    save_plot(sns.stripplot, dot_path, x=range(len(vetor_embaralhado)), y=vetor_embaralhado)

    return {
        "scatter": 'static/images/scatter_plot.png',
        "line": 'static/images/line_chart.png',
        "bar": 'static/images/bar_chart.png',
        "bubble": 'static/images/bubble_chart.png',
        "dot": 'static/images/dot_plot.png'
    }
