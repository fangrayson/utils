"""
Module containing functions and variables to assist in drawing plots
"""

from cycler import cycler

# Official colours for UKHSA use, as per the UKHSA Identity guidelines: https://www.khub.net/documents/135939561/603183171/UKHSA+colour+palette+Pantone+CMYK+RGB+HTML.pdf/43e59a6c-ff52-6a19-27d6-d813646b1b11?t=1646138663715
UKHSA_colour_palette = {
    # Primary Identity Colour
    "UKHSA_teal": "#007C91",
    # Secondary Colours:
    "midnight" : "#003B5C",
    "plum" : "#582C83",
    "moonlight" : "#1D57A5",
    "wine" : "#8A1B61",
    "cherry" : "#E40046",
    "DHSC_green" : "#00AB8E",
    "ocean" : "#00A5DF",
    "grass" : "#84BD00",
    "tangerine" : "#FF7F32",
    "sunny" : "#FFB81C",
    "sand" : "#D5CB9F",
}

# Order to use the colours in
UKHSA_colour_names_cycle = [
    "UKHSA_teal",
    "grass",
    "midnight",
    "cherry",
    "ocean",
    "plum",
    "sunny",
    "moonlight",
    "wine",
    "tangerine",
    "DHSC_green",
    "sand"
]

# Generating a colour cycler
UKHSA_colour_cycler = cycler('color', [UKHSA_colour_palette[color] for color in UKHSA_colour_names_cycle])

# UKHSA theme parameters. The list of settings can be found in plt.rcParams.keys()
# For more help, visit: https://matplotlib.org/stable/tutorials/introductory/customizing.html
UKHSA_theme_rc_params = {
    # Font settings
    'font.family':  'sans-serif',
    'font.sans-serif' : ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"], # Order in which to try fonts in the sans-serif font family
    "font.size": 13.0, # Default text font size
    "font.style" : "normal", # Default text not italicised
    # Background and grid
    "axes.facecolor" : "white", # Background white
    'axes.grid' : True, # Show grid lines
    'axes.grid.axis' : "y", # Only show horizontal grid lines
    "grid.color" : "lightgrey", # Grid lines set to grey
    # Suptitle (treat this as the main title)
    "figure.titlesize" : "large", # Suptitle default font size (large is relative to "font.size")
    "figure.titleweight" : "bold", # Suptitle default font weight
    # Title (treat this as the subtitle)
    "axes.titlesize" : "medium",
    "axes.titleweight" : "normal",
    "axes.titlelocation" : "left", # Left align the title
    "axes.titlepad" : 6.0, # (vertical padding)
    # Axes labels
    "axes.labelsize" : "medium",
    "axes.labelweight" : "normal",
    # Axes ticks
    "xtick.labelsize" : "small",
    "ytick.labelsize" : "small",
    # Axes borders
    'axes.spines.left': False, # Remove the axes spines
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.spines.bottom': False,
    # Graph properties
    'lines.linewidth' : 3,
    "lines.color" : UKHSA_colour_palette["UKHSA_teal"],
    "patch.facecolor": UKHSA_colour_palette["UKHSA_teal"],
    "patch.edgecolor": "white",
    "axes.prop_cycle" : UKHSA_colour_cycler,
    # Legend properties
    "legend.loc" : "center right",
    "legend.edgecolor" : "white",
    "legend.fontsize" : "medium",
    "legend.labelspacing": 1.0,
}
