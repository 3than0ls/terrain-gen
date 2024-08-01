from pathlib import Path
import json

Gradient = dict[int, str]


def load_gradient(fp: Path) -> Gradient:
    """
    Load a gradient from a JSON file. 
    Return Gradient object, which is just a dictionary with a int key to hex string.
    """
    with open(fp) as f:
        gradient = json.load(f)["gradient"]

    out = {}
    for height, color in gradient.items():
        out[int(height)] = color

    return out


def get_color(gradient: Gradient, value: int) -> str:
    """
    Given a gradient and a value, return the gradient color.
    If there are no colors in the gradient, return black.
    If no floor gradient height/color is specified, return black.
    Otherwise, return the gradient color that corresponds to the floor gradient height.
    """
    out = "#000"
    for height, color in reversed(gradient.items()):
        if value >= height:
            out = color
            break

    return out
