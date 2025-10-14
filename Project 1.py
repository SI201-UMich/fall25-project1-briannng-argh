# SI 201 Project 1
# Your name: Brianna Nguyen
# Your student id: 23058414
# Your email: briannng@umich.edu
# Used ChatGPT for....

import csv
import os
import unittest

def read_penguins(f):
    inFile = open(f)
    csvFile = csv.DictReader(inFile)
    rows = []
    for row in csvFile:
        if not row:
            continue #skip empty 
        rows.append(dict(row))


    inFile.close()

    return rows

#calculation to find average weight for each species, seperated by female and male penguins

def avg_body_mass_by_species_and_sex(rows):
    totals = {}
    counts = {}
    for r in rows:
        species = r.get("species")
        sex = r.get("sex")
        mass = r.get("body_mass_g")
        if not species or not sex or mass is None:
            continue
        key = (species, sex)
        totals[key] = totals.get(key, 0.0) + mass
        counts[key] = counts.get(key, 0) + 1
    return {k: totals[k]/counts[k] for k in totals}



#calculation to find penguins with flippers longer than 200mm on each island
def percentage_long_flippers_by_island(rows, threshhold=200.0):
    island_stats = {}
    
    for row in rows:
        island = row.get("island")
        flipper_length = row.get("flipper_length_mm")
        species = row.get("species")
        
        # Skip rows with missing data
        
        if not island or flipper_length is None or not species:
            continue
        
        #initalize island data if not present
        if island not in island_stats:
            island_stats[island] = {'total': 0, 'long_flipper': 0}
            
        island_stats[island]['total'] += 1
        if flipper_length > threshhold:
            island_stats[island]['island_flippers'] += 1
            
        #calculate percentages 
        
        percentages = {}
        for island, stats in island_stats.items():
            if stats['total'] > 0:
                percentages[island] = (stats['long_flippers'] / stats['total']) * 100
            else:
                percentages[island] = 0.0
        
        return percentages

def write_results_to_file(avg_body_mass, flipper_percentages, filename="penguin_analysis_results.txt"):
    pass

class TestProject1(unittest.TestCase):

    def setUp(self):
        CSV_PATH = "archive/pengunis.csv" #locating file
        if not os.path.exists(CSV_PATH):
            self.skipTest(f"{CSV_PATH} not found.")
        self.rows = read_penguins(CSV_PATH)

        # Precompute results
        self.avg_dict = avg_body_mass_by_species_and_sex(self.rows)
        self.flipper_dict = percentage_long_flippers_by_island(self.rows)

    #test penguins read function
    def test_read_penguins(self): 
        self.assertIsInstance(self.rows, list)
        self.assertGreater(len(self.rows), 0)
        self.assertIsInstance(self.rows[0], dict)
        
        for key in ("species", "island", "sex", "flipper_length_mm", "body_mass_g"):
            self.assertIn(key, self.rows[0])
        
        val = None
        for row in self.rows:
            v = row.get("body_mass_g")
            
            if v not in (None, "", "NA"):
                val = v
                break
        self.assertIsNotNone(val, "No usable body_mass_g values found in dataset.")
        
        #tests for average body mass by species and sex
        
    def avg_matches(self, species, sex):
        vals = []
        for row in self.rows:
            if row.get("species") == species and row.get("sex") == sex:
                v = row.get("body_mass_g")
                if v not in (None, "", "NA"):
                    vals.append(float(v))
        if not vals:
            return None           
        return sum(vals) / len(vals)
    
    def test_avg_matches_manual_for_adelie_male(self):
        species = "Adelie"
        sex = "Male"
        expected = self.avg_matches(species, sex)
        if expected is None:
            self.skipTest("No Adelie Male rows present; dataset variant differs.")
        self.assertAlmostEqual(self.avg_dict[(species, sex)], expected, places=6)
    
    def test_avg_ignores_missing_body_mass(self):
        species = "Adelie"
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
       