#! python3

from PIL import Image
import argparse

# This is a Python port of Pixels to SVG (https://codepen.io/shshaw/pen/XbxvNj),
# since Python fits better with my workflow. 
# Works best with 8-bit images, or graphics where colors are limited and the 
# dimensions are relatively small. After conversion, run the output through 
# SVGOMG for even smaller file sizes.
#
# The image data is extracted from a canvas, and separated by color. 
# The coordinates for each color are combined into single runs where 
# possible to keep the path data syntax short, then merged into one 
# path with a stroke of the color.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_color(r, g, b, a):
    if a == 255:
        return f"#{r:02x}{g:02x}{b:02x}"
    elif a == 0:
        return None
    return f"rgba({r},{g},{b},{a / 255})"

def create_pixel_run_path(origin: Point, width):
    return f"M{origin.x} {origin.y}h{width}"

def make_path(color, data):
    return f'<path stroke="{color}" d="{data}" />'

def convert_image_to_svg(image_path):
    # Load image.
    # TODO: Handle the case where there is more than one image in this file
    # (like an ICO or CUR).
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    pixels = image.load()

    # Store colors and their coordinates
    colors = {}
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            color = get_color(r, g, b, a)
            if color not in colors:
                colors[color] = []
            
            colors[color].append(Point(x, y))

    # Create SVG paths
    svg_output = ""
    for color, coordinates in colors.items():
        svg_color = color
        if svg_color is None:
            continue

        paths = []
        path_origin_point = None
        run_width = 1

        for coord in coordinates:
            if path_origin_point and coord.y == path_origin_point.y and coord.x == (path_origin_point.x + run_width):
                run_width += 1
            else:
                if path_origin_point:
                    pixel_run = create_pixel_run_path(path_origin_point, run_width)
                    paths.append(pixel_run)
                path_origin_point = coord
                run_width = 1

        pixel_run = create_pixel_run_path(path_origin_point, run_width)
        paths.append(pixel_run)
        svg_output += make_path(svg_color, "".join(paths))

    # Final SVG
    svg_output = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -0.5 {width} {height}" shape-rendering="crispEdges">\n{svg_output}</svg>'
    return svg_output

# MAKE THE CONVERTER USABLE FROM THE COMMAND LINE.
def main():
    # DEFINE THE COMMAND LINE PARSER.
    parser = argparse.ArgumentParser(description='Convert a raster image to SVG.')
    parser.add_argument(
        'input', 
        help = 'Input image path. Can be any image format that Pillow supports.')
    parser.add_argument(
        '--output', 
        required = False, 
        help = 'Output SVG path. If not included, the output path fill be the input path plus an SVG extension.')

    # CONVERT THE REQUESTED IMAGE.
    args = parser.parse_args()
    svg_content = convert_image_to_svg(args.input)
    if args.output is None:
        args.output = f'{args.input}.svg'
    with open(args.output, "w") as f:
        f.write(svg_content)
# Check the case when the script is run interactively.
# If it's installed from PyPI, this shouldn't be needed,
# but I'll keep it in in case it is run directly.
if __name__ == "__main__":
    main()
