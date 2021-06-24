import numpy as np
import control as ct
import csv
import datetime as dt

class DataExtract():
    data_loc = ct.db_loc  
    col_dic = ct.col_dic  
    dob = dt.datetime.strptime(ct.dob, '%d/%m/%Y')
    
    def open_db(self):
        #Opens and extracts data as list
        with open(self.data_loc, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        return data

    def unique_of_cats(self, data):
        #Returns distinct categories in the data
        all_cats = [x[self.col_dic['cat']] for x in data if x[self.col_dic['cat']] != '']
        unq_cats = set(all_cats)
        return unq_cats

    def num_weeks_since_birth(self, date):
        #Given date, calculate the number of weeks since birth
        if (date - self.dob).days < 0:
            print(str(date) + ' is before you were born!')
            delta = 0
        else:
            delta = (date - self.dob).days // ct.days_per_week

        return delta

    def coords_from_data(self, data):
        #Finds the coordinates of each entry in the database and returns list of start/end coords
        start_coords = []
        end_coords = []

        #Skip headers
        for entry in data[1:]:
            if entry[self.col_dic['date_from']] != '':
                start_week = self.num_weeks_since_birth(dt.datetime.strptime(entry[self.col_dic['date_from']], '%d/%m/%Y'))
                start_coords.append(start_week)

                if entry[self.col_dic['date_to']] == '':  
                    end_week = self.num_weeks_since_birth(dt.datetime.today())
                else:
                    end_week = self.num_weeks_since_birth(dt.datetime.strptime(entry[self.col_dic['date_to']], '%d/%m/%Y'))
                    
                end_coords.append(end_week)
        
        return start_coords, end_coords

    def boolian_array_maker(self):
        #Given data, makes an array of whether a given week includes each category.

        data = self.open_db()

        unq_cats = list(self.unique_of_cats(data))
        array_holder = np.zeros((ct.last_year + 1, ct.weeks_per_year, len(unq_cats))) #extra year added to include final year
        mask_template = np.reshape(np.arange(0, (ct.last_year + 1) * ct.weeks_per_year), (ct.last_year + 1, ct.weeks_per_year))

        s_coord, e_coord = self.coords_from_data(data)
        
        for idx, entry in enumerate(data[1:]):
            cat_num = unq_cats.index(entry[self.col_dic['cat']])

            #mask array
            mask = (mask_template >= s_coord[idx]) & (mask_template <= e_coord[idx])
            array_holder[mask, cat_num] = 1 / len(unq_cats)
            
        return array_holder