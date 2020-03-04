#!/usr/bin/env python
"""Converts an image to a 16 colour scheme.

Attribution: Many parts originally authored by <Charles Leifer https://github.com/coleifer>

Usage: pyimgpal [OPTIONS] IMAGE_PATH

Options:
  -o, --outfile FILENAME
  -f, --format [rgb|hex]
  --adjusted / --unadjusted  [default: True]
  -p, --add-prefix           [default: False]
  -nl, --new-lines           [default: False]
  --help                     Show this message and exit.
"""
import argparse
import click
import colorsys
import heapq
import math

from PIL import Image


parser = argparse.ArgumentParser(
    description="This script reads in an image and returns a 16 color palette."
)

canonical = [
    (0, 0, 0),  # Black
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (255, 255, 0),  # Yellow
    (0, 0, 255),  # Blue
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (192, 192, 192),  # Light gray

    (64, 64, 64),  # Dark gray
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (255, 255, 0),  # Yellow
    (0, 0, 255),  # Blue
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 255),  # White
]


def isolate_colors(filename, ncolors):
    img = Image.open(filename)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.convert('P', palette=Image.ADAPTIVE, colors=ncolors)
    img = img.convert('RGB')
    return sorted(img.getcolors(ncolors), reverse=True)


# count_color is a sorted (desc) list of: [(pixel count, (r, g, b)), ...]
# rollup is the distance heuristic, arrived at by fiddling til it looked ok
def dedupe(count_color, rollup=10):
    result = {}
    for count, rgb in count_color:
        if rgb in result:
            result[rgb] += count
        else:
            for rrgb in result:
                dist = euclidean_dist(rrgb, rgb)
                if dist < rollup:
                    result[rrgb] += count
                    break
            else:
                result[rgb] = count

    return sorted([(count, color) for color, count in result.items()],
                  reverse=True)


def euclidean_dist(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(3)))


def get_xcolors(colors, substitution_distance=20):
    results = []
    for crgb in canonical:
        distances = []
        for rgb in colors:
            distance = euclidean_dist(crgb, rgb)
            heapq.heappush(distances, (distance, rgb))

        # First, try the closest RGB match.
        best = heapq.nsmallest(1, distances)[0][1]
        if best not in results:
            results.append(best)
        else:
            # Attempt to find a substitute.
            current = 0  # Distance from best color to potential substitute.
            min_dist = None
            vals = []
            while distances and current < substitution_distance:
                dist, rgb = heapq.heappop(distances)
                vals.append(rgb)

                # Here we're keeping an eye on the distance between
                # the potential substitute color, and the original
                # "best" color.
                if min_dist is None:
                    min_dist = dist
                else:
                    current = dist - min_dist

            for rgb in vals:
                if rgb not in results:
                    # We found a substitute that isn't in use.
                    results.append(rgb)
                    break
            else:
                # No substitute found, just use the best match.
                results.append(vals[0])

    return results


def ensure_value(rgb, low, high):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 256., g / 256., b / 256.)
    v = max(min(v, high), low)
    return tuple([round(i * 256., 0) for i in colorsys.hsv_to_rgb(h, s, v)])


def to_hex(rgb):
    return "{0:02x}{1:02x}{2:02x}".format(*rgb)


@click.command()
@click.argument('image-path', type=click.Path(exists=True))
@click.option('-o', '--outfile', type=click.File('w'))
@click.option('-f', '--format', 'format_', type=click.Choice(['rgb', 'hex']), default='rgb')
@click.option('--adjusted/--unadjusted', default=True, show_default=True)
@click.option('-p', '--add-prefix', is_flag=True, show_default=True)
@click.option('-nl', '--new-lines', is_flag=True, show_default=True)
def main(image_path, outfile, format_, adjusted, add_prefix, new_lines):
    colors = isolate_colors(image_path, 50)
    colors_deduped = dedupe(colors)
    xcolors = get_xcolors([rbg for cnt, rbg in colors_deduped])
    # return the palette with black and white adjusted
    if adjusted:
        xcolors[0] = tuple(int(v) for v in ensure_value(xcolors[0], .0, .2))
        xcolors[-1] = tuple(int(v) for v in ensure_value(xcolors[-1], .8, 1.))
    if format_ == 'hex':
        xcolors = [to_hex(rgb) for rgb in xcolors]
    palette = xcolors
    if add_prefix:
        fmtsr = "rgb({0},{1},{2})" if format_ == 'rgb' else "#{0}{1}{2}{3}{4}{5}"
        palette = [fmtsr.format(*rgb) for rgb in xcolors]
    if new_lines:
        palette = "\n".join([str(color) for color in palette])

    click.echo(palette, file=outfile)
