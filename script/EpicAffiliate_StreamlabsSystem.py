# -*- coding: utf-8 -*-
#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import clr
import json
import codecs
import os
import re
import random
import datetime
import glob
import time
import threading
import shutil
import tempfile
from HTMLParser import HTMLParser
import argparse

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(
#     os.path.realpath(__file__)), "./libs/ChatbotSystem.dll"))
# import ChatbotSystem


#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "Epic Affiliate"
Website = "http://darthminos.tv"
Description = ""
Creator = "DarthMinos"
Version = "1.0.0-snapshot"
Repo = "camalot/chatbot-epicaffiliate"

DonateLink = "https://paypal.me/camalotdesigns"
ReadMeFile = "https://github.com/" + Repo + "/blob/develop/ReadMe.md"

SettingsFile = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "settings.json")

DataUrl = "https://cdn.jsdelivr.net/gh/camalot/epic-data-converter@develop/epic.json"
ScriptSettings = None
Initialized = False
EpicData = None
KnownBots = None

class AffiliateData(object):
    def __init__(self, dataUrl):
        try:
            self.Links = []
            # with codecs.open(dataFile, encoding="utf-8", mode="r") as f:
            #     data = json.load(f, encoding="utf-8")
            data = json.loads(json.loads(Parent.GetRequest(dataUrl, {}))['response'])
            self.Links = data
        except Exception as e:
            Parent.Log(ScriptName, str(e))

class TwitchBot(object):
    def __init__(self):
        try:
            botData = json.loads(json.loads(Parent.GetRequest(
                "https://api.twitchinsights.net/v1/bots/online", {}))['response'])['bots']
            self.Names = [bot[0].lower() for bot in botData]
        except Exception as e:
            Parent.Log(ScriptName, str(e))

class Settings(object):
    """ Class to hold the script settings, matching UI_Config.json. """

    def __init__(self, settingsfile=None):
        """ Load in saved settings file if available else set default values. """
        try:
            self.Command = "!link"
            self.CommandMessage = "Get The Game Now: "
            self.DisplaySeconds = 10
            self.BetweenAdDelay = 10
            self.Opacity = 100,
            self.TitleFontSize = 2
            self.HelpFontSize = 1.5

            self.HelpColor = "rgba(0,0,0,1)"
            self.BackgroundColor = "rgba(0,0,0,1)"
            self.IconBackgroundColor = "rgba(0,0,0,1)"
            self.OutlineColor = "rgba(240,240,240,1)"
            self.TextColor = "rgba(255,255,255,1)"
            self.CommandColor = "rgba(153,74,0,1)"

            self.FontName = "days-one"
            self.CustomFontName = ""

            self.BoxBorderRadiusTopRight = 0
            self.BoxBorderRadiusTopLeft = 0
            self.BoxBorderRadiusBottomRight = 0
            self.BoxBorderRadiusBottomLeft = 0

            self.CommandMarginTop = 0
            self.CommandMarginLeft = 12
            self.CommandMarginBottom = 0
            self.CommandMarginRight = 0

            self.HelpMarginTop = 0
            self.HelpMarginLeft = 10
            self.HelpMarginBottom = 0
            self.HelpMarginRight = 0

            self.TitleMarginTop = 0
            self.TitleMarginLeft = 12
            self.TitleMarginBottom = 0
            self.TitleMarginRight = 0

            self.IconMarginTop = 0
            self.IconMarginLeft = 0
            self.IconMarginBottom = 0
            self.IconMarginRight = 12

            self.InTransition = "slideInRight"
            self.InAttentionAnimation = "pulse"
            self.OutTransition = "slideOutRight"
            self.OutAttentionAnimation = "pulse"
            self.ResponseMessage = "You can get $epicGame and support this channel by going to $epicLink"
            self.CreatorCode = ""
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                fileSettings = json.load(f, encoding="utf-8")
                self.__dict__.update(fileSettings)

        except Exception as e:
            Parent.Log(ScriptName, str(e))

    def Reload(self, jsonData):
        """ Reload settings from the user interface by given json data. """
        Parent.Log(ScriptName, "Reload Settings")
        fileLoadedSettings = json.loads(jsonData, encoding="utf-8")
        self.__dict__.update(fileLoadedSettings)


def Init():
    global ScriptSettings
    global Initialized
    global KnownBots
    global EpicData
    if Initialized:
        Parent.Log(ScriptName, "Skip Initialization. Already Initialized.")
        return

    Parent.Log(ScriptName, "Initialize")

    KnownBots = TwitchBot()
    # Load saved settings and validate values
    ScriptSettings = Settings(SettingsFile)
    EpicData = AffiliateData(DataUrl)

    SendSettingsUpdate()

    Initialized = True
    return


