# VisiData config used only for screenshot capture.
# Anything here should make screenshots reproducible, not change behavior
# a reader would see when following the tutorial.
import random

# No network fetch on startup (the "message of the day" in the status bar).
options.motd_url = ''

# The help sidebar changes with version and context; keep the sheet uncluttered.
options.disp_sidebar = False

# Commands like select-random should pick the same rows every run.
random.seed(0)

# Don't draw the pop-up box of recent status messages ("selected 49 rows",
# "search wrapped", ...). It covers part of the sheet and disappears on the
# next keystroke; the status bar still shows counts like "•49".
from visidata import VisiData
VisiData.recentStatusMessages = property(lambda vd: '')

# In batch mode VisiData prints a timer ("[0.1s] 50%") to stderr while it
# replays; its value depends on machine speed, so leave it out.
VisiData.outputProgressEvery = lambda vd, sheet, seconds=0.5: None
