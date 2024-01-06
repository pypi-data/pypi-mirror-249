This is a Python port of [Pixels to SVG](https://codepen.io/shshaw/pen/XbxvNj), which is itself inspired by [px2svg](https://github.com/meyerweb/px2svg). I did the Python port since Python-based scripting fits better with my workflow than JS-based scripting.

Essentially, each pixel of the original image is put into an SVG rectangle so a lowres image can be scaled without blurriness! Here's quote from [Pixels to SVG](https://codepen.io/shshaw/pen/XbxvNj):
    The image data is extracted from a canvas, and separated by color. The coordinates for each color are combined into single runs where possible to keep the path data syntax short, then merged into one path with a stroke of the color.

Just like [Pixels to SVG](https://codepen.io/shshaw/pen/XbxvNj), this works best with 8-bit images, or graphics where colors are limited and the 
dimensions are relatively small. 

If you like my projects, please consider supporting me!

<a href="https://www.buymeacoffee.com/natster" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>