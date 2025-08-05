class LanguageProxy(object):

    def __init__(self, value) -> None:
        self.value = value


class LanguageEnumValue(object):
    def __init__(self, key: str, lang_display_names: dict[str, str]) -> None:
        self.key = key
        self.lang_display_names = lang_display_names

    def __get__(self, obj, objtype=None) -> LanguageProxy:
        return LanguageProxy(self)

    def get_display_name(self, lang) -> str:
        # 英文名按理一定存在
        return self.lang_display_names.get(
            lang, self.lang_display_names.get("en-US", self.key)
        )

    # def __str__(self) -> str:
    #     return self.key

    def __eq__(self, value: object) -> bool:
        return self.key == value

    def __hash__(self) -> int:
        return self.key.__hash__()

    def to_dict(self):
        return {
            "key": self.key,
            "language_display_names": self.lang_display_names,
        }
