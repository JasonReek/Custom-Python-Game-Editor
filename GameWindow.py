import sys
import sdl2.ext
from sdl2 import (SDLK_DOWN, SDLK_UP, SDLK_LEFT, SDLK_RIGHT, SDL_KEYDOWN, SDL_KEYUP, 
SDL_SCANCODE_LEFT, SDL_SCANCODE_RIGHT, SDL_Renderer)
from Graphics import Graphics
from Player import Player
from Input import Input

FPS = 50;
MAX_FRAME_TIME = (5 * 1000 / FPS);

class GameWindow:
    def __init__(self):
        self._window = None
        self._graphics = None
        self._sprite = None 
        self._running = True
        self._renderer = SDL_Renderer()
        self._player = None
        self._input = Input() 

    def gameLoop(self):
        sdl2.ext.init()
        self._window = sdl2.ext.Window("Game Window", size=(800, 600))
        self._graphics = Graphics(self._window)
        self._player = Player(self._graphics, 100, 100)
        self._window.show()

        LAST_UPDATE_TIME = 0

        while self._running:

            self._input.beginNewFrame()
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == SDL_KEYDOWN:
                    if event.key.repeat == 0:
                        self._input.keyDownEvent(event)
                elif event.type == SDL_KEYUP:
                    self._input.keyUpEvent(event)
                
                elif event.type == sdl2.SDL_QUIT:
                    self._running = False
                    break

            if self._input.wasKeyPressed(SDL_SCANCODE_LEFT):
                self._player.moveLeft()
            elif self._input.wasKeyPressed(SDL_SCANCODE_RIGHT):
                self._player.moveRight()
            if not self._input.isKeyHeld(SDL_SCANCODE_LEFT) and not self._input.isKeyHeld(SDL_SCANCODE_RIGHT):
                self._player.stopMoving()

            CURRENT_TIME_MS = sdl2.SDL_GetTicks()
            ELAPSED_TIME_MS = CURRENT_TIME_MS - LAST_UPDATE_TIME
            self.update(min([ELAPSED_TIME_MS, MAX_FRAME_TIME]))
            LAST_UPDATE_TIME = CURRENT_TIME_MS

            self.draw()
            

        return 0
    
    def draw(self):
        self._graphics.clear()

        self._player.draw()
        self._graphics.flip()
    
    def update(self, elapsed_time):
        self._player.update(elapsed_time)
    
    def start(self):
        sys.exit(self.gameLoop())

if __name__ == '__main__':
    game_window = GameWindow()
    game_window.start()
    