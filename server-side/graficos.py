import random
import seaborn as sns
import matplotlib.pyplot as plt
import os


def save_plot(plot_func, filename, **kwargs):
    plot_func(**kwargs)
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo em: {filename}")  # Log para verificar onde o gráfico está sendo salvo


def create_all_charts(vetor_embaralhado, vetor_gerado):
    os.makedirs('static/images', exist_ok=True)

    scatter_path = 'images/scatter_plot.png'
    line_path = 'images/line_chart.png'
    bar_path = 'images/bar_chart.png'
    bubble_path = 'images/bubble_chart.png'
    dot_path = 'images/dot_plot.png'

    print("Criando gráficos...")  # Log para iniciar a criação de gráficos

    save_plot(sns.scatterplot, f'static/{scatter_path}', x=range(len(vetor_embaralhado)), y=vetor_embaralhado)
    save_plot(sns.lineplot, f'static/{line_path}', x=range(len(vetor_gerado)), y=vetor_gerado)
    save_plot(sns.barplot, f'static/{bar_path}', x=range(len(vetor_gerado)), y=vetor_gerado)
    save_plot(sns.scatterplot, f'static/{bubble_path}', x=range(len(vetor_embaralhado)), y=vetor_embaralhado,
              size=[random.randint(1, 100) for _ in range(len(vetor_embaralhado))])
    save_plot(sns.stripplot, f'static/{dot_path}', x=range(len(vetor_embaralhado)), y=vetor_embaralhado)

    print("Gráficos criados.")  # Log para finalizar a criação de gráficos

    return {
        "scatter": scatter_path,
        "line": line_path,
        "bar": bar_path,
        "bubble": bubble_path,
        "dot": dot_path
    }
