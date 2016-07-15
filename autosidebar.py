"""AutoSideBar."""
import sublime
import sublime_plugin

tab_enabled = False


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
        if win is not None:
            sidebar_visible = win.is_sidebar_visible()
            if sidebar_visible is False and hover_zone == sublime.HOVER_GUTTER:
                win.run_command('toggle_side_bar')
            elif sidebar_visible is True and hover_zone != sublime.HOVER_GUTTER:
                win.run_command('toggle_side_bar')


class AutoTabBarListener(sublime_plugin.EventListener):
    """Listener that auto hides/shows the sidebar."""

    def on_hover(self, view, point, hover_zone):
        """Hide/Show tabs on hover event."""
        if tab_enabled:
            win = view.window()
            y = view.viewport_position()[1]
            point_y = view.text_to_layout(point)[1]
            top_view = hover_zone != sublime.HOVER_GUTTER and (point_y - y) <= 1.0
            if win is not None:
                tabs_visible = win.get_tabs_visible()
                if not tabs_visible and top_view:
                    win.run_command('toggle_tabs')
                elif tabs_visible and not top_view:
                    win.run_command('toggle_tabs')
