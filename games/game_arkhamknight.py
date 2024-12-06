import mobase
from PyQt6.QtCore import QDir, QFileInfo

from ..basic_features import BasicLocalSavegames
from ..basic_game import BasicGame
from ..steam_utils import find_steam_path

# Lifted from https://github.com/ModOrganizer2/modorganizer-basic_games/games/game_arkhamcity.py

class ArkhamKnightModDataChecker(mobase.ModDataChecker):
    def __init__(self):
        super().__init__()
        self.validDirNames = [
            "DLC",
            "config",
            "cookedpcconsole",
            "localization",
            "movies",
            "moviesstereo",
            "splash",
        ]

def dataLooksValid(
        self, filetree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        for entry in filetree:
            if not entry.isDir():
                continue
            if entry.name().casefold() in self.validDirNames:
                return mobase.ModDataChecker.VALID
        return mobase.ModDataChecker.INVALID

class ArkhamKnightGame(BasicGame):
    Name = "Batman: Arkham Knight Plugin"
    Author = "dirtydanisreal"
    Version = "0.1"

    GameName = "Batman: Arkham Knight"
    GameShortName = "batmanarkhamknight"
    GameNexusId = 1630795
    GameSteamId = 208650
    GameGogId = 188197070
    GameBinary = "Binaries/Win64/BatmanAK.exe"
    GameDataPath = "BmGame"
    GameDocumentsDirectory = (
        "BmGame/Config"
    )
    GameIniFiles = ["BmEngine.ini", "BmGame.ini", "BmInput.ini", "CONSOLE.txt]
    GameSavesDirectory = "%DOCUMENTS%/WB Games/Batman Arkham Knight/BmGame/Config"
    GameSaveExtension = "sgd"

    # This will only detect saves from the earliest-created Steam profile on the user's PC.
    def savesDirectory(self) -> QDir:
        docSaves = QDir(self.gameSavesDirectory().cleanPath("../../SaveData"))
        if self.is_steam():
            if (steamDir := find_steam_path()) is None:
                return docSaves
            for child in steamDir.joinpath("userdata").iterdir():
                if not child.is_dir() or child.name == "0":
                    continue
                steamSaves = child.joinpath("208650", "remote")
                if steamSaves.is_dir():
                    return QDir(str(steamSaves))
            else:
                return docSaves
        else:
            return docSaves

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(ArkhamKnightModDataChecker())
        self._register_feature(BasicLocalSavegames(self.savesDirectory()))
        return True

    def executables(self):
        return [
            mobase.ExecutableInfo(
                "Batman: Arkham City",
                QFileInfo(self.gameDirectory(), "Binaries/Win64/BatmanAK.exe"),
            )
        ]
