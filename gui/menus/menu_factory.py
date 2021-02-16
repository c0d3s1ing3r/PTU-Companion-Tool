import pygame_menu


#class MetaMenu():

#    def __init__(self):
#        self.attributes = dict()
#        self.menu = None

class MenuFactory():

    # define constants all menus should have
    def __init__(self, display_width, display_height, theme):
        self.display_height = display_height
        self.display_width = display_width
        self.theme = theme
    
    def build_menu(self, title, width=-1, height=-1, theme=-1, columns=1, rows=None):
        if width == -1:
            width = self.display_width
        if height == -1:
            height = self.display_height
        if theme == -1:
            theme = self.theme

        return pygame_menu.Menu(
            width=width, 
            height=height, 
            columns=columns, 
            rows=rows, 
            theme=theme, 
            title=title
        )
