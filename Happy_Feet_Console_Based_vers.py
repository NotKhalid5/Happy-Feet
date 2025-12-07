"""Project Happy Feet is an initiative that uses the data from x dataset to be used by specialists
   to determine whether penguins both in captivity and in the wild are growing properly."""
import csv
import kagglehub

# Download latest version
path = kagglehub.dataset_download("larsen0966/penguins")

# print("Path to dataset files:", path)

def parse_csv(filename):
    dataset_a = []
    dataset_g = []
    dataset_c = []
    with open(filename,'r') as cf:
        reader = csv.DictReader(cf)
        invalid_adelies = 0
        invalid_gentoo = 0
        invalid_chinstraps = 0
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

def compare_flipper_length(flipper_length, average_flipper_length_for_species):
    u_good_mud = False
    if flipper_length < average_flipper_length_for_species:
        u_good_mud = False
        return f"This penguin's flipper length of {flipper_length}mm is less than the average flipper length for {species} of {average_flipper_length_for_species}mm." , u_good_mud
    elif flipper_length > average_flipper_length_for_species:
        u_good_mud = True
        return f"This penguin's flipper length of {flipper_length}mm is greater than the average flipper length for {species} of {average_flipper_length_for_species}mm." , u_good_mud
    else:
        u_good_mud = True
        return f"This penguin's flipper length of {flipper_length}mm is equal to the average flipper length for {species} which is {average_flipper_length_for_species}mm.", u_good_mud

def next_measures(comparison=True):
    if comparison:
        print("This penguin may need to seek professional help. Contact www.justiceforpenguins.org for help from experts.\n\n")

if __name__ == "__main__":
    dataset_a, dataset_g, dataset_c, invalid_adelies, invalid_gentoo, invalid_chinstraps  = parse_csv('penguins.csv')


    # Adelie Examples (Psuedo Test Cases)
    print("\n")
    species = "Adelie"
    average_flipper_length_for_adelies, invalid_adelies = find_avg_flipper_length(dataset_a, invalid_adelies)
    print(f"{species}s have an average flipper length of {average_flipper_length_for_adelies}.")
    print(f"This average was calculated excluding {invalid_adelies} penguin(s) that didn't have flipper length data.")
    comparison = compare_flipper_length(187.88, average_flipper_length_for_adelies)[1]
    print(compare_flipper_length(187.88, average_flipper_length_for_adelies)[0])
    if not(compare_flipper_length(187.88, average_flipper_length_for_adelies)[1]):
        next_measures(comparison=True)

    # Gentoo Examples (Psuedo Test Cases)
    print("\n")
    species = "Gentoo"
    average_flipper_length_for_gentoo, invalid_gentoo = find_avg_flipper_length(dataset_g, invalid_gentoo)
    print(f"{species}s have an average flipper length of {average_flipper_length_for_gentoo}.")
    print(f"This average was calculated excluding {invalid_gentoo} penguin(s) that didn't have flipper length data.")
    comparison = compare_flipper_length(217.188, average_flipper_length_for_gentoo)[1]
    print(compare_flipper_length(217.188, average_flipper_length_for_gentoo)[0])
    if not(compare_flipper_length(217.188, average_flipper_length_for_gentoo)[1]):
        next_measures(comparison=True)

    # Chinstrap  Examples (Psuedo Test Cases)
    print("\n")
    species = "Chinstrap"
    average_flipper_length_for_chinstraps, invalid_chinstraps = find_avg_flipper_length(dataset_c, invalid_chinstraps)
    print(f"{species}s have an average flipper length of {average_flipper_length_for_chinstraps}.")
    print(f"This average was calculated excluding {invalid_chinstraps} penguin(s) that didn't have flipper length data.")
    comparison = compare_flipper_length(195.824, average_flipper_length_for_chinstraps)[1]
    print(compare_flipper_length(195.824, average_flipper_length_for_chinstraps)[0])
    if not(compare_flipper_length(195.824, average_flipper_length_for_chinstraps)[1]):
        next_measures(comparison=True)
    print("\n")


    # format for t
    # dataset, invalid_count  = parse_csv('data/penguins.csv')
    # print(dataset_a)
    # average_flipper_length_for_species = find_avg_flipper_length(dataset)
    # print(compare_flipper_length(specific_penguin, average_flipper_length_for_species))
