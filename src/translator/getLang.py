import json
import os
import re

from src.function.UserLocalModel import UserLocal


def _loadLanguage(file_path: str):
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
    return data


class Language:
    def __init__(self):
        self._FilePath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self._getFile = f"{self._FilePath}/lang"
        self.lang = []
        self._allFile = []
        self._getAll()

    def _getAll(self):
        self._allFile = os.listdir(f"{self._getFile}")
        self.lang = [os.path.splitext(file)[0] for file in self._allFile if file.endswith('.json')]
        return self.lang

    def _getDefault(self, translator: str):
        data = _loadLanguage(f"{self._getFile}/zh-hant.json")
        if translator in data:
            return data[translator]
        else:
            return translator

    def get(self, translator: str, toLanguage: str = 'zh-hant', inpData: str = None) -> str:
        if toLanguage not in self.lang:
            return self._getDefault(translator)
        data = _loadLanguage(f"{self._getFile}/{toLanguage}.json")
        if inpData is not None and translator in data:
            subData = re.sub(r"%s", inpData, data[translator])
            return subData
        if translator not in data:
            return self._getDefault(translator)
        return data[translator]

    def getDefault(self, local: UserLocal, default: str | None):
        if local.Check:
            language = local.Language
            return language
        elif default is None and default not in self.lang and not local.Check:
            local.initUserLocal()
            language = "zh-hant"
            return language
        else:
            local.initUserLocal(default)
            language = default
            return language
