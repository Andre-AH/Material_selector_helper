import csv
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import matplotlib.pyplot as plt
import numpy as np


# Load material data from a CSV file with units in headers
def load_material_data(filename):
    materials = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                materials.append({
                    "name": row["name"],
                    "density_(kg/m^3)": float(row["density_(kg/m^3)"]),
                    "UTS_(MPa)": float(row["UTS_(MPa)"]),
                    "cost_per_kg_($)": float(row["cost_per_kg_($)"]),
                    "thermal_conductivity_(W/mK)": float(row["thermal_conductivity_(W/mK)"]),
                    "maximum_temperature_(C)": float(row["maximum_temperature_(C)"]),
                    "young_modulus_(GPa)": float(row["young_modulus_(GPa)"]),
                    "thermal_capacity_(J/kgK)": float(row["thermal_capacity_(J/kgK)"]),
                    "tensile_strength_yield_(MPa)": float(row["tensile_strength_yield_(MPa)"]),
                    "Elongation_(%)": float(row["Elongation_(%)"]),
                    "recycle_fraction_(%)": float(row["recycle_fraction_(%)"]),
                    "type": row["type"]
                })
    except FileNotFoundError:
        messagebox.showerror("File Error", f"Could not find file: {filename}")
    except ValueError:
        messagebox.showerror("Data Error", "Data format in file is incorrect.")
    return materials

# Save updated materials data to the CSV file
def save_material_data(filename, materials):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "density_(kg/m^3)", "UTS_(MPa)", "cost_per_kg_($)", "thermal_conductivity_(W/mK)", "maximum_temperature_(C)", "young_modulus_(GPa)", "thermal_capacity_(J/kgK)", "tensile_strength_yield_(MPa)", "Elongation_(%)", "recycle_fraction_(%)", "type"])
            writer.writeheader()
            for material in materials:
                writer.writerow(material)
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving: {e}")

# Filter materials based on user-defined intervals and selected types
def filter_materials(materials, density_range, strength_range, cost_range, conductivity_range, maximum_temperature_range, young_modulus_range, thermal_capacity_range, tensile_strength_range, ductility_range, recycle_fraction_range, selected_types):
    return [
        material for material in materials
        if (density_range[0] <= material["density_(kg/m^3)"] <= density_range[1] and
            strength_range[0] <= material["UTS_(MPa)"] <= strength_range[1] and
            cost_range[0] <= material["cost_per_kg_($)"] <= cost_range[1] and
            conductivity_range[0] <= material["thermal_conductivity_(W/mK)"] <= conductivity_range[1] and
            maximum_temperature_range[0] <= material["maximum_temperature_(C)"] <= maximum_temperature_range[1] and
            young_modulus_range[0] <= material["young_modulus_(GPa)"] <= young_modulus_range[1] and
            thermal_capacity_range[0] <= material["thermal_capacity_(J/kgK)"] <= thermal_capacity_range[1] and
            tensile_strength_range[0] <= material["tensile_strength_yield_(MPa)"] <= tensile_strength_range[1] and
            ductility_range[0] <= material["Elongation_(%)"] <= ductility_range[1] and
            recycle_fraction_range[0] <= material["recycle_fraction_(%)"] <= recycle_fraction_range[1] and
            (material["type"] in selected_types))
    ]

