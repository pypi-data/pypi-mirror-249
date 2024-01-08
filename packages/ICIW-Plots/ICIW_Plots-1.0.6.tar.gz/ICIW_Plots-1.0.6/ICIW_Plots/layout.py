import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import Divider, Size


def make_square_ax(fig, left_h, bottom_v, ax_width):
    fig_width, fig_height = fig.get_size_inches()

    if ax_width + left_h >= fig_width:
        raise ValueError("Axes width exceeds figure width")
    if ax_width + bottom_v >= fig_height:
        raise ValueError("Axes height exceeds figure height")

    top_v = fig_height - ax_width - bottom_v
    right_h = fig_width - ax_width - left_h
    h = [Size.Fixed(left_h), Size.Scaled(1), Size.Fixed(right_h)]
    v = [Size.Fixed(bottom_v), Size.Scaled(1), Size.Fixed(top_v)]
    div = Divider(fig, (0.0, 0.0, 1.0, 1.0), h, v, aspect=False)
    ax = fig.add_axes(div.get_position(), axes_locator=div.new_locator(nx=1, ny=1))
    return ax
