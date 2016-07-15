"""AutoSideBar."""
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
        win = view.window()

        sidebar_visible = win.is_sidebar_visible()
        if sidebar_visible is not None:
            if sidebar_visible is False and hover_zone == sublime.HOVER_GUTTER:
                win.run_command('toggle_side_bar')
            elif sidebar_visible is True and hover_zone != sublime.HOVER_GUTTER:
                win.run_command('toggle_side_bar')
