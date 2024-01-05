import os, sys, platform
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction, QGuiApplication
from pathlib import Path
from functools import partial


letMeDoItFile = os.path.realpath(__file__)
letMeDoItAIFolder = os.path.dirname(letMeDoItFile)
with open(os.path.join(letMeDoItAIFolder, "package_name.txt"), "r", encoding="utf-8") as fileObj:
    package = fileObj.read()
apps = {
    "myhand": "MyHand",
    "letmedoit": "LetMeDoIt",
    "taskwiz": "TaskWiz",
    "cybertask": "CyberTask",
}
iconFile = os.path.join(letMeDoItAIFolder, "icons", f"{apps[package]}.png")
thisOS = platform.system()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)

        self.menu = QMenu(parent)

        for i in (
            package,
            "chatgpt",
            "geminipro",
            "geminiprovision",
            "palm2",
            "codey",
            "autoassist",
            "autoretriever",
            "automath",
            "autoteachable",
            "autobuilder",
            "etextedit",
        ):
            action = QAction(i, self)
            action.triggered.connect(partial(self.runLetMeDoItCommand, i))
            self.menu.addAction(action)

        self.menu.addSeparator()

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.exit)
        self.menu.addAction(exitAction)

        self.setContextMenu(self.menu)

    def exit(self):
        self.setVisible(False)
        QGuiApplication.instance().quit()

    def runLetMeDoItCommand(self, command):
        def createShortcutFile(filePath, content):
            with open(filePath, "w", encoding="utf-8") as fileObj:
                fileObj.write(content)

        shortcut_dir = os.path.join(letMeDoItAIFolder, "shortcuts")
        Path(shortcut_dir).mkdir(parents=True, exist_ok=True)
        commandPath = os.path.join(os.path.dirname(sys.executable), command)

        if thisOS == "Windows":
            opencommand = "start"
            filePath = os.path.join(shortcut_dir, f"{command}.bat")
            if not os.path.isfile(filePath):
                content = f'''powershell.exe -NoExit -Command "'{commandPath}' \"%1\""'''
                createShortcutFile(filePath, content)
        elif thisOS == "Darwin":
            opencommand = "open"
            filePath = os.path.join(shortcut_dir, f"{command}.command")
            if not os.path.isfile(filePath):
                content = f"""#!/bin/bash
cd {letMeDoItAIFolder}
{commandPath}"""
                createShortcutFile(filePath, content)
                os.chmod(filePath, 0o755)
        elif thisOS == "Linux":
            opencommand = "xdg-open"
            filePath = os.path.join(shortcut_dir, f"{command}.desktop")
            if not os.path.isfile(filePath):
                content = f"""#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=true
Path={letMeDoItAIFolder}
Exec={command}
Icon={iconFile}
Name={commandPath}"""
                createShortcutFile(filePath, content)
        os.system(f"{opencommand} {filePath}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    icon = QIcon(iconFile)
    trayIcon = SystemTrayIcon(icon)
    trayIcon.show()

    sys.exit(app.exec())
