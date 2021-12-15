import constants
from datetime import datetime as dt, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import ScalarFormatter, PercentFormatter
import seaborn as sns

class Graph:

    def __init__(self):

        self.scatter_plot = None
        self.trail_opacity = None
        self.labels = None
        self.date_text = None

animation_frames = (constants.END_DATE - constants.PLOT_START_DATE).days + 1 + constants.END_PAUSE_FRAMES

def get_event_string(date, events_by_date):

    event_string = ""
    opacity = 0

    for event_date in events_by_date:

        if event_date >= date - timedelta(days=constants.EVENT_FADE_DAYS) and event_date < date:
            event_string = events_by_date[event_date]

            opacity = 1 - (date - event_date).days/constants.EVENT_FADE_DAYS

    return (event_string, opacity)

def read_events_from_file(events_file):

    with open(events_file) as f:
        lines = f.readlines()

    events_by_date = {}

    for line in lines:
        linesplit = line.split(";")
        events_by_date[dt.strptime(linesplit[0],constants.DATE_FORMAT)] = linesplit[1]

    return events_by_date

def plot_animation(areas, file_base_name, events_file):

    start_time = dt.now()

    fig, ax = plt.subplots()

    graph = Graph

    events_by_date = read_events_from_file(events_file)

    ani = FuncAnimation(fig, update_graph, init_func=create_graph(ax, graph, areas, events_by_date), fargs=(graph, areas, events_by_date), frames=animation_frames, interval=constants.MS_PER_FRAME, repeat=False, blit=False)

    if constants.LOG_SCALE:
        file_name_suffix = "log"
    else:
        file_name_suffix = "linear"

    if constants.test:
        file_name_suffix = file_name_suffix + "-test"

    plt.show()

    # ani.save(f"/static/images/covid-visualisation-{file_base_name}-{file_name_suffix}-{dt.today().strftime(constants.DATE_FORMAT)}.gif", writer='imagemagick', fps=1000/constants.MS_PER_FRAME)
    
    ani.save("static/images/covid-visualisation.gif", writer='imagemagick', fps=1000/constants.MS_PER_FRAME)


def create_graph(ax, graph, areas, events_by_date):

    palette = sns.color_palette("Paired", len(areas))
    i = 0

    for name, area in areas.items():

        area.colour = palette[i]
        i = i + 1

    max_global_7d_cases = max(area.max_normalised_7d_cases for name, area in areas.items())

    y_axis_max = max_global_7d_cases * constants.Y_AXIS_HEADROOM

    # opacity = [i/constants.TRAIL_LENGTH_DAYS for i in range(constants.TRAIL_LENGTH_DAYS)]

    graph.trail_opacity = {}

    date = constants.PLOT_START_DATE

    while date <= constants.END_DATE:
        graph.trail_opacity[date] = 0

        date = date + timedelta(days=1)

    graph.trail_plots = {}

    for name, area in areas.items():

        graph.trail_plots[name] = {}

        x = [seven_day_change for date, seven_day_change in area.seven_day_changes.items() if date >= constants.PLOT_START_DATE]
        y = [normalised_seven_day_sum for date, normalised_seven_day_sum in area.normalised_seven_day_sums.items() if date >= constants.PLOT_START_DATE]

        date = constants.PLOT_START_DATE

        while date <= constants.END_DATE:
            
            j = (date - constants.PLOT_START_DATE).days

            graph.trail_plots[name][date] = (ax.plot(x[j-1:j+1],y[j-1:j+1],color=area.colour, alpha = graph.trail_opacity[date], zorder = 10, marker=None)[0])

            date = date + timedelta(days=1)

    ax.plot([0,0],[0,y_axis_max],'k--',zorder=0)

    x = []
    y = []

    x = [area.seven_day_changes[constants.PLOT_START_DATE] for name, area in areas.items()]
    y = [area.normalised_seven_day_sums[constants.PLOT_START_DATE] for name, area in areas.items()]
    size = [area.population*10 for name, area in areas.items()]
    names = [name for name, area in areas.items()]

    print(names)

    graph.scatter_plot = ax.scatter(x,y, s=size, c=palette, zorder = 20)

    graph.labels = []
    for j in range(len(names)):
        print(names[j])
        graph.labels.append(ax.annotate(names[j], (x[j], y[j]), fontsize=5, ha='center', zorder = 30))
        print(graph.labels)
    

    graph.date_text = ax.text(0.98,0.97,constants.PLOT_START_DATE.strftime(constants.DATE_FORMAT), ha='right', va='top', transform=ax.transAxes, fontsize=20)
    event_string, event_opacity = get_event_string(constants.PLOT_START_DATE, events_by_date)

    graph.event_text = ax.text(0.98,0.89,s=event_string,alpha=event_opacity, ha='right', va='top', transform=ax.transAxes)
    
    ax.text(0.26,0.94,s="Growth", ha='left', va='bottom', transform=ax.transAxes)
    ax.text(0.24,0.94,s="Decay", ha='right', va='bottom', transform=ax.transAxes)

    ax.set_xlim([-100,constants.X_AXIS_MAX])
    
    if constants.LOG_SCALE:
        ax.set_yscale('log')
    
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_major_formatter(PercentFormatter())
    ax.set_ylim([1,y_axis_max])
    
    plt.xlabel("Percent change on 7 days earlier")
    plt.ylabel("Cases in last 7 days, per 100k population")

def update_graph(frame, graph, areas, events_by_date):
    
    plot_date = constants.PLOT_START_DATE + timedelta(days = frame)
    plot_date = min(plot_date, constants.END_DATE)

    print(plot_date)

    trail_start_date = max(constants.PLOT_START_DATE,plot_date - timedelta(days = constants.TRAIL_LENGTH_DAYS))

    for date in graph.trail_opacity:

        if date < trail_start_date or date > plot_date:
            graph.trail_opacity[date] = 0
        else:
            graph.trail_opacity[date] = (date - trail_start_date).days / constants.TRAIL_LENGTH_DAYS

    for name, area in areas.items():

        # x = [seven_day_change for date, seven_day_change in area.seven_day_changes.items() if date >= constants.PLOT_START_DATE]
        # y = [normalised_seven_day_sum for date, normalised_seven_day_sum in area.normalised_seven_day_sums.items() if date >= constants.PLOT_START_DATE]

        # trail_plot = ax.plot(x,y)

        # for j in range(1,len(x)):
            # ax.plot(x[i:i+1],y[i:i+1],alpha=trail_opacity[i],color=area.colour, zorder = 10, marker=None)
            # ax.plot(x[j-1:j+1],y[j-1:j+1],color=area.colour, zorder = 10, marker=None)
        # trail_plots[name] = trail_plot

        trail_plot = graph.trail_plots[name]

        for date in trail_plot:
            

            trail_plot[date].set_alpha(graph.trail_opacity[date])
    
    x = []
    y = []

    x = [area.seven_day_changes[plot_date] for name, area in areas.items()]
    y = [area.normalised_seven_day_sums[plot_date] for name, area in areas.items()]

    graph.scatter_plot.set_offsets(np.c_[x,y])

    for j in range(len(graph.labels)):
        graph.labels[j].set_position((x[j],y[j]))

    print(graph.labels)

    graph.date_text.set_text(plot_date.strftime(constants.DATE_FORMAT))
    
    event_string, event_opacity = get_event_string(plot_date, events_by_date)

    graph.event_text.set_text(event_string)
    graph.event_text.set_alpha(event_opacity)



