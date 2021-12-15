import constants
from parse_data import parse_data, Area
from plot_animation import plot_animation
from datetime import datetime

def main():

    utla_url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=newCasesBySpecimenDate&format=json"
    ltla_url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&format=json"

    population_file = "population/scotland_la_population"
    events_file = "events/scotland"
    savefile_base_name = "scotland-las"

    areas = parse_data([utla_url, ltla_url], population_file)

    start_time = datetime.now()

    print(areas)

    plot_animation(areas, savefile_base_name, events_file)

    end_time = datetime.now()

    print((end_time - start_time).seconds)

if __name__ == "__main__":

    main()