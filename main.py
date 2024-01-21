import extract_data
import topsis
import rsm
import UTA
import Sp_Cs
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# window size
global_window_width = 1500
global_window_height = 900

def try_conv(vector):
    try:
        [float(el) for el in vector]
        return True
    except ValueError:
        return False

def open_topsis_window(r, minimum, benefit_attributes_):

    def fun_method():
        ranking_area.delete('1.0', tk.END)  # Clear the ranking area
        lower_limits_ = []
        upper_limits_ = []
        weight_vector_ = []

        for i in range(len(criteria_entries)):
            if i % 3 == 0:
                lower_limits_.append(float(criteria_entries[i].get()))
            elif i % 3 - 1 == 0:
                upper_limits_.append(float(criteria_entries[i].get()))
            elif i % 3 - 2 == 0:
                weight_vector_.append(float(criteria_entries[i].get()))

        if try_conv(lower_limits_) and try_conv(upper_limits_) and try_conv(weight_vector_):
            lower_limits_ = list(map(float, lower_limits_))
            upper_limits_ = list(map(float, upper_limits_))
            weight_vector_ = list(map(float, weight_vector_))
            sum_weight_vector = sum(weight_vector_)
            weight_vector_normalized = [el / sum_weight_vector for el in weight_vector_]

            result_ = topsis.topsis(r[3], lower_limits_, upper_limits_, weight_vector_normalized,
                                    benefit_attributes_)
            text = ""
            for i in range(len(result_)):
                text += f"{i + 1}. {r[1][result_[i]][1]}, {r[1][result_[i]][2]}\n"

            ranking_area.insert(tk.END, text)
        else:
            messagebox.showwarning("Warning", "Wrong value entered!")

    new_window = tk.Toplevel(root)
    new_window.title("Topsis")
    new_window.attributes('-fullscreen', True)

    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        return "break"

    new_window.bind("<Escape>", end_fullscreen)
    
    # Ustaw rozmiar i pozycjonowanie okna
    window_width = global_window_width
    window_height = global_window_height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Criteria frame with canvas for scrolling
    criteria_frame = tk.LabelFrame(new_window, text="Kryteria brane pod uwagę", padx=5, pady=5)
    criteria_frame.grid(row=0, column=0, sticky="news", padx=10, pady=5)

    # Define the criteria here
    criteria_labels = r[2][1:]  # Add more criteria as needed
    criteria_entries = []

    # Add labels for Min, Max, Weight above the columns
    tk.Label(criteria_frame, text="Kryterium").grid(row=0, column=0, sticky="w", padx=5)
    for j, label in enumerate(["Min", "Max", "Weight[%]"]):
        tk.Label(criteria_frame, text=label).grid(row=0, column=j + 1, sticky="w", padx=5)

    # Dynamically create the criteria entries
    for i, label in enumerate(criteria_labels):
        tk.Label(criteria_frame, text=label).grid(row=i + 1, column=0, sticky="w", padx=5)
        for j in range(3):  # For Min, Max, Weight
            entry = tk.Entry(criteria_frame, width=8)
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=2)
            # Set default value
            if j % 3 == 0:
                entry.insert(tk.END, str(minimum[i]))
            elif j % 3 - 1 == 0:
                entry.insert(tk.END, str(maximum[i]))
            elif j % 3 - 2 == 0:
                entry.insert(tk.END, str(1 / len(minimum) * 100))
            criteria_entries.append(entry)

    # Ranking frame with scrolling text
    ranking_frame = tk.LabelFrame(new_window, text="Ranking", padx=5, pady=5)
    ranking_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
    ranking_area = tk.Text(ranking_frame, wrap=tk.WORD)
    ranking_area.grid(row=0, column=0, sticky="nsew")

    scrollbar_ranking = tk.Scrollbar(ranking_frame, orient="vertical", command=ranking_area.yview)
    ranking_area['yscrollcommand'] = scrollbar_ranking.set
    scrollbar_ranking.grid(row=0, column=1, sticky='nsew')

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=1, column=0, padx=5, pady=5)

    generate_button = tk.Button(button_frame, text="Generuj Ranking", command=fun_method)
    generate_button.grid(row=0, column=0, pady=5)

    return_button = tk.Button(button_frame, text="Powrót do okna głównego", command=new_window.destroy)
    return_button.grid(row=0, column=1, pady=5)

    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    ranking_frame.grid_columnconfigure(0, weight=1)
    ranking_frame.grid_rowconfigure(0, weight=1)

