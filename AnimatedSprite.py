from sdl2 import (SDL_Rect)
from Sprite import Sprite
from Globals import (game_globals)

class AnimatedSprite(Sprite):
    def __init__(self, graphics, file_path, src_x, src_y, width, height, pos_x, pos_y, time_to_update):
        super(AnimatedSprite, self).__init__(graphics, file_path, src_x, src_y, width, height, pos_x, pos_y) 
        self._frame_index = 0
        self._time_to_update = time_to_update
        self._time_elapsed = 0
        self._visible = True 
        self._current_animation_once = False 
        self._current_animation = ""
        self._animations = {}
        self._offsets = {}

    def addAnimation(self, frames, x, y, name, width, height, offset):
        rects = []
        for i in range(0, frames):
            rects.append(SDL_Rect((i + x) * width, y, width, height))
        
        self._animations[name] = rects
        self._offsets[name] = offset
    
    def resetAnimation(self):
        self._animations.clear()
        self._offsets.clear()
    
    def playAnimation(self, animation, once=False):
        self._current_animation_once = once
        if self._current_animation != animation:
            self._current_animation = animation
            self._frame_index = 0

    def setVisible(self, visible):
        self._visible = visible

    def stopAnimation(self):
        self._frame_index = 0
        self.animationDone(self._current_animation) 

    def updateAnimation(self, elapsed_time):
        self.updateSprite()

        self._time_elapsed += elapsed_time
        if self._time_elapsed > self._time_to_update:
            self._time_elapsed -= self._time_to_update
            if self._frame_index < len(self._animations[self._current_animation])-1:
                self._frame_index += 1
            else:
                if self._current_animation_once:
                    self.setVisible(False)
                self._frame_index = 0
                self.animationDone(self._current_animation)

    def animationDone(self, current_animation):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def setupAnimation(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def drawAnimation(self, x, y):
        if self._visible:
            dest_rect = SDL_Rect()
            src_rect = None 
            
            dest_rect.x = int(x + self._offsets[self._current_animation].x)
            dest_rect.y = int(y + self._offsets[self._current_animation].y)
            dest_rect.w = int(self._src_rect.w * game_globals.SPRITE_SCALE)
            dest_rect.h = int(self._src_rect.h * game_globals.SPRITE_SCALE)

            src_rect = self._animations[self._current_animation][self._frame_index]
            self._graphics.blitSurface(self._sprite_sheet, src_rect, dest_rect)



