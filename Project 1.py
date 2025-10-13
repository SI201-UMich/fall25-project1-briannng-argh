# SI 201 Project 1
# Your name: Brianna Nguyen
# Your student id: 23058414
# Your email: briannng@umich.edu
# Used ChatGPT for....

from pathlib import Path
import csv
import unittest


BASE = Path(__file__).parent
# find the first CSV anywhere under the script folder (e.g., in 'archive/')
CSV_PATH = next(BASE.rglob("*.csv"), None)
if not CSV_PATH:
    raise FileNotFoundError("No .csv found. Is it inside the 'archive' folder?")
print("Using:", CSV_PATH.name)

with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    data = list(reader)

print(len(data), "rows")
print(data[0])



def read_penguins(path):
    num_cols = {"bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"}
    rows = []
    with Path(path).open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            row = dict(row)
            for col in num_cols:
                value = row.get(col)
                row[col] = float(value) if value not in (None, "", "NA") else None
            rows.append(row)
    return rows


def avg_body_mass_by_species_and_sex(rows):
    totals = {}
    counts = {}
    for r in rows:
        species = r.get("species"),
        sex = r.get("sex")
        mass = r.get("body_mass_g")
        if not species or not sex or mass is None:
            continue
        key = (species, sex)
        totals[key] = totals.get(key, 0.0) + mass
        counts[key] = counts.get(key, 0) + 1
    return {k: totals[k]/counts[k] for k in totals}

#calculation to find average weight for each species, seperated by female and male penguins

def percentage_long_flippers_by_island():
    pass

#calculation to find penguins with flippers longer than 200mm on each island
SAMPLE = [
    {"species":"Adelie","sex":"Male","body_mass_g":3700.0,"island":"Torgersen","flipper_length_mm":181.0},
    {"species":"Adelie","sex":"Female","body_mass_g":3400.0,"island":"Torgersen","flipper_length_mm":186.0},
    {"species":"Gentoo","sex":"Male","body_mass_g":5000.0,"island":"Biscoe","flipper_length_mm":220.0},
    {"species":"Gentoo","sex":"Female","body_mass_g":4600.0,"island":"Biscoe","flipper_length_mm":214.0},
    {"species":"Chinstrap","sex":"Male","body_mass_g":3800.0,"island":"Dream","flipper_length_mm":195.0},
]
class TestCalcs(unittest.TestCase):
  
    #Avg_body_mass_by_species_and_sex
    def test_avg_two_species(self):
        results = avg_body_mass_by_species_and_sex(SAMPLE)
        self.assertAlmostEqual(results[("Adelie", "Male")], 3700.0)
        self.assertAlmostEqual(results[("Adelie","Female")], 3400.0)

if __name__ == "__main__":
    unittest.main()
    