def open_RSM_window(r, minimum, benefit_attributes_):
    def fun_method():
        ranking_area.delete('1.0', tk.END)  # Clear the ranking area
        lower_limits_ = []
        upper_limits_ = []
        weight_vector_ = []

        for i in range(len(criteria_entries)):
            if i % 2 == 0:
                lower_limits_.append(float(criteria_entries[i].get()))
            elif i % 2 - 1 == 0:
                upper_limits_.append(float(criteria_entries[i].get()))

        if try_conv(lower_limits_) and try_conv(upper_limits_):
            lower_limits_ = list(map(float, lower_limits_))
            upper_limits_ = list(map(float, upper_limits_))
            weight_vector_ = list(map(float, weight_vector_))
            result_ = rsm.rsm(r[3], lower_limits_, upper_limits_, weight_vector_,benefit_attributes_)
            text = ""
            for i in range(len(result_)):
                text += f"{i + 1}. {r[1][result_[i]][1]}, {r[1][result_[i]][2]}\n"

            ranking_area.insert(tk.END, text)
        else:
            messagebox.showwarning("Warning", "Wrong value entered!")

    new_window = tk.Toplevel(root)
    new_window.title("RSM")
    new_window.attributes('-fullscreen', True)

    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        return "break"

    new_window.bind("<Escape>", end_fullscreen)

    # Ustaw rozmiar i pozycjonowanie okna
    window_width = global_window_width
    window_height = global_window_height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Criteria frame with canvas for scrolling
    criteria_frame = tk.LabelFrame(new_window, text="Kryteria brane pod uwagę", padx=5, pady=5)
    criteria_frame.grid(row=0, column=0, sticky="news", padx=10, pady=5)

    # Define the criteria here
    criteria_labels = r[2][1:]  # Add more criteria as needed
    criteria_entries = []

    # Add labels for Min, Max, Weight above the columns
    tk.Label(criteria_frame, text="Kryterium").grid(row=0, column=0, sticky="w", padx=5)
    for j, label in enumerate(["Min", "Max"]):
        tk.Label(criteria_frame, text=label).grid(row=0, column=j + 1, sticky="w", padx=5)

    # Dynamically create the criteria entries
    for i, label in enumerate(criteria_labels):
        tk.Label(criteria_frame, text=label).grid(row=i + 1, column=0, sticky="w", padx=5)
        for j in range(2):  # For Min, Max, Weight
            entry = tk.Entry(criteria_frame, width=8)
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=2)
            # Set default value
            if j % 2 == 0:
                entry.insert(tk.END, str(minimum[i]))
            elif j % 2 - 1 == 0:
                entry.insert(tk.END, str(maximum[i]))
            criteria_entries.append(entry)


    # Ranking frame with scrolling text
    ranking_frame = tk.LabelFrame(new_window, text="Ranking", padx=5, pady=5)
    ranking_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
    ranking_area = tk.Text(ranking_frame, wrap=tk.WORD)
    ranking_area.grid(row=0, column=0, sticky="nsew")

    scrollbar_ranking = tk.Scrollbar(ranking_frame, orient="vertical", command=ranking_area.yview)
    ranking_area['yscrollcommand'] = scrollbar_ranking.set
    scrollbar_ranking.grid(row=0, column=1, sticky='nsew')

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=1, column=0, padx=5, pady=5)

    generate_button = tk.Button(button_frame, text="Generuj Ranking", command=fun_method)
    generate_button.grid(row=0, column=0, pady=5)

    return_button = tk.Button(button_frame, text="Powrót do okna głównego", command=new_window.destroy)
    return_button.grid(row=0, column=1, pady=5)

    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    ranking_frame.grid_columnconfigure(0, weight=1)
    ranking_frame.grid_rowconfigure(0, weight=1)

