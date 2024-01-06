# Copyright 2021 Casey Devet
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

################################################################################
#                               GLOBAL VARIABLES
################################################################################

import math
import pygame

vector = pygame.Vector2

################################################################################
#                                 SPRITE CLASS
################################################################################

class Sprite (pygame.sprite.DirtySprite):
    '''
    A Sprite represents an image that moves around the screen in a game.

    Sprite objects store the following information necessary for drawing these
    images on the screen:
    * The position of the sprite on the screen using coordinates
    * The direction that the sprite is pointing using an angle measured
      counterclockwise from the positive x-axis.

    Attributes and methods are provided for the following:
    * Moving and turning the sprite
    * Animating the sprite
    '''

    def __init__ (self, image, position=(0,0), direction=0, speed=0, rotates=True):
        '''
        Create a Sprite object with the provided file as its image
        '''

        pygame.sprite.Sprite.__init__(self)

        # Handle the image
        if not isinstance(image, pygame.Surface):
            raise ValueError("The image must be a Surface object!") from None
        self._original = image
        self._image = image
        
        # Attributes that hold the position, direction and speed
        self._rotates = bool(rotates)
        self.position = vector(position)
        self.direction = float(direction)
        self.speed = float(speed)

        # Attributes for DirtySprite
        self.dirty = 1
        self.blendmode = 0
        self.source_rect = None
        self.visible = 1
        self._layer = 0


    ### .image and .rect properties need in sprites
    @property
    def image (self):
        '''
        The Surface that the sprite represents.  This Surface is
        used when blitting the sprite.
        '''

        return self._image

    @image.setter
    def image (self, new_image):

        self._original = new_image
        self.direction = self._dir

    
    @property
    def rect (self):
        '''
        The Rect containing the size and position of the sprite.
        This Rect is used when blitting the sprite.
        
        This property is readonly.
        '''

        return self._image.get_rect(topleft=self._pos)


    ### Size Properties

    @property
    def size (self):
        '''
        The size (width, height) of the sprite's image.
        
        This property is readonly.
        '''

        return tuple(self._image.get_size())

    @property
    def width (self):
        '''
        The width of the sprite's image.
        
        This property is readonly.
        '''

        return self._image.get_width()

    @property
    def height (self):
        '''
        The height of the sprite's image.
        
        This property is readonly.
        '''

        return self._image.get_height()


    ### Position Methods

    @property
    def position (self):
        '''
        The current the position of the sprite on the screen.
        '''

        return tuple(self._pos)

    @position.setter
    def position (self, new_position):

        try:
            self._pos = vector(new_position)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def topleft (self):
        '''
        The coordinates of the top left corner of the sprite.
        '''

        return tuple(self._pos)

    @top_left.setter
    def topleft (self, new_top_left):

        try:
            self._pos = vector(new_top_left)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def bottomleft (self):
        '''
        The coordinates of the bottom left corner of the sprite.
        '''

        return tuple(self._pos + vector(0, self.height))

    @bottom_left.setter
    def bottomleft (self, new_bottom_left):

        try:
            self._pos = vector(new_bottom_left) - vector(0, self.height)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def topright (self):
        '''
        The coordinates of the top right corner of the sprite.
        '''

        return tuple(self._pos + vector(self.width, 0))

    @top_right.setter
    def topright (self, new_top_right):

        try:
            self._pos = vector(new_top_right) - vector(self.width, 0)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def bottomright (self):
        '''
        The coordinates of the bottom right corner of the sprite.
        '''

        return tuple(self._pos + vector(self.size))

    @bottom_right.setter
    def bottomright (self, new_bottom_right):

        try:
            self._pos = vector(new_bottom_right) - vector(self.size)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def midleft (self):
        '''
        The coordinates of the middle of the left edge of the sprite.
        '''

        return tuple(self._pos + vector(0, self.height / 2))

    @mid_left.setter
    def midleft (self, new_mid_left):

        try:
            self._pos = vector(new_mid_left) - vector(0, self.height / 2)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def midright (self):
        '''
        The coordinates of the middle of the right edge of the sprite.
        '''

        return tuple(self._pos + vector(self.width, self.height / 2))

    @mid_right.setter
    def midright (self, new_mid_right):

        try:
            self._pos = vector(new_mid_right) - vector(self.width, self.height / 2)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def midtop (self):
        '''
        The coordinates of the middle of the top edge of the sprite.
        '''

        return tuple(self._pos + vector(self.width / 2, 0))

    @mid_top.setter
    def midtop (self, new_mid_top):

        try:
            self._pos = vector(new_mid_top) - vector(self.width / 2, 0)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def midbottom (self):
        '''
        The coordinates of the middle of the bottom edge of the sprite.
        '''

        return tuple(self._pos + vector(self.width / 2, self.height))

    @mid_bottom.setter
    def midbottom (self, new_mid_bottom):

        try:
            self._pos = vector(new_mid_bottom) - vector(self.width / 2, self.height)
        except Exception as e:
            raise ValueError("Invalid position!") from None


    @property
    def center (self):
        '''
        The coordinates of the center of the sprite.
        '''

        return tuple(self._pos + vector(self.size) / 2)

    @center.setter
    def center (self, new_center):

        try:
            self._pos = vector(new_center) - vector(self.size) / 2
        except Exception as e:
            raise ValueError("Invalid position!") from None

    
    @property
    def x (self):
        '''
        The x-coordinate of the sprite on the screen.
        '''
        return self._pos.x

    
    @x.setter
    def x (self, new_x):

        try:
            self._pos.x = new_x
        except:
            raise ValueError("Invalid x-coordinate!") from None

    
    @property
    def y (self):
        '''
        The y-coordinate of the sprite on the screen.
        '''
        return self._pos.y

    
    @y.setter
    def y (self, new_y):

        try:
            self._pos.y = new_y
        except:
            raise ValueError("Invalid y-coordinate!") from None

    
    @property
    def left (self):
        '''
        The x-coordinate of the left side of the sprite.
        '''
        return self._pos.x

    
    @left.setter
    def left (self, new_left):

        try:
            self._pos.x = new_left
        except:
            raise ValueError("Invalid x-coordinate!") from None

    
    @property
    def right (self):
        '''
        The x-coordinate of the right side of the sprite.
        '''

        return self._pos.x + self.width

    @right.setter
    def right (self, new_right):

        try:
            self._pos.x = new_right - self.width
        except:
            raise ValueError("Invalid x-coordinate!")

    
    @property
    def centerx (self):
        '''
        The x-coordinate of the center of the sprite.
        '''

        return self._pos.x + self.width / 2

    @center_x.setter
    def centerx (self, new_center_x):

        try:
            self._pos.x = new_center_x - self.width / 2
        except:
            raise ValueError("Invalid x-coordinate!")

    
    @property
    def top (self):
        '''
        The y-coordinate of the top of the sprite.
        '''

        return self._pos.y

    @top.setter
    def top (self, new_top):

        try:
            self._pos.y = new_top
        except:
            raise ValueError("Invalid y-coordinate!")

    
    @property
    def bottom (self):
        '''
        The y-coordinate of the bottom of the sprite.
        '''

        return self._pos.y + self.height

    @bottom.setter
    def bottom (self, new_bottom):

        try:
            self._pos.y = new_bottom - self.height
        except:
            raise ValueError("Invalid y-coordinate!")

    
    @property
    def centery (self):
        '''
        The y-coordinate of the center of the sprite.
        '''

        return self._pos.y + self.height / 2

    @center_y.setter
    def centery (self, new_center_y):

        try:
            self._pos.y = new_center_y - self.height / 2
        except:
            raise ValueError("Invalid y-coordinate!")


    ### Movement Methods

    def move_forward (self, distance):
        '''
        Move the sprite by the given `distance` in the direction it is 
        currently pointing.
        '''

        self._pos = self._pos + distance * self._delta


    def move_backward (self, distance):
        '''
        Move the sprite by the given `distance` in the opposite of the
        direction it is currently pointing.
        '''

        self._pos = self._pos - distance * self._delta


    ### Direction and Rotation
       

    @property
    def direction (self):
        '''
        The current direction that the sprite is pointing.

        The direction is an angle (in degrees) counterclockwise from the
        positive x-axis.  Here are some important directions:
         - 0 degrees is directly to the right
         - 90 degrees is directly up
         - 180 degrees is directly to the left
         - 270 degrees is directly down
        '''

        return self._dir

    @direction.setter
    def direction (self, new_direction):

        # Ensure that the direction is a number
        try:
            self._dir = float(new_direction)
        except:
            raise ValueError("The direction must be a number!")

        # Ensure that the direction is between 0 and 360
        self._dir %= 360

        # Create a 2D vector that contains the amount that the x-coordinate
        # and y-coordinate change if the sprite moves forward 1 pixel in this
        # direction
        self._delta = vector(1, 0)
        self._delta.rotate_ip(-self._dir)

        # Rotate the image about its center
        old_offset = vector(self._image.get_size()) / 2
        angle = self._dir if self._rotates else 0
        self._image = pygame.transform.rotate(self._original, angle)
        new_offset = vector(self._image.get_size()) / 2
        self._pos = self._pos + old_offset - new_offset


    def turn_left (self, angle):
        '''
        Turn the sprite left (counterclockwise) by the given `angle`.
        '''

        self.direction += angle


    def turn_right (self, angle):
        '''
        Turn the sprite right (clockwise) by the given `angle`.
        '''

        self.direction -= angle

    @property
    def rotates (self):
        '''
        Whether or not the image rotates when the sprite changes direction.
        '''

        return self._rotates

    @rotates.setter
    def rotates (self, new_rotates):

        self._rotates = bool(new_rotates)
        self.direction = self._dir


    @property
    def speed (self):
        '''
        The distance that the sprite moves forward by on each update.
        '''

        return self._speed

    @speed.setter
    def speed (self, new_speed):

        try:
            self._speed = float(new_speed)
        except:
            raise ValueError("Invalid speed!")


    @property
    def layer (self):
        '''
        The layer number to draw the sprite on.  Higher layers are drawn on top.
        '''

        return self._layer

    @layer.setter
    def layer (self, new_layer):

        self._layer = new_layer


    def contains_point (self, x, y=None):
        '''
        Determine whether or not a point is contained within this sprite's
        rectangle.
        '''

        try:
            if y is None:
                point = vector(x)
            else:
                point = vector(x, y)
        except:
            raise ValueError("Invalid point!") from None

        return self.rect.collidepoint(point)


    def mask_contains_point (self, x, y=None):
        '''
        Determine whether or not a point is contained within this sprite's
        mask.
        '''

        try:
            if y is None:
                point = vector(x)
            else:
                point = vector(x, y)
        except:
            raise ValueError("Invalid point!") from None

        if self.rect.collidepoint(point):
            mask = pygame.mask.from_surface(self.image)
            return bool(mask.get_at(point - self._pos))
        return False


    ### Update Method

    def update (self):
        '''
        Update the sprite in preparation to draw the next frame.

        This method should generally not be called explicitly, but will be called
        by the event loop if the sprite is on the active screen.
        '''

        # Update the sprite's position
        self._pos = self._pos + self._speed * self._delta
        


    def draw (self, surface):
        '''
        Draw the sprite on the given Surface object.
        '''

        surface.blit(self.image, self.rect)


# What is included when importing *
__all__ = [
    "Sprite"
]