# Update results based on current slider values and sorting preference
def update_results():
    density_range = (density_min_scale.get(), density_max_scale.get())
    strength_range = (strength_min_scale.get(), strength_max_scale.get())
    cost_range = (cost_min_scale.get(), cost_max_scale.get())
    conductivity_range = (conductivity_min_scale.get(), conductivity_max_scale.get())
    maximum_temperature_range = (maximum_temperature_min_scale.get(), maximum_temperature_max_scale.get())
    young_modulus_range = (young_modulus_min_scale.get(), young_modulus_max_scale.get())
    thermal_capacity_range = (thermal_capacity_min_scale.get(), thermal_capacity_max_scale.get())
    tensile_strength_range = (tensile_strength_min_scale.get(), tensile_strength_max_scale.get())
    ductility_range = (ductility_min_scale.get(), ductility_max_scale.get())
    recycle_fraction_range = (recycle_fraction_min_scale.get(), recycle_fraction_max_scale.get())

    selected_types = [material_type for material_type, var in material_vars.items() if var.get()]

    global suitable_materials
    suitable_materials = filter_materials(materials, density_range, strength_range, cost_range, conductivity_range, maximum_temperature_range, young_modulus_range, thermal_capacity_range, tensile_strength_range, ductility_range, recycle_fraction_range, selected_types)

    # Sort results based on selected property and order
    sort_property = sort_combobox.get()
    if sort_property:
        suitable_materials.sort(key=lambda x: x[sort_property], reverse=not sort_order)  # Reverse if descending

    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.END, f"Number of suitable materials found: {len(suitable_materials)}\n\n")
    if suitable_materials:
        for material in suitable_materials:
            result_text.insert(tk.END, (f"Name: {material['name']}, Density: {material['density_(kg/m^3)']} kg/m³\n"
                                        f"UTS: {material['UTS_(MPa)']} MPa, Cost: ${material['cost_per_kg_($)']} per kg\n"
                                        f"Thermal Conductivity: {material['thermal_conductivity_(W/mK)']} W/mK\n"
                                        f"Maximum Temperature: {material['maximum_temperature_(C)']} C\n"
                                        f"Young's Modulus: {material['young_modulus_(GPa)']} GPa\n"
                                        f"Thermal Capacity: {material['thermal_capacity_(J/kgK)']} J/kgK\n"
                                        f"Yield Tensile Strength: {material['tensile_strength_yield_(MPa)']} MPa\n"
                                        f"Elongation: {material['Elongation_(%)']} %\n"  # Corrected line
                                        f"Recycle Fraction: {material['recycle_fraction_(%)']} %\n"  # Corrected line
                                        f"{'-' * 60}\n"))  # Line separator
    else:
        result_text.insert(tk.END, "No materials meet your criteria.")


# Create a slider with a dual range (min and max)
def create_range_slider(frame, row, label_text, from_, to_, default_min, default_max):
    label = ttk.Label(frame, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5)

    min_scale = tk.Scale(frame, from_=from_, to=to_, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="white")
    min_scale.set(default_min)
    min_scale.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)

    max_scale = tk.Scale(frame, from_=from_, to=to_, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="white")
    max_scale.set(default_max)
    max_scale.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)

    # Link scales to ensure max_scale value is always greater than or equal to min_scale value
    def update_max(val):
        if min_scale.get() > max_scale.get():
            max_scale.set(min_scale.get())
        update_results()  # Update results on slider move

    def update_min(val):
        if max_scale.get() < min_scale.get():
            min_scale.set(max_scale.get())
        update_results()  # Update results on slider move

    min_scale.config(command=update_max)
    max_scale.config(command=update_min)

    return min_scale, max_scale

# Export results to a CSV file
def export_to_csv():
    if not suitable_materials:
        messagebox.showwarning("Export Warning", "No materials to export.")
        return

    # Ask user for a filename to save the results
    filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                              filetypes=[("CSV files", "*.csv"),
                                                         ("All files", "*.*")])
    if filename:
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["name", "density_(kg/m^3)", "UTS_(MPa)", "cost_per_kg_($)", "thermal_conductivity_(W/mK)", "maximum_temperature_(C)", "young_modulus_(GPa)", "thermal_capacity_(J/kgK)", "tensile_strength_yield_(MPa)", "Elongation_(%)", "recycle_fraction_(%)", "type"])
                writer.writeheader()
                for material in suitable_materials:
                    writer.writerow(material)
            messagebox.showinfo("Export Successful", f"Results exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting: {e}")

