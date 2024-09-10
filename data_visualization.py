import matplotlib.pyplot as plt
import base64
from io import BytesIO

def plot_histogram(data, title, xlabel, ylabel, filename):
    """
    Creates and saves a histogram plot.
    """
    plt.figure(figsize=(8, 6))
    plt.hist(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return embed_image(filename)

def plot_scatter(x_data, y_data, title, xlabel, ylabel, filename):
    """
    Creates and saves a scatter plot.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return embed_image(filename)

def plot_bar_chart(x_data, y_data, title, xlabel, ylabel, filename):
    """
    Creates and saves a bar chart.
    """
    plt.figure(figsize=(8, 6))
    plt.bar(x_data, y_data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels if needed
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return embed_image(filename)


def plot_box_plot(data, labels, title, ylabel, filename):
    """
    Creates and saves a box plot.
    """
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return embed_image(filename)

def embed_image(filename):
    """
    Embeds an image as a base64 string for HTML.
    """
    with open(filename, "rb") as f:
        image_data = f.read()
    base64_data = base64.b64encode(image_data).decode()
    return f"<img src='data:image/png;base64,{base64_data}'/>"