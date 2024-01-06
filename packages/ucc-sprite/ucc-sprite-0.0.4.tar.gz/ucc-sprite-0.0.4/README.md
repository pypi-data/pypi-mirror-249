# UCC Sprite Class

This module provides the `Sprite` class.  It is a convenience class that implements many desireable features for Pygame sprites.

## Install the module

```
pip3 install ucc-sprite
```

## Getting Started

```
from ucc_sprite import Sprite
...
image = pygame.image.load("image.png")
my_sprite = Sprite(image)
```

You can use the `my_sprite` object as a Pygame sprite.

# Table of Contents

* [ucc\_sprite](#ucc_sprite)
  * [Sprite](#ucc_sprite.Sprite)
    * [\_\_init\_\_](#ucc_sprite.Sprite.__init__)
    * [image](#ucc_sprite.Sprite.image)
    * [rect](#ucc_sprite.Sprite.rect)
    * [size](#ucc_sprite.Sprite.size)
    * [width](#ucc_sprite.Sprite.width)
    * [height](#ucc_sprite.Sprite.height)
    * [position](#ucc_sprite.Sprite.position)
    * [top\_left](#ucc_sprite.Sprite.top_left)
    * [bottom\_left](#ucc_sprite.Sprite.bottom_left)
    * [top\_right](#ucc_sprite.Sprite.top_right)
    * [bottom\_right](#ucc_sprite.Sprite.bottom_right)
    * [mid\_left](#ucc_sprite.Sprite.mid_left)
    * [mid\_right](#ucc_sprite.Sprite.mid_right)
    * [mid\_top](#ucc_sprite.Sprite.mid_top)
    * [mid\_bottom](#ucc_sprite.Sprite.mid_bottom)
    * [center](#ucc_sprite.Sprite.center)
    * [x](#ucc_sprite.Sprite.x)
    * [y](#ucc_sprite.Sprite.y)
    * [left](#ucc_sprite.Sprite.left)
    * [right](#ucc_sprite.Sprite.right)
    * [center\_x](#ucc_sprite.Sprite.center_x)
    * [top](#ucc_sprite.Sprite.top)
    * [bottom](#ucc_sprite.Sprite.bottom)
    * [center\_y](#ucc_sprite.Sprite.center_y)
    * [move\_forward](#ucc_sprite.Sprite.move_forward)
    * [move\_backward](#ucc_sprite.Sprite.move_backward)
    * [direction](#ucc_sprite.Sprite.direction)
    * [turn\_left](#ucc_sprite.Sprite.turn_left)
    * [turn\_right](#ucc_sprite.Sprite.turn_right)
    * [rotates](#ucc_sprite.Sprite.rotates)
    * [speed](#ucc_sprite.Sprite.speed)
    * [layer](#ucc_sprite.Sprite.layer)
    * [contains\_point](#ucc_sprite.Sprite.contains_point)
    * [mask\_contains\_point](#ucc_sprite.Sprite.mask_contains_point)
    * [update](#ucc_sprite.Sprite.update)
    * [draw](#ucc_sprite.Sprite.draw)

<a id="ucc_sprite"></a>

# ucc\_sprite

<a id="ucc_sprite.Sprite"></a>

## Sprite Objects

```python
class Sprite(pygame.sprite.DirtySprite)
```

A Sprite represents an image that moves around the screen in a game.

Sprite objects store the following information necessary for drawing these
images on the screen:
* The position of the sprite on the screen using coordinates
* The direction that the sprite is pointing using an angle measured
  counterclockwise from the positive x-axis.

Attributes and methods are provided for the following:
* Moving and turning the sprite
* Animating the sprite

<a id="ucc_sprite.Sprite.__init__"></a>

#### \_\_init\_\_

```python
def __init__(image, position=(0, 0), direction=0, speed=0, rotates=True)
```

Create a Sprite object with the provided file as its image

<a id="ucc_sprite.Sprite.image"></a>

#### image

```python
@property
def image()
```

The Surface that the sprite represents.  This Surface is
used when blitting the sprite.

<a id="ucc_sprite.Sprite.rect"></a>

#### rect

```python
@property
def rect()
```

The Rect containing the size and position of the sprite.
This Rect is used when blitting the sprite.

This property is readonly.

<a id="ucc_sprite.Sprite.size"></a>

#### size

```python
@property
def size()
```

The size (width, height) of the sprite's image.

This property is readonly.

<a id="ucc_sprite.Sprite.width"></a>

#### width

```python
@property
def width()
```

The width of the sprite's image.

This property is readonly.

<a id="ucc_sprite.Sprite.height"></a>

#### height

```python
@property
def height()
```

The height of the sprite's image.

This property is readonly.

<a id="ucc_sprite.Sprite.position"></a>

#### position

```python
@property
def position()
```

The current the position of the sprite on the screen.

<a id="ucc_sprite.Sprite.top_left"></a>

#### top\_left

```python
@property
def top_left()
```

The coordinates of the top left corner of the sprite.

<a id="ucc_sprite.Sprite.bottom_left"></a>

#### bottom\_left

```python
@property
def bottom_left()
```

The coordinates of the bottom left corner of the sprite.

<a id="ucc_sprite.Sprite.top_right"></a>

#### top\_right

```python
@property
def top_right()
```

The coordinates of the top right corner of the sprite.

<a id="ucc_sprite.Sprite.bottom_right"></a>

#### bottom\_right

```python
@property
def bottom_right()
```

The coordinates of the bottom right corner of the sprite.

<a id="ucc_sprite.Sprite.mid_left"></a>

#### mid\_left

```python
@property
def mid_left()
```

The coordinates of the middle of the left edge of the sprite.

<a id="ucc_sprite.Sprite.mid_right"></a>

#### mid\_right

```python
@property
def mid_right()
```

The coordinates of the middle of the right edge of the sprite.

<a id="ucc_sprite.Sprite.mid_top"></a>

#### mid\_top

```python
@property
def mid_top()
```

The coordinates of the middle of the top edge of the sprite.

<a id="ucc_sprite.Sprite.mid_bottom"></a>

#### mid\_bottom

```python
@property
def mid_bottom()
```

The coordinates of the middle of the bottom edge of the sprite.

<a id="ucc_sprite.Sprite.center"></a>

#### center

```python
@property
def center()
```

The coordinates of the center of the sprite.

<a id="ucc_sprite.Sprite.x"></a>

#### x

```python
@property
def x()
```

The x-coordinate of the sprite on the screen.

<a id="ucc_sprite.Sprite.y"></a>

#### y

```python
@property
def y()
```

The y-coordinate of the sprite on the screen.

<a id="ucc_sprite.Sprite.left"></a>

#### left

```python
@property
def left()
```

The x-coordinate of the left side of the sprite.

<a id="ucc_sprite.Sprite.right"></a>

#### right

```python
@property
def right()
```

The x-coordinate of the right side of the sprite.

<a id="ucc_sprite.Sprite.center_x"></a>

#### center\_x

```python
@property
def center_x()
```

The x-coordinate of the center of the sprite.

<a id="ucc_sprite.Sprite.top"></a>

#### top

```python
@property
def top()
```

The y-coordinate of the top of the sprite.

<a id="ucc_sprite.Sprite.bottom"></a>

#### bottom

```python
@property
def bottom()
```

The y-coordinate of the bottom of the sprite.

<a id="ucc_sprite.Sprite.center_y"></a>

#### center\_y

```python
@property
def center_y()
```

The y-coordinate of the center of the sprite.

<a id="ucc_sprite.Sprite.move_forward"></a>

#### move\_forward

```python
def move_forward(distance)
```

Move the sprite by the given `distance` in the direction it is 
currently pointing.

<a id="ucc_sprite.Sprite.move_backward"></a>

#### move\_backward

```python
def move_backward(distance)
```

Move the sprite by the given `distance` in the opposite of the
direction it is currently pointing.

<a id="ucc_sprite.Sprite.direction"></a>

#### direction

```python
@property
def direction()
```

The current direction that the sprite is pointing.

The direction is an angle (in degrees) counterclockwise from the
positive x-axis.  Here are some important directions:
 - 0 degrees is directly to the right
 - 90 degrees is directly up
 - 180 degrees is directly to the left
 - 270 degrees is directly down

<a id="ucc_sprite.Sprite.turn_left"></a>

#### turn\_left

```python
def turn_left(angle)
```

Turn the sprite left (counterclockwise) by the given `angle`.

<a id="ucc_sprite.Sprite.turn_right"></a>

#### turn\_right

```python
def turn_right(angle)
```

Turn the sprite right (clockwise) by the given `angle`.

<a id="ucc_sprite.Sprite.rotates"></a>

#### rotates

```python
@property
def rotates()
```

Whether or not the image rotates when the sprite changes direction.

<a id="ucc_sprite.Sprite.speed"></a>

#### speed

```python
@property
def speed()
```

The distance that the sprite moves forward by on each update.

<a id="ucc_sprite.Sprite.layer"></a>

#### layer

```python
@property
def layer()
```

The layer number to draw the sprite on.  Higher layers are drawn on top.

<a id="ucc_sprite.Sprite.contains_point"></a>

#### contains\_point

```python
def contains_point(x, y=None)
```

Determine whether or not a point is contained within this sprite's
rectangle.

<a id="ucc_sprite.Sprite.mask_contains_point"></a>

#### mask\_contains\_point

```python
def mask_contains_point(x, y=None)
```

Determine whether or not a point is contained within this sprite's
mask.

<a id="ucc_sprite.Sprite.update"></a>

#### update

```python
def update()
```

Update the sprite in preparation to draw the next frame.

This method should generally not be called explicitly, but will be called
by the event loop if the sprite is on the active screen.

<a id="ucc_sprite.Sprite.draw"></a>

#### draw

```python
def draw(surface)
```

Draw the sprite on the given Surface object.

