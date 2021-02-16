import pygame
import pygame_menu.locals
from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core.widget import Widget

class PokemonTypeWidget(Widget):

    def __init__(self, type1: str, type2: str="", scale=(1.0,1.0), align=pygame_menu.locals.ALIGN_LEFT):
        super(PokemonTypeWidget, self).__init__()
        self.set_alignment(align)
        self.type1 = type1.strip()
        self.type2 = type2.strip()

        self._image1 = BaseImage('./images/gui/' + self.type1 + '.png')
        self._image1.scale(scale[0], scale[1], smooth=True)
        if self.type2 == None or self.type2 == "":
            self._image2 = None
        else:
            self._image2 = BaseImage('./images/gui/' + self.type2 + '.png')
            self._image2.scale(scale[0], scale[1], smooth=True)

    def _draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._rect.topleft)
    
    def draw(self, surface):
        self._draw(surface)

    def _render(self):
        if self._surface is not None:
            return True
        surface1 = self._image1.get_surface()
        if self._image2 == None:
            self._rect.width, self._rect.height = surface1.get_size()
            self._surface = surface1
        else:
            surface2 = self._image2.get_surface()
            surface = pygame.Surface((surface1.get_width() + surface2.get_width() + 15, surface1.get_height()), pygame.SRCALPHA)
            surface.blit(surface1, (5, 0))
            surface.blit(surface2, (surface1.get_width() + 10, 0))
            self._surface = surface
            self._rect.width, self._rect.height = surface.get_size()

        #if not self._render_hash_changed(self._visible):
        #    return True
        #self.force_menu_surface_update()
    
    def _apply_font(self):
        pass

    def update(self, events):
        pass