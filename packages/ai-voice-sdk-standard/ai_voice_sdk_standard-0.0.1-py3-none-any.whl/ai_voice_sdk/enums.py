from enum import Enum

# orator
class Voice(Enum):
    AURORA_HANNAH = 'zh-TW-szyu_news_cs'
    STEADY_AARON = 'zh-TW-M03_cs'
    CHARMING_MERCURY_SOFT_BELLA  = 'zh-TW-Mercury_soft_cs'
    CHEERFUL_MERCURY_HAPPY_BELLA = 'zh-TW-Mercury_happy_cs'
    VIBRANT_BILL = 'zh-TW-Bob_cs'
    GRACEFUL_SHAWN = 'zh-TW-Rongin_cs'
    ADVERTISEMENT_AARON = 'zh-TW-M03_vc_tianxia_female_cs'
    AT_EASE_HANNAH = 'zh-TW-szyu_colloquial_cs'
    STEADFAST_AURORA = 'zh-TW-F05_vc_tianxia_female_cs'


class SsmlVersion(Enum):
    V1 = 'version="1.1"'


class SsmlLanguage(Enum):
    TW = 'zh-TW'


class SsmlPhoneme(Enum):
    TW = 'bopomo'


class ConverterStatus(Enum):
    ConverterStartUp = 0
    ConverVoiceStart = 10
    ConverVoiceRunning = 11
    ConverVoiceCompleted = 12
    ConverVoiceFail = 13
    ServerBusy = 21
    GetSpeechSuccess = 91
    GetSpeechFail = 92
