language_timezone_mapping = {
    "en-US": "America/New_York",
    "zh-CN": "Asia/Shanghai",
    "pt-BR": "America/Sao_Paulo",
    "es-ES": "Europe/Madrid",
    "fr-FR": "Europe/Paris",
    "de-DE": "Europe/Berlin",
    "ja-JP": "Asia/Tokyo",
    "ko-KR": "Asia/Seoul",
    "ru-RU": "Europe/Moscow",
    "it-IT": "Europe/Rome",
    "uk-UA": "Europe/Kyiv",
    "vi-VN": "Asia/Ho_Chi_Minh",
}

languages = set(language_timezone_mapping.values())


def supported_language(lang):
    if lang in languages:
        return lang
    raise ValueError("{} is not a valid language".format(lang))