def open_UTA_window(r, minimum, benefit_attributes_):

    def fun_method():
        ranking_area.delete('1.0', tk.END)  # Clear the ranking area
        lower_limits_ = []
        upper_limits_ = []
        weight_vector_ = []
        compartments_ = []

        for i in range(len(criteria_entries)):
            if i % 4 == 0:
                lower_limits_.append(float(criteria_entries[i].get()))
            elif i % 4 - 1 == 0:
                upper_limits_.append(float(criteria_entries[i].get()))
            elif i % 4 - 2 == 0:
                weight_vector_.append(float(criteria_entries[i].get()))
            elif i % 4 - 3 == 0:
                compartments_.append(float(criteria_entries[i].get()))

        if try_conv(lower_limits_) and try_conv(upper_limits_) and try_conv(weight_vector_) and try_conv(compartments_):
            lower_limits_ = list(map(float, lower_limits_))
            upper_limits_ = list(map(float, upper_limits_))
            weight_vector_ = list(map(float, weight_vector_))
            compartments_ = list(map(int, compartments_))
            sum_weight_vector = sum(weight_vector_)
            weight_vector_normalized = [el / sum_weight_vector for el in weight_vector_]

            result_ = UTA.UTA(r[3], lower_limits_, upper_limits_, weight_vector_normalized,
                                    benefit_attributes_, compartments_)
            text = ""
            for i in range(len(result_)):
                text += f"{i + 1}. {r[1][result_[i]][1]}, {r[1][result_[i]][2]}\n"

            ranking_area.insert(tk.END, text)
        else:
            messagebox.showwarning("Warning", "Wrong value entered!")

    new_window = tk.Toplevel(root)
    new_window.title("UTA")
    new_window.attributes('-fullscreen', True)

    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        return "break"

    new_window.bind("<Escape>", end_fullscreen)

    # Ustaw rozmiar i pozycjonowanie okna
    window_width = global_window_width
    window_height = global_window_height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Criteria frame without scrolling
    criteria_frame = tk.LabelFrame(new_window, text="Kryteria brane pod uwagę", padx=5, pady=5)
    criteria_frame.grid(row=0, column=0, sticky="news", padx=10, pady=5)

    # Define the criteria here
    criteria_labels = r[2][1:]  # Add more criteria as needed
    criteria_entries = []

    # Add labels for Min, Max, Weight above the columns
    tk.Label(criteria_frame, text="Kryterium").grid(row=0, column=0, sticky="w", padx=5)
    for j, label in enumerate(["Min", "Max", "Weight[%]", "Liczba przedziałów"]):
        tk.Label(criteria_frame, text=label).grid(row=0, column=j + 1, sticky="w", padx=5)

    # Dynamically create the criteria entries
    for i, label in enumerate(criteria_labels):
        tk.Label(criteria_frame, text=label).grid(row=i + 1, column=0, sticky="w", padx=5)
        for j in range(4):  # For Min, Max, Weight
            entry = tk.Entry(criteria_frame, width=8)
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=2)
            # Set default value
            if j % 4 == 0:
                entry.insert(tk.END, str(minimum[i]))
            elif j % 4 - 1 == 0:
                entry.insert(tk.END, str(maximum[i]))
            elif j % 4 - 2 == 0:
                entry.insert(tk.END, str(1 / len(minimum) * 100))
            elif j % 4 - 3 == 0:
                entry.insert(tk.END, str(1))
            criteria_entries.append(entry)
    # Ranking frame with scrolling text
    ranking_frame = tk.LabelFrame(new_window, text="Ranking", padx=5, pady=5)
    ranking_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=5)
    ranking_area = tk.Text(ranking_frame, wrap=tk.WORD)
    ranking_area.grid(row=0, column=0, sticky="nsew")

    scrollbar_ranking = tk.Scrollbar(ranking_frame, orient="vertical", command=ranking_area.yview)
    ranking_area['yscrollcommand'] = scrollbar_ranking.set
    scrollbar_ranking.grid(row=0, column=1, sticky='nsew')

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=1, column=0, padx=5, pady=5)

    generate_button = tk.Button(button_frame, text="Generuj Ranking", command=fun_method)
    generate_button.grid(row=0, column=0, pady=5)

    return_button = tk.Button(button_frame, text="Powrót do okna głównego", command=new_window.destroy)
    return_button.grid(row=0, column=1, pady=5)

    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_rowconfigure(0, weight=1)

    ranking_frame.grid_columnconfigure(0, weight=1)
    ranking_frame.grid_rowconfigure(0, weight=1)
    


