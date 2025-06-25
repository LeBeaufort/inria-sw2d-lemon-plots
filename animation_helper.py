import parser
from matplotlib import pyplot as plt
import matplotlib
from matplotlib import animation

def draw_scatter_animation(data:str, filenames: list[str]):
    animation_data = [parser.ResultHydro_parser(c) for c in filenames]

    min_value, max_value = 0, 0
    for each in animation_data:
        if min(each[data]) < min_value:
            min_value = min(each[data])
        if max(each[data]) > max_value:
            max_value = max(each[data])

    fig, ax = plt.subplots()
    ax.scatter(animation_data[0]["x"], animation_data[0]["y"], c=animation_data[0][data], cmap="Blues")
    fig.colorbar(matplotlib.cm.ScalarMappable(cmap="Blues",
                                              norm=matplotlib.colors.Normalize(vmin=min_value, vmax=max_value)),
                ax=ax)

    def update(frame):
        scat = ax.scatter(animation_data[frame]["x"], animation_data[frame]["y"], c=animation_data[frame][data],cmap="Blues")
        return scat

    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(filenames), interval=300)
    plt.show()

def draw_quiver_animation(filenames: list[str]):
    animation_data = [parser.ResultHydro_parser(c) for c in filenames]

    min_value, max_value = 0, 0
    for each in animation_data:
        if min(each["unit_discharge_norm"]) < min_value:
            min_value = min(each["unit_discharge_norm"])
        if max(each["unit_discharge_norm"]) > max_value:
            max_value = max(each["unit_discharge_norm"])

    fig, ax = plt.subplots()
    qv = ax.quiver(animation_data[0]["x"], animation_data[0]["y"], animation_data[0]["unit_discharge_x"], animation_data[0]["unit_discharge_y"], animation_data[0]["unit_discharge_norm"], cmap="viridis")
    fig.colorbar(matplotlib.cm.ScalarMappable(cmap="viridis",
                                              norm=matplotlib.colors.Normalize(vmin=min_value, vmax=max_value)),
                 ax=ax)

    def update(frame):
        qv.set_UVC(
            animation_data[frame]["unit_discharge_x"],
            animation_data[frame]["unit_discharge_y"],
            animation_data[frame]["unit_discharge_norm"]
        )
        return qv

    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(filenames), interval=300)
    plt.show()