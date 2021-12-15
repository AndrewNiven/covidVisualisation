import json
from datetime import datetime as dt, timedelta
import urllib.request

import constants

class Area:

    def __init__(self, name, population):

        self.name = name
        self.population = population / 100000
        self.cases = {}
        self.max_normalised_7d_cases = 0

    def populate_seven_day_sums(self):

        self.seven_day_sums = {}

        seven_day_sum = 0

        # print(self.cases)

        for i in range(0,7):
            seven_day_sum = seven_day_sum + self.cases[constants.START_DATE + timedelta(days=i)]

        self.seven_day_sums[constants.START_DATE + timedelta(days=7)] = seven_day_sum

        date = constants.START_DATE + timedelta(days=7)

        while date <= constants.END_DATE:

            seven_day_sum = seven_day_sum - self.cases[date - timedelta(days=7)]
            seven_day_sum = seven_day_sum + self.cases[date]

            # print(sevenDaySum)

            self.seven_day_sums[date] = seven_day_sum

            date = date + timedelta(days=1)

    def normalise_seven_day_sums(self):

        self.normalised_seven_day_sums = {}

        for date in self.seven_day_sums:

            normalised_seven_day_sum = self.seven_day_sums[date] / self.population

            self.max_normalised_7d_cases = max(self.max_normalised_7d_cases, normalised_seven_day_sum)

            self.normalised_seven_day_sums[date] = normalised_seven_day_sum

        # print(self.normalised_seven_day_sums)

    def calculate_seven_day_changes(self):

        self.seven_day_changes = {}

        for date in self.seven_day_sums:
            
            if date - timedelta(days=7) not in self.seven_day_sums:
                continue
            elif self.seven_day_sums[date - timedelta(days=7)] == 0:
                self.seven_day_changes[date] = 99999 
            else:
                self.seven_day_changes[date] = 100*(self.seven_day_sums[date] - self.seven_day_sums[date - timedelta(days=7)])/self.seven_day_sums[date - timedelta(days=7)]


def parse_data(data_urls, population_file):

    with open(population_file) as f:
        lines = f.readlines()

    areas = {}

    
    areas_by_parent_regions = {}

    for line in lines:

        linesplit = line.split(";")

        name = linesplit[0]
        population = int(linesplit[1])


        areas[name] = (Area(name,population))
        
        if len(linesplit) > 2:
            parent_region_name = linesplit[2]
            
            if parent_region_name not in areas_by_parent_regions:
                areas_by_parent_regions[parent_region_name] = [areas[name]]
            else:
                areas_by_parent_regions[parent_region_name].append(areas[name])

    print(areas_by_parent_regions)    

    collected_area_data = []

    for url in data_urls:

        with urllib.request.urlopen(url) as this_url:
            area_data = json.loads(this_url.read().decode())
            area_data = area_data["body"]

            collected_area_data = collected_area_data + area_data

    for item in collected_area_data:

        if item["areaName"] in areas.keys():
            areas[item["areaName"]].cases[dt.strptime(item["date"],constants.DATE_FORMAT)] = item["newCasesBySpecimenDate"]

    if len(areas_by_parent_regions) > 0:
        
        parent_regions = {}

        for parent_region_name in areas_by_parent_regions:

            parent_region = Area(parent_region_name,0)

            for area in areas_by_parent_regions[parent_region_name]:

                parent_region.population = parent_region.population + area.population

                for date in area.cases:
                    if date not in parent_region.cases:
                        parent_region.cases[date] = 0

                    parent_region.cases[date] = parent_region.cases[date] + area.cases[date]

            parent_regions[parent_region_name] = parent_region

        areas = parent_regions

    for name, area in areas.items():

        area.populate_seven_day_sums()

        area.normalise_seven_day_sums()

        area.calculate_seven_day_changes()

    return areas
    



