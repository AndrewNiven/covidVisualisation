from datetime import datetime as dt, timedelta

DATE_FORMAT = "%Y-%m-%d"
START_DATE = dt.strptime("2020-04-01",DATE_FORMAT)
PLOT_START_DATE = dt.strptime("2021-01-01",DATE_FORMAT)

test=True

if dt.now().hour < 17:
    END_DATE_DAYS_AGO = 5
else:
    END_DATE_DAYS_AGO = 4

END_DATE = dt.today() - timedelta(days=END_DATE_DAYS_AGO)
END_DATE = dt(END_DATE.year,END_DATE.month,END_DATE.day,0,0,0,0)

TRAIL_LENGTH_DAYS = 50
MS_PER_FRAME = 200

END_PAUSE_FRAMES = 20

LOG_SCALE = False

Y_AXIS_HEADROOM = 1.2 # Factor by which the y axis goes higher than the highest value in the graph
X_AXIS_MAX = 300

EVENT_FADE_DAYS = 20

