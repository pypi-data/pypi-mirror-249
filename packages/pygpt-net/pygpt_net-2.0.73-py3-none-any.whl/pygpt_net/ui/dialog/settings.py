#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.25 21:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget, QFrame, QLineEdit

from pygpt_net.ui.widget.dialog.settings import SettingsDialog
from pygpt_net.ui.widget.option.checkbox import OptionCheckbox
from pygpt_net.ui.widget.option.input import OptionInput
from pygpt_net.ui.widget.option.slider import OptionSlider
from pygpt_net.ui.widget.option.textarea import OptionTextarea
from pygpt_net.ui.widget.element.group import CollapsedGroup
from pygpt_net.ui.widget.element.url import UrlLabel
from pygpt_net.utils import trans


class Settings:
    def __init__(self, window=None):
        """
        Settings dialog

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup settings dialog"""

        id = "settings"
        path = self.window.core.config.path

        # buttons
        self.window.ui.nodes['settings.btn.defaults.user'] = QPushButton(trans("dialog.settings.btn.defaults.user"))
        self.window.ui.nodes['settings.btn.defaults.app'] = QPushButton(trans("dialog.settings.btn.defaults.app"))
        self.window.ui.nodes['settings.btn.save'] = QPushButton(trans("dialog.settings.btn.save"))
        self.window.ui.nodes['settings.btn.defaults.user'].clicked.connect(
            lambda: self.window.controller.settings.editor.load_defaults_user())
        self.window.ui.nodes['settings.btn.defaults.app'].clicked.connect(
            lambda: self.window.controller.settings.editor.load_defaults_app())
        self.window.ui.nodes['settings.btn.save'].clicked.connect(
            lambda: self.window.controller.settings.editor.save(id))

        # set enter key to save button
        self.window.ui.nodes['settings.btn.defaults.user'].setAutoDefault(False)
        self.window.ui.nodes['settings.btn.defaults.app'].setAutoDefault(False)
        self.window.ui.nodes['settings.btn.save'].setAutoDefault(True)

        # bottom buttons layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.window.ui.nodes['settings.btn.defaults.user'])
        bottom_layout.addWidget(self.window.ui.nodes['settings.btn.defaults.app'])
        bottom_layout.addWidget(self.window.ui.nodes['settings.btn.save'])

        self.window.ui.paths[id] = QLabel(str(path))
        self.window.ui.paths[id].setStyleSheet("font-weight: bold;")

        # advanced options keys
        advanced_options = []

        # get settings options config
        settings_options = self.window.controller.settings.editor.get_options()
        for key in settings_options:
            if 'advanced' in settings_options[key] and settings_options[key]['advanced']:
                advanced_options.append(key)

        # build settings widgets
        settings_widgets = self.build_settings_widgets(settings_options)

        # apply settings widgets
        for key in settings_widgets:
            self.window.ui.config_option[key] = settings_widgets[key]

        # apply widgets to layouts
        options = {}
        for key in settings_widgets:
            type = settings_options[key]['type']
            label = 'settings.' + settings_options[key]['label']
            extra = {}
            if 'extra' in settings_options[key]:
                extra = settings_options[key]['extra']
            if type == 'text' or type == 'int' or type == 'float':
                options[key] = self.add_option(label, settings_widgets[key], type, extra)
            elif type == 'textarea':
                options[key] = self.add_row_option(label, settings_widgets[key], type, extra)
            elif type == 'bool':
                options[key] = self.add_raw_option(settings_widgets[key], type, extra)

        fixed_options = [
            'api_key',
            'organization_key'
        ]

        # prepare scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        line = self.add_line()
        scroll_content = QVBoxLayout()

        # API keys at the top
        rows = QVBoxLayout()
        for key in fixed_options:
            scroll_content.addLayout(options[key])
            if 'urls' in settings_options[key]:
                urls_widget = self.add_urls(settings_options[key]['urls'], Qt.AlignCenter)
                scroll_content.addWidget(urls_widget)

        scroll_content.addWidget(line)

        # append widgets options layouts to scroll area
        for opt_key in options:
            option = options[opt_key]

            # hide advanced options
            if opt_key in advanced_options:
                continue

            # prevent already added options from being added again
            if opt_key in fixed_options:
                continue

            # add option
            scroll_content.addLayout(option)

            # append URLs
            if 'urls' in settings_options[opt_key]:
                urls_widget = self.add_urls(settings_options[opt_key]['urls'])
                scroll_content.addWidget(urls_widget)

            line = self.add_line()
            scroll_content.addWidget(line)

        # append advanced options at the end
        if len(advanced_options) > 0:
            group_id = 'settings.advanced'
            self.window.ui.groups[group_id] = CollapsedGroup(self.window, group_id, None, False, None)
            self.window.ui.groups[group_id].box.setText(trans('settings.advanced.collapse'))
            for opt_key in options:
                # hide non-advanced options
                if opt_key not in advanced_options:
                    continue

                # add option to group
                option = options[opt_key]
                self.window.ui.groups[group_id].add_layout(option)

                # add line if not last option
                if opt_key != advanced_options[-1]:
                    line = self.add_line()
                    self.window.ui.groups[group_id].add_widget(line)

            scroll_content.addWidget(self.window.ui.groups[group_id])

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_content)
        scroll.setWidget(scroll_widget)

        layout = QVBoxLayout()
        # layout.addLayout(rows)  # api keys
        layout.addWidget(scroll)  # rest of options widgets
        layout.addLayout(bottom_layout)  # buttons (save, defaults)

        self.window.ui.dialog['config.' + id] = SettingsDialog(self.window, id)
        self.window.ui.dialog['config.' + id].setLayout(layout)
        self.window.ui.dialog['config.' + id].setWindowTitle(trans('dialog.settings'))

    def build_settings_widgets(self, options) -> dict:
        """
        Build settings widgets

        :param options: settings options
        """
        widgets = {}
        for key in options:
            option = options[key]
            label = options[key]['label']

            # create widget by option type
            if option['type'] == 'text' or option['type'] == 'int' or option['type'] == 'float':
                if 'slider' in option and option['slider'] \
                        and (option['type'] == 'int' or option['type'] == 'float'):
                    min = 0
                    max = 1
                    step = 1

                    if 'min' in option:
                        min = option['min']
                    if 'max' in option:
                        max = option['max']
                    if 'step' in option:
                        step = option['step']
                    value = min
                    if 'value' in option:
                        value = option['value']

                    multiplier = 1
                    if 'multiplier' in option:
                        multiplier = option['multiplier']

                    if option['type'] == 'float':
                        value = value * multiplier  # multiplier makes effect only on float
                        min = min * multiplier
                        max = max * multiplier
                        # step = step * multiplier
                    elif option['type'] == 'int':
                        value = int(value)

                    # slider + text input
                    widgets[key] = OptionSlider(self.window, label, '',
                                                min,
                                                max,
                                                step,
                                                value)
                else:
                    # text input
                    widgets[key] = OptionInput(self.window, label)
                    if 'secret' in option and option['secret']:
                        # password
                        widgets[key].setEchoMode(QLineEdit.Password)

            elif option['type'] == 'textarea':
                # textarea
                widgets[key] = OptionTextarea(self.window, label)
                widgets[key].setMinimumHeight(100)
            elif option['type'] == 'bool':
                # checkbox
                widgets[key] = OptionCheckbox(self.window, label, trans('settings.' + key))

        return widgets

    def add_line(self) -> QFrame:
        """
        Make line
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def add_option(self, title: str, option, type, extra=None) -> QHBoxLayout:
        """
        Add option (label + option)

        :param title: Title
        :param option: Option
        :param type: Option type
        :param extra: Extra params
        """
        label_key = title + '.label'
        self.window.ui.nodes[label_key] = QLabel(trans(title))
        if extra is not None and 'bold' in extra and extra['bold']:
            self.window.ui.nodes[label_key].setStyleSheet(self.window.controller.theme.get_style('text_bold'))
        layout = QHBoxLayout()
        layout.addWidget(self.window.ui.nodes[label_key])
        layout.addWidget(option)

        if title == 'settings.api_key':
            self.window.ui.nodes[label_key].setMinimumHeight(60)
        return layout

    def add_row_option(self, title: str, option, type, extra=None) -> QHBoxLayout:
        """
        Add option (label + option)

        :param title: Title
        :param option: Option
        :param type: Option type
        :param extra: Extra params
        """
        label_key = title + '.label'
        self.window.ui.nodes[label_key] = QLabel(trans(title))
        if extra is not None and 'bold' in extra and extra['bold']:
            self.window.ui.nodes[label_key].setStyleSheet(self.window.controller.theme.get_style('text_bold'))
        layout = QVBoxLayout()
        layout.addWidget(self.window.ui.nodes[label_key])
        layout.addWidget(option)

        # append URLs
        if 'urls' in extra \
                and extra['urls'] is not None \
                and len(extra['urls']) > 0:
            urls_widget = self.add_urls(extra['urls'])
            layout.addWidget(urls_widget)

        if title == 'settings.api_key':
            self.window.ui.nodes[label_key].setMinimumHeight(60)
        return layout

    def add_raw_option(self, option, type, extra=None) -> QHBoxLayout:
        """
        Add raw option row (option only)

        :param option: Option
        :param type: Option type
        :param extra: Extra options
        """
        layout = QHBoxLayout()
        layout.addWidget(option)

        # append URLs
        if 'urls' in extra \
                and extra['urls'] is not None \
                and len(extra['urls']) > 0:
            urls_widget = self.add_urls(extra['urls'])
            layout.addWidget(urls_widget)

        return layout

    def add_urls(self, urls, align=Qt.AlignLeft) -> QWidget:
        """
        Add clickable urls to list

        :param urls: urls dict
        :param align: alignment
        """
        layout = QVBoxLayout()
        for name in urls:
            url = urls[name]
            label = UrlLabel(name, url)
            layout.addWidget(label)

        layout.setAlignment(align)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        return widget