def open_SPCS_window():
    def update_comboboxes(*args):
        selected = set(cb.get() for cb in comboboxes)
        for cb in comboboxes:
            current = cb.get()
            cb['values'] = [c for c in criteria_labels if c not in selected or c == current]

    def fun_method():
        ranking_area.delete('1.0', tk.END)
        lower_limits_ = []
        upper_limits_ = []

        for i, cb in enumerate(comboboxes):
            selected_category = cb.get()
            if selected_category in criteria_labels:
                index = criteria_labels.index(selected_category)
                lower_limit = float(min_entries[i].get())
                upper_limit = float(max_entries[i].get())
                lower_limits_.append(lower_limit)
                upper_limits_.append(upper_limit)

        if try_conv(lower_limits_) and try_conv(upper_limits_):
            # Zakładam, że weight_vector_ i benefit_attributes_ są odpowiednio zdefiniowane
            result_ = Sp_Cs.spcs(r[3], lower_limits_, upper_limits_, benefit_attributes_)
            text = ""
            for i in range(len(result_)):
                text += f"{i + 1}. {r[1][result_[i]][1]}, {r[1][result_[i]][2]}\n"
            ranking_area.insert(tk.END, text)
        else:
            messagebox.showwarning("Warning", "Wrong value entered!")

    new_window = tk.Toplevel(root)
    new_window.title("SP_CS")
    new_window.attributes('-fullscreen', True)
    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        return "break"

    new_window.bind("<Escape>", end_fullscreen)

    window_width = global_window_width
    window_height = global_window_height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)
    new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    criteria_frame = tk.LabelFrame(new_window, text="Kryteria brane pod uwagę", padx=5, pady=5)
    criteria_frame.grid(row=0, column=0, sticky="news", padx=10, pady=5)

    criteria_labels = r[2][1:]  # Zmienne kryteriów
    comboboxes = []
    criteria_labels = r[2][1:]
    comboboxes = []
    min_entries = []
    max_entries = []

    for i in range(3):
        cb = ttk.Combobox(criteria_frame, values=criteria_labels)
        cb.grid(row=i, column=1, padx=5, pady=2)
        cb.bind('<<ComboboxSelected>>', update_comboboxes)
        comboboxes.append(cb)

        min_entry = tk.Entry(criteria_frame, width=10)
        min_entry.grid(row=i, column=2, padx=5, pady=2)
        min_entries.append(min_entry)

        max_entry = tk.Entry(criteria_frame, width=10)
        max_entry.grid(row=i, column=3, padx=5, pady=2)
        max_entries.append(max_entry)

    ranking_frame = tk.LabelFrame(new_window, text="Ranking", padx=5, pady=5)
    ranking_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
    ranking_area = tk.Text(ranking_frame, wrap=tk.WORD)
    ranking_area.grid(row=0, column=0, sticky="nsew")

    scrollbar_ranking = tk.Scrollbar(ranking_frame, command=ranking_area.yview)
    ranking_area['yscrollcommand'] = scrollbar_ranking.set
    scrollbar_ranking.grid(row=0, column=1, sticky='nsew')

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=1, column=0, padx=5, pady=5)

    generate_button = tk.Button(button_frame, text="Generuj Ranking", command=fun_method)
    generate_button.grid(row=0, column=0, pady=5)

    return_button = tk.Button(button_frame, text="Powrót do okna głównego", command=new_window.destroy)
    return_button.grid(row=0, column=1, pady=5)

    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    ranking_frame.grid_columnconfigure(0, weight=1)
    ranking_frame.grid_rowconfigure(0, weight=1)

    update_comboboxes()  # Aktualizuj comboboxy przy inicjalizacji
    

if __name__ == "__main__":
    r = extract_data.get_data_from_database()

    benefit_attributes_ = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    transposed_list = list(zip(*r[3]))[1:]
    minimum = [min(column) for column in transposed_list]
    maximum = [max(column) for column in transposed_list]


    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Systemy Wspomagania Decyzji")
    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        return "break"

    root.bind("<Escape>", end_fullscreen)

    # Ustaw rozmiar i położenie okna
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 1500
    height = 900
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Załaduj obraz tła
    width_background_image = 900
    height_background_image = 500
    background_image = Image.open("start_page_photo.png")
    background_image = background_image.resize((width_background_image, height_background_image), Image.ANTIALIAS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    # Dodaj etykietę "Wybierz metodę"
    tk.Label(root, text="Gdzie świat poniesie cię dziś?", font=("Helvetica", 40)).pack()

    methods = {"Topsis": lambda: open_topsis_window(r, minimum, benefit_attributes_),
               "RSM": lambda: open_RSM_window(r, minimum, benefit_attributes_),
               "UTA": lambda: open_UTA_window(r, minimum, benefit_attributes_),
               "SP_CS": open_SPCS_window}
    
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=20)

    for method, action in methods.items():
        button = tk.Button(button_frame, text=method, command=action, height=2, width=20, bg='black', fg='white', font=("Helvetica",12,'bold'))
        button.pack(side=tk.LEFT, padx=10)


    label_reminder = tk.Label(root, text="Poniżej wybierz odpowiednią metodę:", font=("Helvetica", 12))
    label_reminder.pack(side=tk.BOTTOM, pady=0)

    # Dodatkowa etykieta "Pamiętaj, aby dobrze wybrać"
    label_reminder = tk.Label(root, text="Pamiętaj, aby dobrze wybrać", font=("Helvetica", 12))
    label_reminder.pack(side=tk.BOTTOM, pady=0)

    

    #for method, action in methods.items():
    #    tk.Button(root, text=method, command=action).pack()

    root.mainloop()