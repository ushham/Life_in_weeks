import numpy as np
import control as ct
import csv
import datetime as dt

class DataExtract():
    data_loc = ct.db_loc  
    col_dic = ct.col_dic  
    dob = dt.datetime.strptime(ct.dob, '%d/%m/%Y')

    def __init__(self):
        with open(self.data_loc, newline='') as f:
            self.reader = csv.reader(f)
            self.db = list(self.reader)

    def unique_batches(self, data, rings=True):
        #Returns the unique combinations of category and colour [(cat, colour)]
        if rings:
            all_batches = [(x[self.col_dic['cat']], x[self.col_dic['colour']]) for x in data if (x[self.col_dic['cat']] != '') and (x[self.col_dic['cat']] != ct.event)]
            unique_batches = list(dict.fromkeys(all_batches))
        else:
            unique_batches = [x for x in data if (x[self.col_dic['cat']] != '') and (x[self.col_dic['cat']] == ct.event)]
        
        return unique_batches

    def unique_cats(self, data):
        all_cats = [x[self.col_dic['cat']] for x in data if (x[self.col_dic['cat']] != '') and (x[self.col_dic['cat']] != ct.event)]
        unique_cats = list(set(all_cats))
        return unique_cats

    def filter_data_by_batch(self, data, batch):
        #Returns a list of data with the same (cat, colour) in the full data
        filtered_data = [x for x in data if (x[self.col_dic['cat']], x[self.col_dic['colour']]) == batch]
        return filtered_data

    def num_weeks_since_birth(self, date):
        #Given date, calculate the number of weeks since birth
        if (date - self.dob).days < 0:
            print(str(date) + ' is before you were born!')
            delta = 0
        else:
            delta = (date - self.dob).days / ct.days_per_week

        #Corrects the number of weeks since birth as there are 52.1 weeks/year, and we are trying to fit that into a 52 week grid
        years_since_birth = delta / ct.weeks_per_year
        years = int(years_since_birth)
        this_year = years_since_birth - years

        years_corr, this_year_corr = years * ct.standard_weeks_year, this_year * ct.standard_weeks_year
     
        return int(years_corr + this_year_corr)

    def coords_from_data(self, data):
        #Finds the coordinates of each entry in the database and returns list of start/end coords
        start_coords = []
        end_coords = []

        #Skip headers
        for entry in data:
            if entry[self.col_dic['date_from']] != '':
                start_week = self.num_weeks_since_birth(dt.datetime.strptime(entry[self.col_dic['date_from']], '%d/%m/%Y'))
                start_coords.append(start_week)

                if entry[self.col_dic['date_to']] == '':  
                    end_week = self.num_weeks_since_birth(dt.datetime.today())
                else:
                    end_week = self.num_weeks_since_birth(dt.datetime.strptime(entry[self.col_dic['date_to']], '%d/%m/%Y'))
                    
                end_coords.append(end_week)
        
        return start_coords, end_coords

    def extract_data(self):
        #Combines required data extraction functions to input into boolean array maker
        data = self.db[1:]
      
        s_coord, e_coord = self.coords_from_data(data)
        unq_batches = self.unique_batches(data)

        return data, unq_batches, s_coord, e_coord


    def boolian_array_maker(self, data, unq_batches, s_coord, e_coord):
        #Given data, makes an array of whether a given week includes each category.

        num_batches = len(unq_batches)

        array_holder = np.zeros((ct.life_expectancy + 1, ct.standard_weeks_year, num_batches)) #extra year added to include final year
        mask_template = np.reshape(np.arange(0, (ct.life_expectancy + 1) * ct.standard_weeks_year), (ct.life_expectancy + 1, ct.standard_weeks_year))
        
        for idx, entry in enumerate(data):
            if entry[self.col_dic['cat']] != ct.event:
                cat_num = unq_batches.index((entry[self.col_dic['cat']], entry[self.col_dic['colour']]))

                #mask array
                mask = (mask_template >= s_coord[idx]) & (mask_template <= e_coord[idx])
                array_holder[mask, cat_num] = 1 / num_batches

        #Pulls out unique categories
        cats = self.unique_cats(data)
            
        return array_holder, unq_batches, cats

    def ring_locs(self):
        #Returns the ring location and colours to show life events
        data = self.db[1:]
        unq_rings = self.unique_batches(data, False)
        
        holder = []

        for event in unq_rings:
            weeks_since_birth = self.num_weeks_since_birth(dt.datetime.strptime(event[self.col_dic['date_from']], '%d/%m/%Y'))
            coords = (weeks_since_birth // ct.standard_weeks_year, weeks_since_birth % ct.standard_weeks_year)

            holder.append([coords, event[self.col_dic['colour']]])
        
        return holder