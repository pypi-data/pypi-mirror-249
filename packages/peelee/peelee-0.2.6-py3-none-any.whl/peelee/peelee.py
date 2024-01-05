#!/usr/bin/env python3
"""peelee is one module to generate random palette and colors.
"""
import colorsys
import getopt
import random
import sys
from enum import Enum


class ColorName(Enum):
    """Color names"""

    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    CYAN = 4
    VIOLET = 5


def fg(hex_color, msg):
    """Decorate msg with hex_color in foreground."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[38;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def bg(hex_color, msg):
    """Decorate msg with hex_color in background."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[48;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def hex2rgb(hex_color):
    """ "Convert."""
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def hex2hls(hex_color):
    """ "Convert."""
    rgb_color = hex2rgb(hex_color)
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(
        normalized_rgb[0], normalized_rgb[1], normalized_rgb[2]
    )
    return hls_color


def hls2hex(hls_color):
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert."""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def get_scheme_colors(hex_color, n_colors=7):
    """
    Generate a list of n_colors triadic colors based on the given hex_color.

    Args:
        hex_color (str): The hexadecimal color code.
        n_colors (int): The number of triadic colors to generate. Default is 7.

    Returns:
        list: A list of n_colors triadic color codes.

    Raises:
        AssertionError: If hex_color is None or n_colors is not an integer greater than 0.
    """
    assert hex_color is not None, "Invalid argument: hex_color is None."
    assert (
        n_colors is not None and isinstance(n_colors, int) and n_colors > 0
    ), f"Invalid argument: n_colors = {n_colors}"
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in range(0, 360, 360 // n_colors):
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    return [hls2hex(hls_color) for hls_color in triadic_colors][0:n_colors]


def padding(num, target_length=2):
    """
    Padding left for number to make it's string format length reaches the target length.

    This is mainly used to construct valid hex color number in R,G,B
    position. Example, if the given num is a hex number 0xf and the
    target length is 2, then the padding result is 0f.
    """
    str_num = str(num)
    target_length = target_length if target_length and target_length > 2 else 2
    if str_num.startswith("0x"):
        str_num = str_num[2:]
    if len(str_num) < target_length:
        str_num = (
            f"{''.join(['0' for _ in range(target_length - len(str_num))])}{str_num}"
        )
    return str_num


def lighter(base_color, n_color):
    """Given base color, return 'n' color hex codes from base color to lightest
    color."""
    color_rgb = tuple(int(base_color[1:][i : i + 2], 16) for i in (0, 2, 4))

    # to avoid the lighter color is becoming other colors, use the same _gap
    # for r,g,b. _gap is the distance from the max value of r,g,b to 255.
    # when create lighter color, the increasement steps of r,g,b should be the
    # same. if use 255 as the max value, then those smaller values in r,g,b
    # will be becominig bigger than others when it's close to white. And
    # finally, the color is becoming other colors.
    # this is one very important fix.
    _max = max(color_rgb)
    _gap = 255 - _max
    color_rgb_ligher = tuple(
        list(range(color, color + _gap, _gap // n_color))[0:n_color]
        for color in color_rgb
    )

    lighter_colors = [
        f"#{''.join(tuple(padding(hex(color_ligher[index])) for color_ligher in color_rgb_ligher))}"
        for index in range(0, n_color)
    ]

    return lighter_colors


def create_hsl_for_lighter(hsl_value, max_hsl_value, total):
    """Create a list of values of HSL for lighter colors generation."""
    # calculate lightness of the lighter colors - convert the decimal to integer, get difference from the lightness of the base color to the maximum lightness(1) and divide by n_color
    _decimal_length = len(str(hsl_value)[2:]) if hsl_value > 0 else 16
    _max = int(10**_decimal_length * max_hsl_value)
    _min = int(hsl_value * _max)

    # cannot be lighter than if already too light
    if (_max - _min) // total == 0:
        print(
            f"Cannot be lighter than if already too light. {hsl_value} is too light(_max={_max}, _min={_min}, total={total})."
        )
        return [hsl_value for _ in range(total)]

    # get the lighter lightness from the base color to the maximum lightness(1) by divide the lightness with n_color
    hsl_values = list(range(_min, _max, (_max - _min) // total))[0:total]
    # print(hsl_value, hsl_values, _min, _max, _decimal_length)
    return [l / _max for l in hsl_values]


def saturater(base_color, n_color, max_saturation=0.8, max_lightness=0.8):
    """Convert hex to hsl and generate n_color colors by divide the lightness with n_color."""
    _hls = hex2hls(base_color)
    lightness = _hls[1]
    saturation = _hls[2]
    if lightness > max_lightness or saturation > max_saturation:
        return [base_color for _ in range(n_color)]

    lightness_list = create_hsl_for_lighter(lightness, max_lightness, n_color)
    saturation_list = []
    # don't apply saturation for black or dark gray
    if lightness < 0.01:
        saturation_list = [0 for _ in range(n_color)]
    else:
        saturation_list = create_hsl_for_lighter(saturation, max_saturation, n_color)

    # the below code blocked is generated by CodeWhisperer.
    lighter_colors = [
        hls2hex((_hls[0], lightness_list[index], saturation_list[index]))
        for index in range(0, n_color)
    ]
    # insert the base color to the lighter_colors list if it's not in the list
    # if inserted the base color, then remove the lightest color
    if base_color not in lighter_colors:
        lighter_colors.insert(0, base_color)
        return lighter_colors[0:-1]

    return lighter_colors


def set_saturation(hex_color, saturation):
    """Set saturation."""
    hls_color = hex2hls(hex_color)
    new_hls_color = (hls_color[0], hls_color[1], saturation)
    return hls2hex(new_hls_color)


def generate_random_colors(
    min_color=0, max_color=231, colors_total=7, color_gradations=24, saturation=None
):
    """
    Generate random color hex codes.

    Firstly, it will generate random integer from min_color (0-(255 - gradations_total - 1)) to max_color (0-(255 - gradations_total)).
    The max_color should be less than (255 - gradations_total) because it needs the room to generate lighter colors.

    To generate darker colors, use smaller value for max_color.
    To generate ligher colors, use bigger value for min_color.

    It's recommended to use default values.
    If you want to make change, please make sure what you are doing.

    Secondly, it will generate 'gradations_total' different hex color codes from base color to the lightest color.

        min_color - minimum color code. default: 0.
        max_color - maximum color code. default: 254 (cannot be bigger value).
        base_colors_total - how many base colors to generate. default: 7.
        gradations_total - how many lighter colors to generate. default: 24.

    Retrun:
        Generated random base colors and all lighter colors of each base color.
        The returned value is a two-dimention list. First dimention length is the value of base_colors_total. Second dimention length is gradations_total.
    """
    if color_gradations < 0 or color_gradations > 253:
        color_gradations = 24
    if min_color < 0 or min_color > (255 - color_gradations - 1):
        min_color = 0
    if max_color <= min_color or max_color >= (255 - color_gradations):
        max_color = 255 - color_gradations - 1

    random_color = generate_random_hex_color_code(
        min_color, max_color, saturation=saturation
    )
    base_colors = generate_base_colors(random_color, colors_total)

    random_colors_list = []
    for base_color in base_colors:
        hls_base_color = hex2hls(base_color)
        # if very dark color, then use saturater to get lighter colors
        if hls_base_color[1] < 0.1:
            print(f"{base_color}({hex2hls(base_color)}) - to call saturater")
            lighter_colors = saturater(base_color, color_gradations)
        else:
            lighter_colors = lighter(base_color, color_gradations)
        random_colors_list.append(lighter_colors)

    return random_colors_list


def generate_random_hex_color_code(
    min_color, max_color, color_name: ColorName = None, saturation=None
):
    """
    Generates a list of base colors based on the given minimum and maximum
    color values and the total number of colors.

    Parameters:
    - min_color (int): The minimum value of the color range.
    - max_color (int): The maximum value of the color range.
    - total (int): The total number of base colors to generate.

    Returns:
    - base_colors (list): A list of base colors generated based on the given parameters.
    """
    random_hex_color_code = "#"
    rgb = []

    # Old solution - only used for dark colors which needs dynamic colors.
    # By new solution, the dark color might be always the black color since
    # the max value is not big enough to have room to generate random colors
    # after divide by 12.
    # The old solution is usually used for workbench colors.
    if max_color <= 30:
        for index in range(0, 3):
            random_int = random.randint(min_color, max_color)
            _random_color = padding(hex(random_int))
            rgb.append(_random_color)
    else:
        # New solution - 2023.12.19(Stockholm.Kungsängen.TibbleTorg) -in this
        # way, the generated colors are in the 'best' range and the theme
        # effection will be stable. The 'best' range will generate colors
        # that are comfortable for human eyes. E.g. #3c6464 or rgb(60,100,
        # 100). This is usually used for syntax(token) colors.
        diff = max_color - min_color
        step = diff // 12
        for index in range(1, 12, 4):
            random_int = random.randint(
                min_color + (index * step), min_color + ((index + 2) * step)
            )
            _random_color = padding(hex(random_int))
            rgb.append(_random_color)

        # By new solution, in default, the values of R,G,B is increased.
        # To generate the target color, need to swap the values of R,G,B
        if color_name == ColorName.RED:
            rgb = swap_list(rgb, 0, 2)
        elif color_name == ColorName.GREEN:
            rgb = swap_list(rgb, 1, 2)
        elif color_name == ColorName.YELLOW:
            rgb = swap_list(rgb, 0, 2)
            rgb[1] = rgb[0]
        elif color_name == ColorName.CYAN:
            rgb[1] = rgb[2]
        elif color_name == ColorName.VIOLET:
            rgb[0] = rgb[2]

    random_hex_color = random_hex_color_code + "".join(rgb)
    if saturation is not None:
        random_hex_color = set_saturation(random_hex_color, saturation)
    return random_hex_color


def swap_list(_list, _from_index, _to_index):
    """Swap items in _from_index and _to_index in the list."""
    _tmp = _list[_from_index]
    _list[_from_index] = _list[_to_index]
    _list[_to_index] = _tmp
    return _list


def generate_base_colors(hex_color_code, total):
    """Generate base colors by the given hex color code and total number."""
    print(hex_color_code)

    base_colors = get_scheme_colors(hex_color_code, total)[0:total]
    return base_colors


class Palette:
    """Generate palette colors."""

    def __init__(
        self,
        gradations_total=60,
        dark_color_gradations_total=60,
        color_min=120,
        color_max=180,
        colors_total=7,
        color_saturation=0.35,
        dark_color_min=15,
        dark_color_max=20,
        dark_colors_total=7,
        dark_color_saturation=0.2,
        dark_colors=None,
    ):
        """
        Generate random palette.
        Parameters:
            base_colors_total - how many base colors to generate. default: 5.
            gradations_total - how many lighter colors to generate. default: 6.
            general_max_color - maximum color code. default: 200.
            dark_max_color - maximum color code. default: 30.
            dark_colors_total - how many dark colors to generate. default: 5.
            dark_base_colors - base colors for dark theme.
            Note: (1) the value of dark_base_colors is a list.
            (2) the value of dark_base_colors will not be used as color of
             pelette, only their lighter colors will be used.
            (3) if this parameter is given, then dark_colors_total will be ignored.
        """
        # random colors are used for sections, components, and pieces
        self.colors_total = colors_total
        self.gradations_total = gradations_total
        self.dark_color_gradations_total = dark_color_gradations_total
        self.color_min = color_min
        self.color_max = color_max
        self.color_saturation = color_saturation
        self.dark_min_color = dark_color_min
        self.dark_max_color = dark_color_max
        self.dark_colors_total = dark_colors_total
        self.dark_colors_saturation = dark_color_saturation
        self.dark_base_colors = dark_colors

    def generate_palette_colors(self):
        """
        Generate random palette.

        6 group base colors: 5 base colors + dark gray color. echo base
        color has 6 different colors from dark to light. placeholders
        are from light to dark, so need to reverse the order.
        """
        random_colors_list = generate_random_colors(
            min_color=self.color_min,
            max_color=self.color_max,
            colors_total=self.colors_total,
            color_gradations=self.gradations_total,
            saturation=self.color_saturation,
        )

        # dark colors are generated by default and used as base color in theme
        if (
            self.dark_base_colors
            and isinstance(self.dark_base_colors, list)
            and len(self.dark_base_colors) > 0
        ):
            dark_colors = [
                lighter(_base_color, self.dark_color_gradations_total)
                for _base_color in self.dark_base_colors
            ]
        else:
            dark_colors = generate_random_colors(
                min_color=self.dark_min_color,
                max_color=self.dark_max_color,
                colors_total=self.dark_colors_total,
                color_gradations=self.dark_color_gradations_total,
                saturation=self.dark_colors_saturation,
            )

        random_colors_list.extend(dark_colors)
        for r_colors in random_colors_list:
            r_colors.reverse()
        return [color for r_colors in random_colors_list for color in r_colors]

    def generate_palette(self):
        """
        Generate palette content.

        Palette contains a list of colors. Each color is a pair of color
        name and color code.
        The format is "C_[base color sequence]_[colormap sequence]".

        For example, "C_1_1":"#8f67ff".

        Note:
        The 'base color sequence' starts from 1 to base_colors_total (not
        included)
        The 'colormap sequence' starts from 0 to gradations_total (not
        included)
        When "colormap sequence" is 0, then it represents the lightest color.

        One continuous colormap is for one base color and consists of a
        group of colors from lightest color to the base color.

        Return:
        A list of palette colors.
        """
        palette_color_codes = self.generate_palette_colors()
        color_sequence = 1
        sub_color_sequence = 0
        palette_colors = {}
        _gradations_total = self.gradations_total
        for index, color in enumerate(palette_color_codes):
            sub_color_sequence = index % (self.gradations_total)
            # the remaining colors codes belong to dark colors
            if color_sequence > self.colors_total:
                _gradations_total = self.dark_color_gradations_total
                sub_color_sequence = (
                    index - (self.colors_total * self.gradations_total)
                ) % (self.dark_color_gradations_total)
            str_base_color_sequence = padding(
                color_sequence, max(len(str(self.colors_total)), 2)
            )
            str_colormap_sequence = padding(
                sub_color_sequence, max(len(str(_gradations_total)), 2)
            )
            color_name = f"C_{str_base_color_sequence}_{str_colormap_sequence}"
            palette_colors[color_name] = color
            if sub_color_sequence == _gradations_total - 1:
                color_sequence += 1
        return palette_colors


def generate_palette():
    """Generate palette colors."""
    return Palette().generate_palette()


def main():
    """Test."""
    opts, _ = getopt.getopt(
        sys.argv[1:],
        "b:B:d:g:G:m:M:",
        [
            "--base_colors_total=",
            "--dark_base_colors=",
            "--gradations_total=",
            "--dark_color_gradations_total=",
            "--general_max_color=",
            "--dark_max_color=",
        ],
    )
    base_colors_total = 5
    gradations_total = 6
    dark_color_gradations_total = 6
    general_max_color = 200
    dark_max_color = 30
    dark_colors_total = 5
    dark_base_colors = None
    for option, value in opts:
        if option in ("-b", "--base_colors_total"):
            base_colors_total = int(value)
        if option in ("-B", "--dark_base_colors"):
            dark_base_colors = value.split(",")
        if option in ("-d", "--dark_colors_total"):
            dark_colors_total = int(value)
        if option in ("-g", "--gradations_total"):
            gradations_total = int(value)
        if option in ("-G", "--dark_color_gradations_total"):
            dark_color_gradations_total = int(value)
        if option in ("-m", "--general_max_color"):
            general_max_color = int(value)
        if option in ("-M", "--dark_max_color"):
            dark_max_color = int(value)
    palette = Palette(
        colors_total=base_colors_total,
        gradations_total=gradations_total,
        dark_color_gradations_total=dark_color_gradations_total,
        color_min=0,
        color_max=general_max_color,
        dark_color_min=0,
        dark_color_max=dark_max_color,
        dark_colors_total=dark_colors_total,
        dark_colors=dark_base_colors,
    )
    for color_id, color_hex in palette.generate_palette().items():
        print(bg(color_hex, f"{color_id}({color_hex})"))


if __name__ == "__main__":
    main()
