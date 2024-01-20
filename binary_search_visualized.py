import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pysine import sine
import sys
from matplotlib import animation
from IPython.display import HTML


def update(frame_data):
    data, colors, mid, searched = frame_data
    plt.cla() 

    bar_positions = np.arange(len(data))
    axes = sns.barplot(x=bar_positions, y=data, palette=colors)  
    axes.set(xlabel=f'Mid: {mid}; searches: {searched}', xticklabels=data)


def play_sound(i, seconds=0.1):
    sine(frequency=i, duration=seconds)


def play_found_sound(seconds=0.1):
    sine(frequency=523.25, duration=seconds)  # C5
    sine(frequency=698.46, duration=seconds)  # F5
    sine(frequency=783.99, duration=seconds)  # G5


def play_not_found_sound(seconds=0.3):
    sine(frequency=220, duration=seconds)  # A3


def binary_search_visualization(data, target):
    searched = 0
    colors = ['lightgray'] * len(data)
    yield (data, colors, -1, searched)

    low, high = 0, len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        searched += 1
        colors[mid] = 'purple'
        yield (data, colors, mid, searched)
        play_sound(data[mid], seconds=0.1)  

        if data[mid] == target:
            colors[mid] = 'green'
            yield (data, colors, mid, searched)
            play_found_sound()
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

        colors[mid] = 'lightgray'
        yield (data, colors, -1, searched)

    yield (data, colors, -1, searched)
    play_not_found_sound()


def main():
    number_of_values = int(sys.argv[1] if len(sys.argv) == 2 else 25)

    figure = plt.figure('Binary Search')
    numbers = np.arange(1, number_of_values + 1)
    numbers.sort()
    target_value = int(sys.argv[2]) if len(sys.argv) == 3 else np.random.randint(1, number_of_values + 1)

    anim = animation.FuncAnimation(
        figure, update, repeat=False, frames=binary_search_visualization(numbers, target_value), interval=500
    )
    plt.show()
    HTML(anim.to_jshtml())
    anim.save('binarysearch.gif', writer='pillow')

if __name__ == '__main__':
    main()