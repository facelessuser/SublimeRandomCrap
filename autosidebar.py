"""
AutoSideBar.

Licensed under MIT
Copyright (c) 2016 Isaac Muse <isaacmuse@gmail.com>
"""
import sublime
import sublime_plugin


class AutoSideBarListener(sublime_plugin.EventListener):
    """Listener that auto hides/shows the sidebar."""

    def on_hover(self, view, point, hover_zone):
        """
        Hide/Show sidebar on hover event.

        If hovering over the main view, keep the sidebar hidden.
        If hovering over the gutter, show the sidebar.
        Events like "reveal file" in sidebar will usually show the sidebar on their own.
        """

        settings = sublime.load_settings('autosidebar.sublime-settings')
        if settings.get('autosidebar_enable', True):
            win = view.window()
            if win is not None:
                sidebar_visible = win.is_sidebar_visible()
                if sidebar_visible is False and hover_zone == sublime.HOVER_GUTTER:
                    win.run_command('toggle_side_bar')
                elif sidebar_visible is True and hover_zone != sublime.HOVER_GUTTER:
                    win.run_command('toggle_side_bar')


class AutoSideBarToggleCommand(sublime_plugin.WindowCommand):
    """Toggle auto-sidebar feature."""

    def run(self, show_sidebar=None):
        """Run command."""

        settings = sublime.load_settings('autosidebar.sublime-settings')
        enabled = bool(settings.get('autosidebar_enable', False))
        settings.set('autosidebar_enable', not enabled)
        sublime.save_settings('autosidebar.sublime-settings')

        # If originally enabled and a sidebar state is defined
        if enabled and show_sidebar is not None:
            sidebar_visible = self.window.is_sidebar_visible()
            if not sidebar_visible and show_sidebar:
                self.window.run_command('toggle_side_bar')
            if sidebar_visible and not show_sidebar:
                self.window.run_command('toggle_side_bar')
