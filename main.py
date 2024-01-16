import extract_data
import topsis
import rsm
import tkinter as tk
from tkinter import ttk, messagebox


def try_conv(vector):
    try:
        [float(el) for el in vector]
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    r = extract_data.get_data_from_database()

    benefit_attributes_ = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def fun_method():
        ranking_area.delete('1.0', tk.END)  # Clear the ranking area
        lower_limits_ = []
        upper_limits_ = []
        weight_vector_ = []

        for i in range(len(criteria_entries)):
            if i % 3 == 0:
                lower_limits_.append(root.nametowidget(criteria_entries[i]).get())
            elif i % 3 - 1 == 0:
                upper_limits_.append(root.nametowidget(criteria_entries[i]).get())
            elif i % 3 - 2 == 0:
                weight_vector_.append(root.nametowidget(criteria_entries[i]).get())

        if try_conv(lower_limits_) and try_conv(upper_limits_) and try_conv(weight_vector_):
            lower_limits_ = list(map(float, lower_limits_))
            upper_limits_ = list(map(float, upper_limits_))
            weight_vector_ = list(map(float, weight_vector_))
            sum_weight_vector = sum(weight_vector_)
            weight_vector_normalized = [el / sum_weight_vector for el in weight_vector_]

            selected_method = method_var.get()
            result_ = []
            if selected_method == 'Topsis':
                result_ = topsis.topsis(r[3], lower_limits_, upper_limits_, weight_vector_normalized, benefit_attributes_)
            elif selected_method == 'RSM':
                result_ = rsm.rsm(r[3], lower_limits_, upper_limits_, weight_vector_normalized)

            text = ""
            for i in range(len(result_)):
                text += f"{i + 1}. {r[1][result_[i]][1]}, {r[1][result_[i]][2]}\n"

            # Insert some placeholder text for demonstration purposes
            ranking_area.insert(tk.END, text)

        else:
            messagebox.showwarning("Warning", "Wrong value entered !")


    # Main window
    root = tk.Tk()
    root.title("Ranking UI")

    # Criteria frame with canvas for scrolling
    criteria_frame = tk.LabelFrame(root, text="Kryteria brane pod uwagę", padx=5, pady=5)
    criteria_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    canvas = tk.Canvas(criteria_frame)
    scrollbar = tk.Scrollbar(criteria_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Define the criteria here
    criteria_labels = r[2][1:]  # Add more criteria as needed
    criteria_entries = []

    # Add labels for Min, Max, Weight above the columns
    tk.Label(scrollable_frame, text="Kryterium").grid(row=0, column=0, sticky="w", padx=5)
    for j, label in enumerate(["Min", "Max", "Weight[%]"]):
        tk.Label(scrollable_frame, text=label).grid(row=0, column=j + 1, sticky="w", padx=5)

    transposed_list = list(zip(*r[3]))[1:]
    minimum = [min(column) for column in transposed_list]
    maximum = [max(column) for column in transposed_list]

    # Dynamically create the criteria entries
    for i, label in enumerate(criteria_labels):
        tk.Label(scrollable_frame, text=label).grid(row=i + 1, column=0, sticky="w", padx=5)
        for j in range(3):  # For Min, Max, Weight
            entry = tk.Entry(scrollable_frame, width=8)
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=2)
            # Set default value
            if j % 3 == 0:
                entry.insert(tk.END, str(minimum[i]))
            elif j % 3 - 1 == 0:
                entry.insert(tk.END, str(maximum[i]))
            elif j % 3 - 2 == 0:
                entry.insert(tk.END, str(1/len(minimum)*100))
            criteria_entries.append(entry)

    # Bind the scrollable frame to the canvas
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))


    scrollable_frame.bind("<Configure>", on_frame_configure)

    scrollbar.pack(side=tk.RIGHT, fill='y')
    canvas.pack(side=tk.LEFT, fill="both", expand=True)

    # Method selection frame
    method_frame = tk.LabelFrame(root, text="Wybór metody", padx=5, pady=5)
    method_frame.grid(row=1, column=0, sticky="ew", padx=10)

    # Example options for method selection
    methods = ["Topsis", "RSM"]
    method_var = tk.StringVar(value=methods[0])
    method_dropdown = ttk.Combobox(method_frame, textvariable=method_var, values=methods, state="readonly")
    method_dropdown.grid(row=0, column=0, padx=5, pady=5)

    # Ranking frame with scrolling text
    ranking_frame = tk.LabelFrame(root, text="Ranking", padx=5, pady=5)
    ranking_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
    ranking_area = tk.Text(ranking_frame, wrap=tk.WORD)
    ranking_area.grid(row=0, column=0, sticky="nsew")

    scrollbar_ranking = tk.Scrollbar(ranking_frame, orient="vertical", command=ranking_area.yview)
    ranking_area['yscrollcommand'] = scrollbar_ranking.set
    scrollbar_ranking.grid(row=0, column=1, sticky='nsew')

    generate_button = tk.Button(root, text="Generuj Ranking", command=fun_method)
    generate_button.grid(row=2, column=0, pady=5)

    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    ranking_frame.grid_columnconfigure(0, weight=1)
    ranking_frame.grid_rowconfigure(0, weight=1)

    root.mainloop()