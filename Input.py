from sdl2 import(SDL_GetKeyboardState)

""" Input class
	- Keeps track of keyboard state.
"""

class Input:
    def __init__(self):
        self._held_keys = SDL_GetKeyboardState(None)
        self._pressed_keys = SDL_GetKeyboardState(None)
        self._released_keys = SDL_GetKeyboardState(None)
    
    # This function gets called at the beginning of each new frame 
    # to reset the keys that are no longer relevant. 
    def beginNewFrame(self):
        pass
        #self._pressed_keys.clear()
        #self._released_keys.clear()

    # This gets called when a key is pressed. 
    def keyDownEvent(self, event):
        self._pressed_keys[event.key.keysym.scancode] = True 
        self._held_keys[event.key.keysym.scancode] = True 
    
    # This gets called when a key is released 
    def keyUpEvent(self, event):
        self._released_keys[event.key.keysym.scancode] = True 
        self._held_keys[event.key.keysym.scancode] = False 
    
    # Check to see if a certain key was pressed during the current frame.
    def wasKeyPressed(self, key):
        if key in self._pressed_keys:
            return self._pressed_keys[key]
        return False 
    
    # Check to see if a certain key is held during the current frameself.
    def isKeyHeld(self, key):
        if key in self._held_keys:
            return self._held_keys[key]
        return False

    
