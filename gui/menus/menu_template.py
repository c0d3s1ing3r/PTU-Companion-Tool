
from __future__ import annotations
from os import terminal_size
#from gui import gui_manager
#from gui.menus import menu_factory
import pygame_menu





# superclass for menus, namely just a means of setting defaults here instead of per-menu
class MenuTemplate():
    
    def __init__(self, factory: MenuFactory, manager: GUIManager, align=pygame_menu.locals.ALIGN_LEFT):
        self.alignment = align
        self._gui_manager = manager
        self._factory = factory
        # TO BE OVERRIDDEN BY SUBCLASSES
        self.menu: pygame_menu.Menu
        self.menu = self._factory.build_menu('ERROR')
    
    def rebuild_menu(self):
        self._add_label('Hello! You\'ve encountered an error. Please let the developer know that something is wrong')
        self._add_label('Please let them know that there was supposed to be a menu of type ' + self.__repr__() + ' here')
        self._add_label('Press the below button to return to what you were doing')
        self._add_label('Have a nice day!')
        self._add_back_button()
    
    def _refresh_if_current(self):
        if self._gui_manager.get_current() == self:
            self._gui_manager.refresh_current()

    # the below are simple wrappers for the existing menu methods, I just wanted them called with certain program defaults
    def _add_label(self, label_text):
        self.menu.add_label(label_text, align=self.alignment)
    
    def _add_button(self, button_text, button_callback, *args):
        if len(args) == 0:
            self.menu.add_button(button_text, button_callback, align=self.alignment)
        else:
            self.menu.add_button(button_text, button_callback, args, align=self.alignment)
    
    def _add_vertical_margin(self, amt):
        self.menu.add_vertical_margin(amt)
    
    # onreturn_callback gets the current text_input text as its argument
    def _add_text_input(self, prompt, default_text, onreturn_callback, maxchar=0):
        self.menu.add_text_input(prompt, default=default_text, onreturn=onreturn_callback, align=self.alignment, maxchar=maxchar)
    
    def _add_image(self, path, scale=(1,1), align=None):
        if align == None:
            align = self.alignment
        self.menu.add_image(path, scale=scale, align=align)
    
    def _add_generic_widget(self, widget):
        self.menu.add_generic_widget(widget, configure_defaults=False)
    
    def _exit_operations(self):
        '''Submenus can override this method before calling it (which will just go back to the previous menu) if they have some operations they really want to execute before closing'''
        self._gui_manager.go_back()

    def _add_back_button(self, button_text='BACK'):
        self._add_button(button_text, self._exit_operations)
    
    def _add_back_to_main_button(self, button_text='MAIN MENU'):
        self._add_button(button_text, self._gui_manager.back_to_main)
    
