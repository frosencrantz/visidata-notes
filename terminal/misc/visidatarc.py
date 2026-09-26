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