def Unload():
    global Initialized
    Initialized = False
    return


def Execute(data):
    if data.IsChatMessage():
        commandTrigger = data.GetParam(0).lower()
        if not ScriptSettings.CreatorCode:
            Parent.Log(ScriptName, "CREATOR CODE not set")
            return
        # ignore messages from bots
        if IsTwitchBot(data.UserName):
            Parent.Log(ScriptName, "IT'S A BOT")
            return
        if commandTrigger == ScriptSettings.Command.lower():
            if data.GetParamCount() > 1:
                answer = data.GetParam(1)
                if answer.isnumeric():
                    answer_index = int(answer) - 1
                    if answer_index >= 0 and answer_index <= len(EpicData.Links):
                        game = EpicData.Links[answer_index]
                        Parent.SendTwitchMessage(ResponseParse(ScriptSettings.ResponseMessage, game))
                else:
                    pass
            else:
                pass
        else:
            pass
    return


def Tick():
    return


def ScriptToggled(state):
    Parent.Log(ScriptName, "State Changed: " + str(state))
    if state:
        Init()
    else:
        Unload()
    return

# ---------------------------------------
# [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------------------


def ReloadSettings(jsondata):
    Parent.Log(ScriptName, "Reload Settings")
    # Reload saved settings and validate values
    Unload()
    Init()
    return

def ResponseParse(parseString, game):
    resultString = parseString
    return resultString.replace("$epicGame", game['name']).replace("$epicLink", game['link']).replace("{{CREATORCODE}}", ScriptSettings.CreatorCode)

def Parse(parseString, user, target, message):
    resultString = parseString
    return resultString


def SendWebsocketData(eventName, payload):
    Parent.Log(ScriptName, "Trigger Event: " + eventName)
    Parent.BroadcastWsEvent(eventName, json.dumps(payload))
    return
def SendSettingsUpdate():
    SendWebsocketData("EVENT_EPICAFFILIATE_SETTINGS", ScriptSettings.__dict__)

def IsTwitchBot(user):
    return user.lower() in KnownBots.Names


def str2bool(v):
    if not v:
        return False
    return stripQuotes(v).strip().lower() in ("yes", "true", "1", "t", "y")


def stripQuotes(v):
    r = re.compile(r"^[\"\'](.*)[\"\']$", re.U)
    m = r.search(v)
    if m:
        return m.group(1)
    return v


def random_line(filename):
    with open(filename) as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def OpenScriptUpdater():
    currentDir = os.path.realpath(os.path.dirname(__file__))
    chatbotRoot = os.path.realpath(os.path.join(currentDir, "../../../"))
    libsDir = os.path.join(currentDir, "libs/updater")
    Parent.Log(ScriptName, libsDir)
    try:
        src_files = os.listdir(libsDir)
        tempdir = tempfile.mkdtemp()
        Parent.Log(ScriptName, tempdir)
        for file_name in src_files:
            full_file_name = os.path.join(libsDir, file_name)
            if os.path.isfile(full_file_name):
                Parent.Log(ScriptName, "Copy: " + full_file_name)
                shutil.copy(full_file_name, tempdir)
        updater = os.path.join(tempdir, "ChatbotScriptUpdater.exe")
        updaterConfigFile = os.path.join(tempdir, "update.manifest")
        repoVals = Repo.split('/')
        updaterConfig = {
            "path": os.path.realpath(os.path.join(currentDir, "../")),
            "version": Version,
            "name": ScriptName,
            "requiresRestart": True,
            "kill": [],
            "execute": {
                "before": [],
                "after": []
            },
            "chatbot": os.path.join(chatbotRoot, "Streamlabs Chatbot.exe"),
            "script": os.path.basename(os.path.dirname(os.path.realpath(__file__))),
            "website": Website,
            "repository": {
                "owner": repoVals[0],
                "name": repoVals[1]
            }
        }
        Parent.Log(ScriptName, updater)
        configJson = json.dumps(updaterConfig)
        Parent.Log(ScriptName, configJson)
        with open(updaterConfigFile, "w+") as f:
            f.write(configJson)
        os.startfile(updater)
        return
    except OSError as exc:  # python >2.5
        raise
    return


def OpenFollowOnTwitchLink():
    os.startfile("https://twitch.tv/DarthMinos")
    return


def OpenReadMeLink():
    os.startfile(ReadMeFile)
    return


def OpenWordFile():
    os.startfile(WordFile)
    return


def OpenDonateLink():
    os.startfile(DonateLink)
    return

def OpenOverlayInBrowser():
    os.startfile(os.path.realpath(os.path.join(
        os.path.dirname(__file__), "overlay.html")))
    return
