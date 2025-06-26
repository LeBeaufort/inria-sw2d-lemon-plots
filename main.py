import matplotlib.cm
import matplotlib.pyplot as plt
from glob import glob
import argparse

import file_parser
import animation_helper

parser = argparse.ArgumentParser()
parser.add_argument("task", choices=["probe", "map", "animation"], help="What the program is going to do")
parser.add_argument("path", help="the path of the file used to generate plot or regex that match file used to generate animation")
parser.add_argument("--data", help="What data is the program going to use. Not necessary if listing probes")
parser.add_argument("--save-path", help="the path where plot are saved")
parser.add_argument("--list-probes", help="list probes from a file",  action=argparse.BooleanOptionalAction)
parser.add_argument("--probe-name", help="Name of the probe, leave empty for all probes")

args = parser.parse_args()

if args.task == "probe":
    probes, data = file_parser.probe_parser(args.path)
    valid_d = ["zb", "h", "q", "r"]

    if args.list_probes:
        print(f"There is {len(probes)} probes: {probes}")

    if not args.data: exit()
    if not args.data in valid_d:
        exit(f"Invalid data for this option, valid data are {valid_d}")

    if args.probe_name:
        if not args.probe_name in probes: exit("Probe does not exist !")
        plt.plot(data["time"], data[f"{args.probe}_{args.data}"])
        plt.show()
    else:
        for probe in probes:
            plt.plot(data["time"], data[f"{probe}_{args.data}"])

        plt.savefig(args.save_path) if args.save_path else plt.show()

elif args.task == "map":
    if not args.data: exit("No data specified")

    mesh_data = file_parser.ResultHydro_parser(args.path)
    fig, ax = plt.subplots()

    if args.data == "water_depth" or args.data == "zb":
        plt.scatter(mesh_data["x"], mesh_data["y"], c=mesh_data[args.data], cmap="Blues")
        fig.colorbar(matplotlib.cm.ScalarMappable(cmap="Blues", norm=matplotlib.colors.Normalize(vmin=min(mesh_data[args.data]), vmax=max(mesh_data[args.data]))), ax=ax)
        plt.savefig(args.save_path) if args.save_path else plt.show() # save to disk if --save-path has been passed, else show the plot
    elif args.data == "unit_discharge":
        plt.quiver(mesh_data["x"], mesh_data["y"], mesh_data["unit_discharge_x"], mesh_data["unit_discharge_y"], mesh_data["unit_discharge_norm"], cmap="viridis")
        fig.colorbar(matplotlib.cm.ScalarMappable(cmap="viridis", norm=matplotlib.colors.Normalize(vmin=min(mesh_data["unit_discharge_norm"]), vmax=max(mesh_data["unit_discharge_norm"]))), ax=ax)
        plt.savefig(args.save_path) if args.save_path else plt.show()
    else:
        exit("Invalid data ! Valid data are `water_depth` `zb` and `unit_discharge`")

elif args.task == "animation":
    if not args.data: exit("No data specified")
    animation_files = glob(args.path)
    if args.data == "water_depth" or args.data == "zb":
        animation_helper.draw_scatter_animation(args.data, filenames=animation_files)
    elif args.data == "unit_discharge":
        animation_helper.draw_quiver_animation(animation_files)
    else:
        exit("Invalid data ! Valid data are `water_depth` `zb` and `unit_discharge`")






