import os


class MyDirectories:
    # Get the directory of the current script or module
    ProjectDir = os.path.dirname(os.path.realpath(__file__))

    # Navigate up the directory tree until reaching the directory with the .idea folder
    while not os.path.exists(os.path.join(ProjectDir, '.idea')) and ProjectDir != '/':
        ProjectDir = os.path.dirname(ProjectDir)

    # BinRTTradesDir
    BinRTTradesDir = os.path.join(ProjectDir, 'data\\trades')

    def __init__(self):
        pass


def getQuotesDir():
    return os.path.join(MyDirectories.ProjectDir, 'data\\quotes')


def getTradesDir():
    return os.path.join(MyDirectories.ProjectDir, 'data\\trades')


def getProjectDir():
    return MyDirectories.ProjectDir


def getDataDir():
    return os.path.join(MyDirectories.ProjectDir, 'data')