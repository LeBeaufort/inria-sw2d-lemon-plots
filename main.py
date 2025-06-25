import matplotlib.cm
import matplotlib.pyplot as plt
import parser

def print_question(question, choice_list, default="1", input_text="Your choice [{}] : "):
    """This function print a list of answer and prompt the user to select one"""
    print(question)
    for number, answer in enumerate(choice_list):
        print(f"[{number + 1}] {answer}")

    i = input(input_text.format(default)).replace(" ", "")
    if i:
        return i
    else:
        return default


def ask_user(question, choice_list, default="1", input_text="Your choice [{}] : "):
    while True:
        a = print_question(question, choice_list, default, input_text)
        try:
            a = int(a)
            if a <= len(choice_list):
                return choice_list[a - 1]
            else:
                print("Please pick something valid")
        except:
            print("Please pick something valid")



a = print_question("What do you want to do ?", ["Use a ProbeTimeSeries file", "Use a ResultHydro file"])
if a == "1":
    probes, data = parser.probe_parser("input_files/ProbesTimeSeries.txt")
    selected_data = ask_user("What data do you want to view ?", ["zb", "h", "q", "r"])
    probe_n = print_question("What do you want to do ?", ["All probes", "One probe only"])
    if probe_n == "1":
        for probe in probes:
            plt.plot(data["time"], data[f"{probe}_{selected_data}"])
        plt.show()
    else:
        selected_probe = ask_user("What probe do you want to view ?", probes)
        plt.plot(data["time"], data[f"{selected_probe}_{selected_data}"])
        plt.show()

elif a == "2":
    file_name = "input_files/ResultHydro_p0000d09h00m00s000.txt"
    mesh_data = parser.ResultHydro_parser(file_name)

    plot_type = print_question("What type of plot do you want ?", ["Water_depth", "unit_discharge", "zb"])
    if plot_type == "1":
        fig, ax = plt.subplots()
        plt.scatter(mesh_data["x"], mesh_data["y"], c=mesh_data["water_depth"], cmap="Blues")
        fig.colorbar(matplotlib.cm.ScalarMappable(cmap="Blues", norm=matplotlib.colors.Normalize(vmin=min(mesh_data["water_depth"]), vmax=max(mesh_data["water_depth"]))), ax=ax)
        plt.show()
    elif plot_type == "2":
        fig, ax = plt.subplots()
        plt.quiver(mesh_data["x"], mesh_data["y"], mesh_data["unit_discharge_x"], mesh_data["unit_discharge_y"], mesh_data["unit_discharge_norm"], cmap="viridis")
        fig.colorbar(matplotlib.cm.ScalarMappable(cmap="viridis", norm=matplotlib.colors.Normalize(vmin=min(mesh_data["unit_discharge_norm"]), vmax=max(mesh_data["unit_discharge_norm"]))), ax=ax)
        plt.show()
    elif plot_type == "3":
        fig, ax = plt.subplots()
        plt.scatter(mesh_data["x"], mesh_data["y"], c=mesh_data["zb"], cmap="Blues")
        fig.colorbar(matplotlib.cm.ScalarMappable(cmap="Blues",
                                                  norm=matplotlib.colors.Normalize(vmin=min(mesh_data["zb"]),
                                                                                   vmax=max(mesh_data["zb"]))),
                     ax=ax)
        plt.show()
    else:
        print("Please type a valid choice")
else:
    print("Invalid choice")
    exit()






