TRACKED_CLASSES = [
    'car',
    'motorcycle',
    'bus'
]

# TL, TR, BR, BL
SOURCE_RECT = [
    [183., 171.],
    [595., 188.],
    [1615., 700.],
    [66., 570.]
]

WIDTH = 100
HEIGHT = 300

# TL, TR, BR, BL
TARGET_RECT = [
    [0, 0],
    [WIDTH - 1, 0],
    [WIDTH - 1, HEIGHT - 1],
    [0, HEIGHT - 1]
]

TRACKING_REGION_COLOR = (0, 255, 0)