# Function to plot the graph based on selected properties
def plot_graph():
    global x_property_combobox, y_property_combobox
    x_property = x_property_combobox.get()
    y_property = y_property_combobox.get()

    if x_property == "Select X Property" or y_property == "Select Y Property":
        messagebox.showwarning("Selection Error", "Please select both properties to plot.")
        return

    if not suitable_materials:
        messagebox.showwarning("Data Error", "No materials available to plot.")
        return

    x_values = [material[x_property] for material in suitable_materials]
    y_values = [material[y_property] for material in suitable_materials]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, color='blue')

    plt.title(f"{y_property} vs {x_property}")
    plt.xlabel(x_property.capitalize())
    plt.ylabel(y_property.capitalize())
    plt.grid(True)

    for i, material in enumerate(suitable_materials):
        plt.annotate(material['name'], (x_values[i], y_values[i]), fontsize=8, alpha=0.7)

    plt.show()


    # Create the GUI
def create_gui():
    global density_min_scale, density_max_scale, strength_min_scale, strength_max_scale
    global cost_min_scale, cost_max_scale, conductivity_min_scale, conductivity_max_scale
    global maximum_temperature_min_scale, maximum_temperature_max_scale, young_modulus_min_scale, young_modulus_max_scale, thermal_capacity_min_scale, thermal_capacity_max_scale
    global tensile_strength_min_scale, tensile_strength_max_scale, ductility_min_scale, ductility_max_scale, recycle_fraction_min_scale, recycle_fraction_max_scale
    global result_text, material_vars, sort_combobox, sort_order, suitable_materials 
    
    # Load materials from the CSV file
    global materials
    filename = 'materials_data.csv'
    materials = load_material_data(filename)
    
    if not materials:
        return  

    sort_order = True  # True for ascending, False for descending
    suitable_materials = []  

    window = tk.Tk()
    window.title("Material Selection Tool")
    window.configure(bg="#2E2E2E")  # Dark background

    # Style for ttk widgets
    style = ttk.Style()
    style.configure("TFrame", background="#2E2E2E")
    style.configure("TLabel", background="#2E2E2E", foreground="white")
    style.configure("TButton", background="#4D4D4D", foreground="black", padding=5) 
    style.configure("ScrolledText", background="#2E2E2E", foreground="white")

    style.configure("TLabelframe", background="#2E2E2E", bordercolor="#4D4D4D", relief="groove", padding=10)
    style.configure("TLabelframe.Label", font=("Helvetica", 10, "bold"), foreground="black")

    notebook = ttk.Notebook(window)
    notebook.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

    style = ttk.Style()
    style.configure('TNotebook.Tab', padding=[10, 5])  

    style.configure('TNotebook.Tab', background='#2E2E2E', foreground='black')
    style.map('TNotebook.Tab',
        background=[('selected', '#4A90E2')],  # Active tab color (blue)
        foreground=[('selected', 'white')],    # Active tab text color
        expand=[('selected', [1, 1, 1, 0])]    # Make active tab slightly larger
    )

    style.map('TNotebook.Tab',
        background=[('active', '#3A3A3A'),     # Hover color for inactive tabs
                    ('selected', '#4A90E2')],   # Keep active tab color
        foreground=[('active', 'black'),       # Hover text color
                    ('selected', 'red')]
    )

    search_frame = ttk.Frame(notebook)
    notebook.add(search_frame, text="Search")

    type_frame = ttk.Labelframe(search_frame, text="Select Material Type", padding="10")
    type_frame.grid(row=0, column=0, padx=70, pady=10, sticky=tk.NW)

    material_types = ["Metals", "Plastics", "Ceramics", "Composites", "Alloys"]
    material_vars = {}

    style.configure("TCheckbutton", background="#2E2E2E", foreground="white")

    for i, material_type in enumerate(material_types):
        var = tk.BooleanVar()
        material_vars[material_type] = var
        chk = ttk.Checkbutton(type_frame, text=material_type, variable=var, style="TCheckbutton")
        chk.grid(row=i, sticky=tk.W)

    input_frame = ttk.Labelframe(search_frame, text="Material Properties", padding="10")
    input_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NW)

    density_min_scale, density_max_scale = create_range_slider(input_frame, 0, "Density (kg/m³):", 500, 12000, 500, 12000)
    strength_min_scale, strength_max_scale = create_range_slider(input_frame, 1, "UTS (MPa):", 0, 1500, 0, 1500)
    cost_min_scale, cost_max_scale = create_range_slider(input_frame, 2, "Cost ($ per kg):", 0, 100, 0, 100)
    conductivity_min_scale, conductivity_max_scale = create_range_slider(input_frame, 3, "Thermal Conductivity (W/mK):", 0, 2000, 0, 2000)
    maximum_temperature_min_scale, maximum_temperature_max_scale = create_range_slider(input_frame, 4, "Maximum Temperature (C):", 0, 5000, 0, 5000)
    young_modulus_min_scale, young_modulus_max_scale = create_range_slider(input_frame, 5, "Young's Modulus (GPa):", 0, 1000, 0, 1000)
    thermal_capacity_min_scale, thermal_capacity_max_scale = create_range_slider(input_frame, 6, "Thermal Capacity (J/kgK):", 0, 2500, 0, 2500)
    tensile_strength_min_scale, tensile_strength_max_scale = create_range_slider(input_frame, 7, "Yield Tensile Strength (MPa):", 0, 4000, 0, 4000)
    ductility_min_scale, ductility_max_scale = create_range_slider(input_frame, 8, "Max Elongation (%):", 0, 150, 0, 150)
    recycle_fraction_min_scale, recycle_fraction_max_scale = create_range_slider(input_frame, 9, "Recycle Fraction (%):", 0, 100, 0, 100)

    # Dropdown for sorting
    sort_frame = ttk.Frame(search_frame, padding="10")
    sort_frame.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NW)

    sort_combobox = ttk.Combobox(sort_frame, values=[
        "density_(kg/m^3)", "UTS_(MPa)", "cost_per_kg_($)", "thermal_conductivity_(W/mK)",
        "maximum_temperature_(C)", "young_modulus_(GPa)", "thermal_capacity_(J/kgK)",
        "tensile_strength_yield_(MPa)", "Elongation_(%)", "recycle_fraction_(%)"
    ], state="readonly")
    sort_combobox.set("Select Property to Sort")
    sort_combobox.grid(row=0, column=0, padx=5, pady=5)
    sort_combobox.bind("<<ComboboxSelected>>", lambda e: update_results())

    # Sort order buttons
    def set_ascending():
        global sort_order
        sort_order = True
        update_results()  # Update results on button click

    def set_descending():
        global sort_order
        sort_order = False
        update_results()  # Update results on button click

    asc_button = ttk.Button(sort_frame, text="Ascending", command=set_ascending)
    asc_button.grid(row=0, column=1, padx=5, pady=5)

    desc_button = ttk.Button(sort_frame, text="Descending", command=set_descending)
    desc_button.grid(row=0, column=2, padx=5, pady=5)

    # Export button to save results to CSV
    export_button = ttk.Button(search_frame, text="Export to CSV", command=export_to_csv)
    export_button.grid(row=0, column=2, padx=150, pady=75, sticky=tk.NW)

    # Result display area
    result_frame = ttk.Frame(search_frame, padding="10")
    result_frame.grid(row=0, column=2, columnspan=6, padx=10, pady=120, sticky=tk.NW)

    filtered_label = ttk.Label(result_frame, text="Filtered Materials:  ", font=("Arial", 14, "bold"))
    filtered_label.grid(row=0, column=1, sticky="w", pady=200)  # Place label at the top of result_frame

    # Text area for displaying results
    result_text = scrolledtext.ScrolledText(result_frame, width=60, height=15, wrap=tk.WORD)
    result_text.grid(row=0, column=2, pady=(120, 100))  # Place result_text below the label

 # Create "Compare" tab with enhanced functionality
    compare_frame = ttk.Frame(notebook)
    notebook.add(compare_frame, text="Compare")

    # Property selection frame
    selection_frame = ttk.Frame(compare_frame, padding="10")
    selection_frame.pack(fill=tk.X, padx=10, pady=5)

    # Available properties for comparison
    properties = ["density_(kg/m^3)", "UTS_(MPa)", "cost_per_kg_($)", "thermal_conductivity_(W/mK)", "maximum_temperature_(C)", "young_modulus_(GPa)", "thermal_capacity_(J/kgK)", "tensile_strength_yield_(MPa)", "Elongation_(%)", "recycle_fraction_(%)"]
    
    # X-axis property selection
    ttk.Label(selection_frame, text="X-axis Property:").grid(row=0, column=0, padx=5)
    x_property_combobox = ttk.Combobox(selection_frame, values=properties, state="readonly")
    x_property_combobox.set("Select X Property")
    x_property_combobox.grid(row=0, column=1, padx=5)

    # Y-axis property selection
    ttk.Label(selection_frame, text="Y-axis Property:").grid(row=1, column=0, padx=5, pady=10)
    y_property_combobox = ttk.Combobox(selection_frame, values=properties, state="readonly")
    y_property_combobox.set("Select Y Property")
    y_property_combobox.grid(row=1, column=1, padx=5, pady=10)

    # Material type filter frame
    filter_frame = ttk.LabelFrame(compare_frame, text="Material Types", padding="10")
    filter_frame.pack(fill=tk.X, padx=10, pady=5)

    # Create checkboxes for material types
    compare_material_vars = {}
    material_types = set(material["type"] for material in materials)
    for i, mat_type in enumerate(material_types):
        var = tk.BooleanVar(value=True)
        compare_material_vars[mat_type] = var
        ttk.Checkbutton(filter_frame, text=mat_type, variable=var).grid(
            row=i//2, column=i%2, padx=5, pady=2, sticky="w"
        )

    # Add this dictionary near the top of your code or in the create_gui function
    property_units = {
    "density_(kg/m^3)": "kg/m³",
    "UTS_(MPa)": "MPa",
    "cost_per_kg_($)": "$/kg",
    "thermal_conductivity_(W/mK)": "W/mK",
    "maximum_temperature_(C)": "C",
    "young_modulus_(GPa)": "GPa",
    "thermal_capacity_(J/kgK)": "J/kg·K",
    "tensile_strength_yield_(MPa)": "MPa",
    "Elongation_(%)": "%",
    "recycle_fraction_(%)": "%"
    }


    # Updated plot_comparison function with units
    def plot_comparison():
        x_prop = x_property_combobox.get()
        y_prop = y_property_combobox.get()

        if x_prop == "Select X Property" or y_prop == "Select Y Property":
            messagebox.showwarning("Selection Error", "Please select both X and Y properties")
            return

        # Filter materials based on selected types
        selected_materials = [
            material for material in materials
            if compare_material_vars[material["type"]].get()
        ]

        if not selected_materials:
            messagebox.showwarning("Data Error", "No materials selected for comparison")
            return

        # Create the plot
        plt.figure(figsize=(10, 6))
        
        # Plot points for each material type with different colors
        material_types = set(material["type"] for material in selected_materials)
        colors = plt.cm.Set3(np.linspace(0, 1, len(material_types)))
        
        for mat_type, color in zip(material_types, colors):
            type_materials = [m for m in selected_materials if m["type"] == mat_type]
            x_values = [m[x_prop] for m in type_materials]
            y_values = [m[y_prop] for m in type_materials]
            plt.scatter(x_values, y_values, label=mat_type, color=color, alpha=0.6)
            
            # Add material names as annotations
            for i, material in enumerate(type_materials):
                plt.annotate(material['name'], (x_values[i], y_values[i]), 
                        fontsize=8, alpha=0.7, xytext=(5, 5),
                        textcoords='offset points')

        # Customize plot with units
        x_label = f"{x_prop.split('_')[0].title()} [{property_units[x_prop]}]"
        y_label = f"{y_prop.split('_')[0].title()} [{property_units[y_prop]}]"

        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"Material Property Comparison\n{y_label} vs {x_label}")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(title="Material Types", bbox_to_anchor=(1.05, 1), loc='upper left')

        # Show the plot with adjusted layout
        plt.tight_layout()
        plt.show()

    # Plot button
    ttk.Button(compare_frame, text="Plot Comparison", command=plot_comparison).pack(pady=10)

        # Database Management tab
    database_frame = ttk.Frame(notebook)
    notebook.add(database_frame, text="Material Database Management")

    # Define material types list (make sure this matches your actual material types)
    material_types = ["Metals", "Plastics", "Ceramics", "Composites", "Alloys"]

    # Functionality to add a new material
    def add_material():
        name = name_entry.get().strip()
        density = density_entry.get().strip()
        strength = strength_entry.get().strip()
        cost = cost_entry.get().strip()
        conductivity = conductivity_entry.get().strip()
        melting_point = maximum_temperature_entry.get().strip()
        young_modulus = young_modulus_entry.get().strip()
        thermal_capacity = thermal_capacity_entry.get().strip()
        tensile_strength = tensile_strength_entry.get().strip()
        ductility = ductility_entry.get().strip()
        recycle_fraction = recycle_fraction_entry.get().strip()
        material_type = type_combobox.get()

        # Input validation
        if not all([name, density, strength, cost, conductivity, melting_point, young_modulus, thermal_capacity,
                        tensile_strength, ductility, recycle_fraction, material_type]):
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if material_type == "Select Type":
            messagebox.showerror("Input Error", "Please select a material type!")
            return

        # Validate inputs
        try:
            density = float(density)
            strength = float(strength)
            cost = float(cost)
            conductivity = float(conductivity)
            melting_point = float(melting_point)
            young_modulus = float(young_modulus)
            thermal_capacity = float(thermal_capacity)
            tensile_strength = float(tensile_strength)
            ductility = float(ductility)
            recycle_fraction = float(recycle_fraction)

            # Validate ranges
            if not (0 < density <= 25000):
                raise ValueError("Density must be between 0 and 25000 kg/m³")
            if not (0 < strength <= 5000):  
                raise ValueError("UTS must be between 0 and 5000 MPa")
            if not (0 < cost <= 1000):  
                raise ValueError("Cost must be between 0 and 1000 $/kg")
            if not (0 <= conductivity <= 1000):  
                raise ValueError("Thermal conductivity must be between 0 and 1000 W/mK")
            if not (0 <= melting_point <= 5000): 
                raise ValueError("Maximum temperature must be between 0 and 5000 C")
            if not (0 <= young_modulus <= 1500):  
                raise ValueError("Young's modulus must be between 0 and 1500 GPa")
            if not (0 <= thermal_capacity <= 10000): 
                raise ValueError("Thermal capacity must be between 0 and 10000 J/kgK")
            if not (0 <= tensile_strength <= 1000): 
                raise ValueError("Yield Tensile strength must be between 0 and 1000 MPa")
            if not (0 <= ductility <= 100):  
                raise ValueError("Max Elongation must be between 0 and 100 %")
            if not (0 <= recycle_fraction <= 100):  
                raise ValueError("Recycle fraction must be between 0 and 100 %")

            new_material = {
                "name": name,
                "density_(kg/m^3)": density,
                "UTS_(MPa)": strength,
                "cost_per_kg_($)": cost,
                "thermal_conductivity_(W/mK)": conductivity,
                "maximum_temperature_(C)": melting_point,
                "young_modulus_(GPa)": young_modulus,
                "thermal_capacity_(J/kgK)": thermal_capacity,
                "tensile_strength_yield_(MPa)": tensile_strength,
                "Elongation_(%)": ductility,
                "recycle_fraction_(%)": recycle_fraction,
                "type": material_type
            }
            
            # Check for duplicate material names
            if any(material['name'].lower() == name.lower() for material in materials):
                messagebox.showerror("Input Error", "A material with this name already exists!")
                return

            materials.append(new_material)
            save_material_data(filename, materials)
            messagebox.showinfo("Success", f"Material '{name}' added successfully!")
            
            # Clear all fields after successful addition
            name_entry.delete(0, tk.END)
            density_entry.delete(0, tk.END)
            strength_entry.delete(0, tk.END)
            cost_entry.delete(0, tk.END)
            conductivity_entry.delete(0, tk.END)
            maximum_temperature_entry.delete(0, tk.END)
            young_modulus_entry.delete(0, tk.END)
            thermal_capacity_entry.delete(0, tk.END)
            tensile_strength_entry.delete(0, tk.END)
            ductility_entry.delete(0, tk.END)
            recycle_fraction_entry.delete(0, tk.END)
            type_combobox.set("Select Type")
            
        except ValueError as e:
            if str(e).startswith("could not convert"):
                messagebox.showerror("Input Error", "Please enter valid numerical values for properties.")
            else:
                messagebox.showerror("Input Error", str(e))

    # Create a form frame with better styling
    form_frame = ttk.LabelFrame(database_frame, text="Add New Material", padding="20")
    form_frame.pack(pady=20, padx=20, fill="x")

    # Grid configuration for better alignment
    form_frame.columnconfigure(1, weight=1)

    # Entry fields with labels and proper spacing
    ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Density (kg/m³):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    density_entry = ttk.Entry(form_frame)
    density_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="UTS (MPa):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    strength_entry = ttk.Entry(form_frame)
    strength_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Cost ($ per kg):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    cost_entry = ttk.Entry(form_frame)
    cost_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Thermal Conductivity (W/mK):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    conductivity_entry = ttk.Entry(form_frame)
    conductivity_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Maximum Temperature (C):").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    maximum_temperature_entry = ttk.Entry(form_frame)
    maximum_temperature_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Young's Modulus (GPa):").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    young_modulus_entry = ttk.Entry(form_frame)
    young_modulus_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Thermal Capacity (J/kgK):").grid(row=8, column=0, sticky="e", padx=5, pady=5)
    thermal_capacity_entry = ttk.Entry(form_frame)
    thermal_capacity_entry.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Yield Tensile Strength (MPa):").grid(row=9, column=0, sticky="e", padx=5, pady=5)
    tensile_strength_entry = ttk.Entry(form_frame)
    tensile_strength_entry.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Max Elongation (%):").grid(row=10, column=0, sticky="e", padx=5, pady=5)
    ductility_entry = ttk.Entry(form_frame)
    ductility_entry.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Recycle Fraction (%):").grid(row=11, column=0, sticky="e", padx=5, pady=5)
    recycle_fraction_entry = ttk.Entry(form_frame)
    recycle_fraction_entry.grid(row=11, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form_frame, text="Type:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    type_combobox = ttk.Combobox(form_frame, values=material_types, state="readonly")
    type_combobox.set("Select Type")
    type_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

    # Add material button
    add_button = ttk.Button(form_frame, text="Add Material", command=add_material)
    add_button.grid(row=16, column=0, columnspan=2, pady=20)

    # Start the GUI event loop
    window.mainloop()

    

# Run the GUI
if __name__ == "__main__":
    create_gui()