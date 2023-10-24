import json
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

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

    def _getDefault(self, translator: str | None, inpData: tuple) -> str:
        data = _loadLanguage(f"{self._getFile}/zh-hant.json")
        if inpData is not None and translator in data:
            subData = data[translator] % inpData
            return subData
        if translator not in data:
            return translator
        return data[translator]

    def get(self, translator: str, toLanguage: str | None, *inpData: str) -> str:
        if toLanguage not in self.lang:
            return self._getDefault(translator, inpData)
        data = _loadLanguage(f"{self._getFile}/{toLanguage}.json")
        if inpData is not None and translator in data:
            subData = data[translator] % inpData
            return subData
        if inpData is None:
            laseData = ()
        else:
            laseData = inpData
        if translator not in data:
            return self._getDefault(translator, laseData)
        return data[translator]

    def getDefault(self, local: UserLocal, default: str | None) -> str:
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

    def button(self) -> InlineKeyboardMarkup:
        index = 0
        max_value = len(self.lang) - 1
        inner_list_length = 5
        result = []
        i = 0
        while index <= max_value:
            inner_list = []
            for j in range(inner_list_length):
                if index > max_value:
                    break
                inner_list.append(
                    InlineKeyboardButton(self._getLangButton(self.lang[index]), callback_data=self.lang[index]))
                index += 1
            result.append(inner_list)
            i += 1
        markup = InlineKeyboardMarkup(result)
        return markup

    def _getLangButton(self, lang: str) -> str:
        data = _loadLanguage(f"{self._getFile}/{lang}.json")
        if lang not in data:
            return lang
        return data[lang]
