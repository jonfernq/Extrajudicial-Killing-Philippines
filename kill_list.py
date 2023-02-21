# kill_list.py - 

# consolidates all the steps of cleaning the Inquirer 'Kill List' 
# before using it to plot visualizations of spatial distribtuion of killings
  
# read file into list of lines 
# eliminate all blank lines
# iterate over lines
# two types of lines, date line and data line
# if date line, put date into current date
# if data line, format output record with current date as first file 

import csv, re  
from datetime import datetime

def convert_date(date_string):
    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
              'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    date_parts = date_string.split()
    month = months.index(date_parts[0]) + 1
    day = int(date_parts[1].replace(',', ''))
    year = int(date_parts[2])
    return datetime(year, month, day)

def remove_blank_lines(lines):
    # remove blank lines from list of lines 
	newlines = []
	for line in lines: 
		if line != '':  
			newlines.append(line)
	return newlines 		
	
def get_data_lines(filename):
    # read lines from data file, remove blank lines 
    lines = []
    with open(filename,'rt',encoding='utf-8') as f: 
        for line in f: 
            lines.append(line.strip())
    newlines = remove_blank_lines(lines)
    return newlines 

def line2list(lines): 
	newlines = []
	for line in lines: 
		l = line.split('|')
		m = [] 
		for i in l:
			m.append(i.strip())
		newlines.append(m)
		return newlines 

def insert_date_in_line(lines):
    # 
    lines2 = []  
    current_date = "" 
    for line in lines:
        if is_date_line(line):
            pass 
            current_date = line.strip() 
        else:
            lines2.append(current_date + ' | ' + line) 
    return lines2

def is_date_line(line):
    pieces = line.split()
    if pieces[0] in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']: 
        return True 
    else: 
        return False     
    
def write_lines_to_file(lines, filename):
    with open(filename, 'w', encoding='utf-8') as fout: 
        for line in lines: 
            fout.write(line + '\n')           
    
def bar2lst(lines):
    newlines = [] 
    for line in lines:
        newline = line.split('|')
        newlines.append(newline)
    return newlines         

def is_valid_time(time_str):
    time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9] (a\.m\.|p\.m\.)$', re.IGNORECASE)
    return bool(time_pattern.match(time_str)) 
    
def insert_missing_times(lines):     
    previous_line = ['','','','',] 
    for line in lines: 
        time_field = line[1].strip()
        #print('*' + time_field + '*')
        #print(is_valid_time(time_field))  
        if not is_valid_time(time_field) and not time_field in ['Early morning', 'Evening', 'Morning', 'Afternoon', 'Before midnight', 'Before dawn']: 
            if line[0].strip() == previous_line[0].strip(): 
                line[1] = previous_line[1].strip()
            else: 
                print('ERROR:') 
                print(str(line))
                print(str(previous_line)) 
                #quit()                 
        previous_line = line            


def shift_columns_right(row, col_index):
    for i in range(len(row) - 1, col_index - 1, -1):
        row[i] = row[i - 1]
    row[col_index] = 'None'
    return row

def is_valid_time_string(time_string):
    # validate string as being valid time, return true or false 
    valid_time_strings = ['Early morning', 'Evening', 'Morning', 'Afternoon', 'Before midnight', 'Before dawn', 'Dawn', 'Late evening'] 
    valid_time_regex = re.compile(r'^\s*(\d{1,2}):(\d\d)\s+(a\.m\.|p\.m\.)\s*$')
    time_string = time_string.strip()
    if time_string in valid_time_strings:
        return True
    match = valid_time_regex.match(time_string)
    if match is None:
        return False
    hours, minutes, am_pm = match.groups()
    hours = int(hours)
    minutes = int(minutes)
    if not (0 <= hours <= 12 and 0 <= minutes <= 59):
        return False
    return True

def validate_record(record):
    # Perform validation checks on the record
    time_index = 1 
    time_string = record[time_index]
    if not is_valid_time_string(time_string) and len(time_string) >= 15:
        is_valid = False 
    else: 
        is_valid = True 
    
    # If the record is invalid, reformat it
    if not is_valid:
        # Perform reformatting
        record = shift_columns_right(record, time_index) # shift columns write, opening up a 'time' column 
        print('shifted: ', record)         
    return record

def split_place(place):
    # Split place on comma
    parts = [p.strip() for p in place.split(',')]
    
    # Initialize the new fields
    barangay, city, province = '', '', ''
    
    # Check the number of elements in parts
    if len(parts) == 1:
        city = parts[0]
    elif len(parts) == 2:
        city, province = parts
    elif len(parts) == 3:
        barangay, city, province = parts
    else:
        barangay = parts[0:-2]
        city     = parts[-2]
        province = parts[-1]
        print('3+ parts: ', barangay, city, province)  
        #raise ValueError('Place field must have at most 3 elements')
    return barangay, city, province

def main():
    filename = 'kill_list.txt'
    lines = get_data_lines(filename)     # read lines from data file, remove blank lines 
    lines2 = insert_date_in_line(lines)  
    write_lines_to_file(lines2, 'reformatted.txt') 
    lines3 = bar2lst(lines2)
    header = ['date', 'time', 'name', 'place', 'facts']
    with open("kill_list_2.csv", "w", newline="\n", encoding="utf-8") as f: 
       writer = csv.writer(f, delimiter='\t')
       writer.writerow(header)
       writer.writerows(lines3)   
    lines4 = list(reversed(lines3))     
    print(str(lines4))  
    lines5 = insert_missing_times(lines4)       
    print(str(lines5))  


    input_filename = 'kill_list_2.csv'
    output_filename = 'kill_list_3.csv'
    with open(input_filename, 'r', encoding='utf-8') as input_file, open(output_filename, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(input_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')
        header = next(reader)        # Extract the header record
        writer.writerow(header)      # Write the header to the output file
        for record in reader:
            validated_record = validate_record(record)
            writer.writerow(validated_record)
            
    import pandas as pd

    # Load the csv file into a pandas dataframe
    df = pd.read_csv('kill_list_3.csv', delimiter='\t', parse_dates=['date']) 

    # Add the 'no.' column with sequential record numbers
    df.insert(0, 'no.', range(1, len(df) + 1))

    # Convert the 'date' column to a pandas datetime object
    print("df['date']: ", df['date']) 
    if not df['date'].empty: 
        df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')

    # Save the updated dataframe to a new csv file
    df.to_csv('kill_list_4.csv', index=False, sep='\t') 
    

    # Read the input CSV file
    with open('kill_list_4.csv', 'r', encoding='utf-8') as f_in:
        reader = csv.reader(f_in, delimiter='\t')
        header = next(reader)
        
        # Add the new fields to the header
        header += ['barangay', 'city', 'province']
        
        # Write the new CSV file
        with open('kill_list_5.csv', 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.writer(f_out, delimiter='\t')
            writer.writerow(header)
            
            # Iterate through the records
            for row in reader:
                place = row[header.index('place')]
                barangay, city, province = split_place(place)
                
                # Add the new fields to the row
                row += [barangay, city, province]
                writer.writerow(row)
        
 	    
if __name__=="__main__":
    main()

