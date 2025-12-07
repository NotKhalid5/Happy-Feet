"""
Project Happy Feet is an initiative that uses the data from x dataset to be used by specialists
to determine whether penguins both in captivity and in the wild are growing properly.
"""

import csv
import os
import streamlit as st
import kagglehub

# Download latest version
path = kagglehub.dataset_download("larsen0966/penguins")

def parse_csv(filename):
    dataset_a = []
    dataset_g = []
    dataset_c = []
    invalid_adelies = 0
    invalid_gentoo = 0
    invalid_chinstraps = 0
    with open(filename, 'r') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            species = row["species"]
            fl = row["flipper_length_mm"]
            if species == "Adelie":
                dataset_a.append(fl)
            elif species == "Gentoo":
                dataset_g.append(fl)
            elif species == "Chinstrap":
                dataset_c.append(fl)
    return dataset_a, dataset_g, dataset_c, invalid_adelies, invalid_gentoo, invalid_chinstraps

def find_avg_flipper_length(dataset, invalid_count):
    usable = []
    for value in dataset:
        try:
            usable.append(float(value))
        except (TypeError, ValueError):
            invalid_count += 1
    average = round(sum(usable)/len(usable), 3)
    return average, invalid_count

def compare_flipper_length(flipper_length, average_flipper_length_for_species, species):
    u_good_mud = False
    if flipper_length < average_flipper_length_for_species:
        u_good_mud = False
        return f"This penguin's flipper length of {flipper_length}mm is less than the average flipper length for {species} of {average_flipper_length_for_species}mm.", u_good_mud
    elif flipper_length > average_flipper_length_for_species:
        u_good_mud = True
        return f"This penguin's flipper length of {flipper_length}mm is greater than the average flipper length for {species} of {average_flipper_length_for_species}mm.", u_good_mud
    else:
        u_good_mud = True
        return f"This penguin's flipper length of {flipper_length}mm is equal to the average flipper length for {species} which is {average_flipper_length_for_species}mm.", u_good_mud

def next_measures(comparison=True):
    if comparison:
        st.warning("This penguin may need to seek professional help. Contact www.justiceforpenguins.org for help from experts.")


# ---------- STREAMLIT UI FUNCTION ----------
def run_streamlit_app(dataset_a, dataset_g, dataset_c, invalid_adelies, invalid_gentoo, invalid_chinstraps):
    st.title("🐧 Project Happy Feet")
    st.write("Determine whether penguins both in captivity and in the wild are growing properly.")

    # User input
    species = st.selectbox("Select Penguin Species", ["Adelie", "Gentoo", "Chinstrap"])
    fl_input = st.number_input("Enter Flipper Length (mm):", min_value=0.0, value=200.0)

    if species == "Adelie":
        average, invalid = find_avg_flipper_length(dataset_a, invalid_adelies)
    elif species == "Gentoo":
        average, invalid = find_avg_flipper_length(dataset_g, invalid_gentoo)
    else:
        averzage, invalid = find_avg_flipper_length(dataset_c, invalid_chinstraps)

    st.write(f"{species}s have an average flipper length of {average} mm (excluding {invalid} penguin(s) with missing data).")
    message, comparison = compare_flipper_length(fl_input, average, species)
    st.write(message)
    if not comparison:
        next_measures(comparison=True)


if __name__ == "__main__":
    # Automatically find CSV in data folder
    csv_path = os.path.join("data", "penguins.csv")
    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
    else:
        dataset_a, dataset_g, dataset_c, invalid_adelies, invalid_gentoo, invalid_chinstraps = parse_csv(csv_path)

        # Call Streamlit function
        run_streamlit_app(dataset_a, dataset_g, dataset_c, invalid_adelies, invalid_gentoo, invalid_chinstraps)
