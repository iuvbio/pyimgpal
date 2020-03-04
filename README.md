pyimgpal
===

A simple script to create a 16 colour scheme from an image.

About
---

The idea (and a lot of the code) were taken from [this](http://charlesleifer.com/blog/suffering-for-fashion-a-glimpse-into-my-linux-theming-toolchain/) blog post from Charles Leifer, so most of the credit goes to him.

By default, the script creates a colour scheme for the terminal which means it is based on the eight primary colours black, red, green, yellow, blue, magenta, cyan, and grey. The 16 final colours are two variations of each, one "normal" and one for emphasis. The normal colours are chosen from the image as the ones closest to each of the primary colours and the emphasis colours are the next best match or the same, if no other match could be found.

```bash
# rgb values for the canonical colours

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
```
