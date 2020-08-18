from sdl2 import (SDL_Renderer, SDL_RenderCopy, SDL_RenderPresent, SDL_RenderClear, SDL_CreateRenderer, SDL_RENDERER_ACCELERATED)
from sdl2.sdlimage import (IMG_Load)
'''
 Graphics Class 
	-Holds all information dealing with graphics for the game.
'''

class Graphics:
    def __init__(self, window):
        self._window = window
        self._renderer = SDL_CreateRenderer(self._window.window, -1, SDL_RENDERER_ACCELERATED)
        self._sprite_sheets = {}
    
    def loadImage(self, file_path):
        if file_path not in self._sprite_sheets.keys():
            self._sprite_sheets[file_path] = IMG_Load(file_path)
        
        return self._sprite_sheets[file_path]
    
    def blitSurface(self, texture, src_rect, dest_rect):
        SDL_RenderCopy(self._renderer, texture, src_rect, dest_rect)
    
    def flip(self):
        SDL_RenderPresent(self._renderer)
    
    def clear(self):
        SDL_RenderClear(self._renderer)
    
    def getRenderer(self):
        return self._renderer

     


    