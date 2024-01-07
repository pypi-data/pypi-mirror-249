import sdl2


class itemBase:
    def __init__(self):
        self.screenID = "/default/"
        self.x, self.y = 0, 0

    def update(self) -> None:
        return None

    def renderObj(self) -> sdl2.surface.SDL_Surface | None:
        return None


class rect(itemBase):
    def __init__(self, screenID: str = "/default/", x: int = 0, y: int = 0, w: int = 50, h: int = 50,
                 color=(255, 255, 255, 255)):
        super().__init__()
        self.screenID = screenID

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color

    def update(self, screenID: str = None, x: int = None, y: int = None, w: int = None, h: int = None, color=None) -> None:
        if screenID is not None:
            self.screenID = screenID

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if w is not None:
            self.w = w

        if h is not None:
            self.h = h

        if color is not None:
            self.color = color

        return None

    def renderObj(self) -> sdl2.surface.SDL_Surface | None:
        surface = sdl2.SDL_CreateRGBSurface(0, self.w, self.h, 32, 0, 0, 0, 0)

        if surface:
            sdl2.SDL_FillRect(surface, None, sdl2.SDL_MapRGBA(surface.contents.format, *self.color))

            return surface
        else:
            print("Failed to create surface:", sdl2.SDL_GetError())
            return None
