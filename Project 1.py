# SI 201 Project 1
# Your name: Brianna Nguyen
# Your student id: 23058414
# Your email: briannng@umich.edu
# Used ChatGPT for general structure advice for functions and test cases, and debugging 

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
        
        # Convert all  numerical columns
        numerical_columns = ['body_mass_g', 'flipper_length_mm', 'bill_length_mm', 'bill_depth_mm']
        
        for col in numerical_columns:
            value = row.get(col)
            if value and value != 'NA':
                # Check if it contains only digits and at most one decimal point
                if value.replace('.', '').isdigit():
                    row[col] = float(value)
                else:
                    row[col] = None
            else:
                row[col] = None
            
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
            
        # Convert mass to float if it's a string
        if isinstance(mass, str):
            # Skip if it's 'NA' or empty
            if mass == 'NA' or not mass:
                continue
            # Try to convert to float using simple check
            if mass.replace('.', '').isdigit():
                mass = float(mass)
            else:
                continue  # Skip if not convertible
        
        key = (species, sex)
        totals[key] = totals.get(key, 0.0) + mass
        counts[key] = counts.get(key, 0) + 1
    return {k: totals[k]/counts[k] for k in totals}



#calculation to find penguins with flippers longer than 200mm on each island
def percentage_long_flippers_by_island_for_species(rows, target_species, threshold=200.0):
    """
    Calculate percentage of penguins with flippers longer than threshold on each island for a specific species
    Uses: island, species, flipper_length_mm (3 columns)
    """
    island_data = {}
    
    for row in rows:
        island = row.get("island")
        species = row.get("species")
        flipper_length = row.get("flipper_length_mm")
        
        # Skip if not target species or missing data
        if species != target_species or not island or flipper_length is None:
            continue
            
        # Initialize with two counters: [total_count, long_flipper_count]
        if island not in island_data:
            island_data[island] = [0, 0]
            
        island_data[island][0] += 1  # Increment total count
        if flipper_length > threshold:
            island_data[island][1] += 1  # Increment long flipper count
    
    # Calculate percentages
    percentages = {}
    for island, counts in island_data.items():
        total, long_count = counts
        if total > 0:
            percentages[island] = (long_count / total) * 100
        else:
            percentages[island] = 0.0
            
    return percentages


#writing analysis results to csv file
def write_results_to_file(avg_body_mass, flipper_percentages, filename="penguin_analysis_results.csv"):
    outfile = open(filename, 'w')
    
    # Write CSV header
    outfile.write("analysis_type,species,sex,island,value,unit\n")
    
    # Write BOTH sections in CSV format:
    for (species, sex), avg_mass in avg_body_mass.items():
        outfile.write(f"average_body_mass,{species},{sex},,{round(avg_mass, 2)},grams\n")
    
    for island, percentage in flipper_percentages.items():
        outfile.write(f"long_flipper_percentage,Adelie,,{island},{round(percentage, 2)},%\n")
    
    outfile.close()


    
class TestProject1(unittest.TestCase):

    def setUp(self):
        CSV_PATH = "archive/penguins.csv" #locating file
        if not os.path.exists(CSV_PATH):
            self.skipTest(f"{CSV_PATH} not found.")
        self.rows = read_penguins(CSV_PATH)
        self.avg_dict = avg_body_mass_by_species_and_sex(self.rows)
        self.flipper_dict = percentage_long_flippers_by_island_for_species(self.rows, "Adelie")

    #test penguins read function
    def test_read_penguins_returns_list(self): 
        self.assertIsInstance(self.rows, list)
        
    def test_read_penguins_has_data(self):
        self.assertGreater(len(self.rows), 0)
        
    def test_read_penguins_has_dicts(self):
        self.assertIsInstance(self.rows[0], dict)
        
    def test_read_penguins_has_required_columns(self):
        for key in ("species", "island", "sex", "flipper_length_mm", "body_mass_g"):
            self.assertIn(key, self.rows[0])
            
            
            
    #tests for average body mass by species and sex
    def test_avg_body_mass_returns_dict(self):
        self.assertIsInstance(self.avg_dict, dict)
    
    def test_avg_body_mass_has_calculations(self):
        self.assertGreater(len(self.avg_dict), 0)
        
    def test_avg_body_mass_correct_calculation(self):
        adelie_male_mass = []
        
        for row in self.rows:
            if (row.get("species") == "Adelie" and row.get("sex") == "male" and row.get("body_mass_g") is not None): adelie_male_mass.append(row["body_mass_g"])

        if adelie_male_mass:
            expected_avg = sum(adelie_male_mass) / len(adelie_male_mass)
            actual_avg = self.avg_dict.get(("Adelie", "male"))
            if actual_avg is not None:
                self.assertAlmostEqual(actual_avg, expected_avg, places=2)
       
    #Test that function properly handles rows with missing data using controlled test data         
    def test_avg_body_mass_ignores_missing_data(self):
    
    # Create controlled test data with known missing values
        test_rows = [
            {"species": "Adelie", "sex": "male", "body_mass_g": 4000.0},
            {"species": "Adelie", "sex": "male", "body_mass_g": 3800.0},
            {"species": "Adelie", "sex": "female", "body_mass_g": 3500.0},
            {"species": "Gentoo", "sex": "female", "body_mass_g": 5000.0},  
        # missing data
            {"species": "Adelie", "sex": "male", "body_mass_g": None},           
            {"species": "Adelie", "sex": None, "body_mass_g": 3700.0},           
            {"species": None, "sex": "female", "body_mass_g": 3200.0},           
            {"species": "Gentoo", "sex": "male", "body_mass_g": "NA"},           
            {"species": "", "sex": "female", "body_mass_g": 3300.0},             
            {"species": "Chinstrap", "sex": "male", "body_mass_g": ""},
        ]
    
        result = avg_body_mass_by_species_and_sex(test_rows)
    
    # Test that only complete data is processed
        expected_adelie_male_avg = (4000.0 + 3800.0) / 2 
        expected_adelie_female_avg = 3500.0
        expected_gentoo_female_avg = 5000.0
    
    # Verify the correct averages (only from complete rows)
        self.assertIn(("Adelie", "male"), result)
        self.assertAlmostEqual(result[("Adelie", "male")], expected_adelie_male_avg, places=2)
    
        self.assertIn(("Adelie", "female"), result)
        self.assertAlmostEqual(result[("Adelie", "female")], expected_adelie_female_avg, places=2)
    
        self.assertIn(("Gentoo", "female"), result)
        self.assertAlmostEqual(result[("Gentoo", "female")], expected_gentoo_female_avg, places=2)
    
    # Verify incomplete data was skipped
        self.assertEqual(len(result), 3)  
    
    # Test edge case: empty input
        empty_result = avg_body_mass_by_species_and_sex([])
        self.assertEqual(empty_result, {})
        
    # Test function with all missing data
