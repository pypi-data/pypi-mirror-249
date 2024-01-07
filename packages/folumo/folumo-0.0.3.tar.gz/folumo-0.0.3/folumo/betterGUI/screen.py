import sdl2
import sdl2.ext


data = {"root": None}


from .Items import itemBase


class screen:
    def __init__(self, title: str = "Magic", icon: str = "/magicLogo/", w: int = 250, h: int = 250, monitor: int = 0, fullscreen: bool = False, screenID: str = "load", debug: bool = False):
        sdl2.ext.init()

        self._running = True
        self._debug = debug

        data["root"] = self

        self._default = screenID
        self._defaults = {
            "title": title,
            "icon": icon,
            "wh": (w, h),
            "monitor": monitor,
            "fullscreen": fullscreen,
            "items": []
        }

        self._IDs = {
            screenID: self._defaults.copy()
        }
        self._thisScreen = screenID

        self._window = sdl2.ext.Window(self.get("title"), size=self.get("wh"))
        self._window.show()

    def get(self, var: str) -> str | tuple[int, int] | int | bool | list[itemBase]:
        var = var.lower()
        if var in ["title", "icon", "wh", "w", "h", "width", "height", "monitor", "fullscreen", "items"]:
            tmp = self._IDs[self._thisScreen]

            if var == "title":
                return tmp["title"]

            elif var == "icon":
                return tmp["icon"]

            elif var == "wh":
                return tmp["wh"]

            elif var in ["w", "width"]:
                return tmp["wh"][0]

            elif var in ["h", "height"]:
                return tmp["wh"][1]

            elif var == "monitor":
                return tmp["monitor"]

            elif var == "fullscreen":
                return tmp["fullscreen"]

            elif var == "items":
                return tmp["items"]

        else:
            self._print(f"Invalid key (var: {var}, get)")

    def _print(self, *args):
        if self.getDebug():
            print(args)

    def getDebug(self) -> bool:
        return self._debug

    def setDebug(self, newState: bool) -> None:
        self._debug = newState
        return None

    def getRun(self) -> bool:
        return self._running

    def stop(self) -> None:
        self._running = False
        return None

    def thisScreen(self) -> str:
        return self._thisScreen

    def getScreen(self, screenID: str) -> str | dict:
        if screenID == "/default/":
            return self._IDs[self._default]

        if screenID in self._IDs:
            return self._IDs[screenID]
        else:
            return f"No screen named {screenID}"

    def switchScreen(self, screenID: str) -> bool:
        if screenID in self._IDs:
            self._thisScreen = screenID
            return True

        self._print(f"Screen not found (screenID: {screenID}, switchScreen)")
        return False

    def newScreen(self, screenID: str, title: str = None, icon: str = None, w: int = None, h: int = None, monitor: int = None, fullscreen: bool = None) -> None:
        update = self._defaults.copy()

        if title is not None:
            update["title"] = title
        if icon is not None:
            update["icon"] = icon
        if w is not None:
            update["wh"][0] = w
        if h is not None:
            update["wh"][1] = h
        if monitor is not None:
            update["monitor"] = monitor
        if fullscreen is not None:
            update["fullscreen"] = fullscreen
        self._IDs[screenID] = update
        return None

    def delScreen(self, screenID: str) -> bool:
        if screenID in self._IDs:
            del self._IDs[screenID]
            return True

        self._print(f"Screen not found (screenID: {screenID}, delScreen)")
        return False

    def run(self):
        while self._running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    self.stop()
                    break

            for item in self._IDs[self.thisScreen()]["items"]:
                surf, pos = item.renderObj()
                if surf is not None:
                    rect = sdl2.SDL_Rect(*pos, surf.contents.w, surf.contents.h)
                    sdl2.SDL_BlitSurface(surf, None, self._window.get_surface(), rect)

                self._window.refresh()

        sdl2.ext.quit()
