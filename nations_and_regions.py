from parse_data import parse_data, Area
from plot_animation import plot_animation

def plot_nations_and_regions():

    region_url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=region&metric=newCasesBySpecimenDate&format=json"
    nation_url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&metric=newCasesBySpecimenDate&format=json"

    population_file = "population/nations_and_regions_population"
    events_file = "events/england"
    savefile_base_name = "nations-and-regions"

    areas = parse_data([region_url, nation_url], population_file)

    # start_time = datetime.now()

    plot_animation(areas, savefile_base_name, events_file)

    # end_time = datetime.now()

    # print((end_time - start_time).seconds)

if __name__ == "__main__":
    plot_nations_and_regions()