def test_avg_body_mass_all_missing_data(self):
    
    all_missing_rows = [
        {"species": None, "sex": "male", "body_mass_g": 3750.0},
        {"species": "Adelie", "sex": None, "body_mass_g": 3800.0},
        {"species": "Adelie", "sex": "male", "body_mass_g": None},
        {"species": None, "sex": None, "body_mass_g": None},
    ]
    
    result = avg_body_mass_by_species_and_sex(all_missing_rows)
    
    # Should return empty dict since no complete data
    self.assertEqual(result, {})
    self.assertEqual(len(result), 0)
    
    
#testing flippers
    
# test function returns a dictionary
def test_percentage_long_flippers_returns_dict(self):

    result = percentage_long_flippers_by_island_for_species(self.rows, "Adelie")
    self.assertIsInstance(result, dict)

# test function returns results for existing species
def test_percentage_long_flippers_has_calculations(self):
   
    result = percentage_long_flippers_by_island_for_species(self.rows, "Adelie")
    self.assertGreater(len(result), 0)
    
    

#test to see if function calculates percentages correctly
def test_percentage_long_flippers_correct_calculation(self):
  
    # Test with controlled data
    test_rows = [
        #long flippers
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 210.0},
        {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 201.0},  
        #short flippers
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 190.0},  
        {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 195.0},    
          
    ]
    
    result = percentage_long_flippers_by_island_for_species(test_rows, "Adelie", threshold=200.0)
    
    # Torgersen: 2 out of 3 have long flippers = 66.67%
    # Biscoe: 1 out of 2 have long flippers = 50.0%
    self.assertIn("Torgersen", result)
    self.assertIn("Biscoe", result)
    self.assertAlmostEqual(result["Torgersen"], (2/3)*100, places=2)
    self.assertAlmostEqual(result["Biscoe"], (1/2)*100, places=2)

def test_percentage_long_flippers_ignores_missing_data(self):
    """Test that function properly handles missing data"""
    test_rows = [
        # Complete data - should be processed
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 210.0},
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 205.0},
        
        # Missing data - should be SKIPPED
        {"species": "Adelie", "island": None, "flipper_length_mm": 210.0},           
        {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": None},        
        {"species": None, "island": "Dream", "flipper_length_mm": 210.0},            
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": "NA"},     
        {"species": "", "island": "Biscoe", "flipper_length_mm": 195.0},             
        {"species": "Adelie", "island": "", "flipper_length_mm": 201.0},             
    ]
    
    result = percentage_long_flippers_by_island_for_species(test_rows, "Adelie")
    
    # Should only process the first two complete rows
    self.assertIn("Torgersen", result)
    # 2 out of 2 have long flippers = 100%
    self.assertEqual(result["Torgersen"], (2/2)*100)  
    
    # Should not include islands with only missing data
    self.assertNotIn("Biscoe", result)
    self.assertNotIn("Dream", result)
        
def test_percentage_long_flippers_all_short(self):
    """Test when all penguins have short flippers"""
    test_rows = [
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 190.0},
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 195.0},
        {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 198.0},
        {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 192.0},
    ]
    
    result = percentage_long_flippers_by_island_for_species(test_rows, "Adelie", threshold=200.0)
    
    # All flippers are short, so percentages should be 0%
    self.assertIn("Torgersen", result)
    self.assertIn("Biscoe", result)
    self.assertEqual(result["Torgersen"], 0.0)
    self.assertEqual(result["Biscoe"], 0.0)

def main():     
    CSV_PATH = "archive/penguins.csv"
        
    penguin_data = read_penguins(CSV_PATH)
    
    if not penguin_data:
        print("No data found.")
        return
    avg_mass_results = avg_body_mass_by_species_and_sex(penguin_data)
    flipper_results = percentage_long_flippers_by_island_for_species(penguin_data, "Adelie")
    
    write_results_to_file(avg_mass_results, flipper_results)
    
    print("Analysis complete! Check penguin_analysis_results.csv")
    
if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
 
 