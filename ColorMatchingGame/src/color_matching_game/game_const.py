from micropython import const


class GameMode:
    """ゲーム難易度"""

    EASY: int = const(0)
    NORMAL: int = const(1)
    HARD: int = const(2)
    EXPERT: int = const(3)


class LightLevel:
    """明るさレベル"""

    OFF: int = const(0)
    POOR: int = const(1)
    LOW: int = const(2)
    MIDDLE: int = const(3)
    HIGH: int = const(4)
    MAX: int = const(5)


class LightValue:
    """ライト値"""

    __v = [0x00, 0x33, 0x66, 0x99, 0xCC, 0xFF]

    def get_val(self, light_level: int):
        """ライト値取得
        Args:
            light_level: ライトレベル
        """
        return self.__v[light_level]


class VolumeSeparatValue:
    """ボリューム区分値"""

    POOR: int = const(6553)
    LOW: int = const(19660)
    MIDDLE: int = const(32767)
    HIGH: int = const(45874)
    MAX: int = const(58981)
