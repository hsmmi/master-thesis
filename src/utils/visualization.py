from matplotlib import pyplot as plt
import numpy as np
from config import FIGURE_PATH


def plot_algorithm_results(
    X,
    y,
    X_,
    y_,
    title="Algorithm Results",
    save_plot=False,
    show_plot=True,
):
    """
    Plot the results of the specified algorithm.

    Parameters:
    X (numpy.ndarray): Feature matrix of the training data.
    y (numpy.ndarray): Labels of the training data.
    X_ (numpy.ndarray): Reduced feature matrix.
    y_ (numpy.ndarray): Reduced labels.
    title (str): Title of the plot.
    save_plot (bool): Whether to save the plot as a file.
    show_plot (bool): Whether to display the plot.
    """
    # Adjust marker size and line width
    point_size = 30  # Increased marker size for better visibility
    linewidth = 0.5  # Reduced line width for better visibility
    alpha = 0.8  # Set transparency level for markers

    # Define marker properties for each class
    marker_properties = {
        0: {
            "marker": "x",
            "s": point_size,
            # Steel Blue
            "facecolors": "#4682B4",
            "linewidths": linewidth,
        },
        1: {
            "marker": "o",
            "s": point_size,
            "facecolors": "none",
            "edgecolors": "black",
            "linewidths": linewidth,
        },
    }

    # Set up the figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))  # Slightly larger figure for clarity

    # Plot the original dataset
    for label in np.unique(y):
        props = marker_properties[label]
        axs[0].scatter(
            X[y == label][:, 0],
            X[y == label][:, 1],
            label=f"Class {label}",
            marker=props["marker"],
            alpha=alpha,
            s=props["s"],
            facecolors=props["facecolors"],
            # Apply edgecolors only if specified (for hollow markers)
            **({"edgecolors": props["edgecolors"]} if "edgecolors" in props else {}),
            linewidths=props["linewidths"],
        )
    axs[0].set_title("Original Dataset")
    axs[0].legend()

    # Plot the reduced dataset
    for label in np.unique(y_):
        props = marker_properties[label]
        axs[1].scatter(
            X_[y_ == label][:, 0],
            X_[y_ == label][:, 1],
            label=f"Class {label}",
            marker=props["marker"],
            alpha=alpha,
            s=props["s"],
            facecolors=props["facecolors"],
            # Apply edgecolors only if specified (for hollow markers)
            **({"edgecolors": props["edgecolors"]} if "edgecolors" in props else {}),
            linewidths=props["linewidths"],
        )
    # Ensure the same scale for both subplots
    axs[1].set_xlim(axs[0].get_xlim())
    axs[1].set_ylim(axs[0].get_ylim())
    axs[1].set_title("Reduced Dataset")
    axs[1].legend()

    # Set the overall title
    plt.suptitle(title)

    # Save the plot if required
    if save_plot:
        plt.savefig(FIGURE_PATH + title + ".png")

    # Show the plot if required
    if show_plot:
        plt.show()

    # Close the plot to free memory
    plt.close()
