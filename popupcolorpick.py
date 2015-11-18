"""Popup color picker."""
import mdpopups
import sublime_plugin

color_wheel = [
    ['036', '369', '36c', '039', '009', '00c', '006'],
    ['066', '069', '09c', '06c', '03c', '00f', '33f', '339'],
    ['699', '099', '3cc', '0cf', '09f', '06f', '36f', '33c', '669'],
    ['396', '0c9', '0fc', '0ff', '3cf', '39f', '69f', '66f', '60f', '60c'],
    ['393', '0c6', '0f9', '6fc', '6ff', '6cf', '9cf', '99f', '96f', '93f', '90f'],
    ['060', '0c0', '0f0', '6f9', '9fc', 'cff', 'ccf', 'c9f', 'c6f', 'c3f', 'c0f', '90c'],
    ['030', '093', '3c3', '6f6', '9f9', 'cfc', 'fff', 'fcf', 'f9f', 'f6f', 'f0f', 'c0c', '606'],
    ['360', '090', '6f3', '9f6', 'cf9', 'ffc', 'fcc', 'f9c', 'f6c', 'f3c', 'c09', '939'],
    ['330', '690', '9f3', 'cf6', 'ff9', 'fc9', 'f99', 'f69', 'f39', 'c39', '909'],
    ['663', '9c0', 'cf3', 'ff6', 'fc6', 'f96', 'f66', 'f06', 'c69', '936'],
    ['996', 'cc0', 'ff0', 'fc0', 'f93', 'f60', 'ff5050', 'c06', '603'],
    ['963', 'c90', 'f90', 'c60', 'f30', 'f00', 'c00', '903'],
    ['630', '960', 'c30', '930', '900', '800000', '933']
]


css = '''
'''


class ColorWheelCommand(sublime_plugin.TextCommand):
    """Experimental color picker."""

    def run(self, edit, initial_color='#ff0000'):
        """Run command."""

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        current_color = rgba1.get_rgba()
        text = []
        text.append('# Color Picker\n')
        obj = mdpopups._get_scheme(self.view)[0]
        bground = obj.bground
        text.append(
            '<span class="color-wheel">%s</span><br>' % (
                mdpopups.color_box(
                    [bground], '#fefefeff', '#333333ff', border_size=0, height=9, width=20 * 14, check_size=2
                )
            )
        )
        padding = (20 * 3 + 10)
        decrement = True
        for row in color_wheel:
            text.append('<span class="color-wheel">')
            pad = mdpopups.color_box(
                [bground], '#fefefeff', '#333333ff', border_size=0, height=18, width=padding, check_size=2
            )
            text.append(pad)
            for color in row:
                if len(color) == 3:
                    color = '#' + ''.join([c * 2 for c in color]) + 'ff'
                else:
                    color = '#' + color + 'ff'
                text.append(
                    '<a href="%s">%s</a>' % (
                        color, mdpopups.color_box([color], '#fefefeff', '#333333ff', border_size=2, height=18, width=20)
                    )
                )
            text.append(pad)
            text.append('</span><br>')
            if padding == 10:
                decrement = False
            if decrement:
                padding -= 10
            else:
                padding += 10

        text.append(
            '<span class="color-wheel">%s</span>\n\n' % (
                mdpopups.color_box(
                    [bground], '#fefefeff', '#333333ff', border_size=0, height=9, width=20 * 14, check_size=2
                )
            )
        )

        text.append('## Current\n')
        text.append(
            '<span class="color-wheel current-color">%s</span>\n\n' % (
                mdpopups.color_box(
                    [current_color], '#fefefeff', '#333333ff', border_size=2, height=18, width=20 * 14, check_size=2
                )
            )
        )

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Red\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.red(0.95)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.red(1.05)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Green\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.green(0.95)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.green(1.05)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Blue\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.blue(0.95)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.blue(1.05)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Alpha\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.alpha(1.05)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.alpha(0.95)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        text.append('## Hue\n')
        text.append('<span class="color-wheel">')
        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        count = 12
        temp = []
        while count:
            rgba1.hue(-15)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1

        text += reversed(temp)

        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.hue(15)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Saturation\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.saturation(1.05)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.saturation(0.95)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        rgba1 = mdpopups.rgba.RGBA(initial_color)
        rgba2 = mdpopups.rgba.RGBA(initial_color)
        text.append('## Luminance\n')
        text.append('<span class="color-wheel">')
        temp = []
        count = 12
        while count:
            rgba1.luminance(0.95)
            temp.append(
                mdpopups.color_box(
                    [rgba1.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text += reversed(temp)
        text.append(
            mdpopups.color_box(
                [current_color], '#fefefeff', '#333333ff', border_size=2, height=22, width=22, check_size=2
            )
        )
        count = 12
        while count:
            rgba2.luminance(1.05)
            text.append(
                mdpopups.color_box(
                    [rgba2.get_rgba()], '#fefefeff', '#333333ff', border_size=2, height=18, width=22, check_size=2
                )
            )
            count -= 1
        text.append('</span>\n\n')

        mdpopups.show_popup(self.view, ''.join(text), css=css, max_width=500, max_height=700)
