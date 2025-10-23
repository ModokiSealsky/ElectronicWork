from micropython import const

from color_matching_game.game_const import LightLevel, VolumeSeparatValue


class ColorLevelConvertor:
    """カラーレベル変換クラス"""

    def get_colr_level(self, volume_u16: int) -> int:
        """カラーレベル取得
        Args:
            volume_u16: ボリューム値(u16)
        """
        if volume_u16 < VolumeSeparatValue.POOR:
            return LightLevel.OFF
        if volume_u16 < VolumeSeparatValue.LOW:
            return LightLevel.POOR
        if volume_u16 < VolumeSeparatValue.MIDDLE:
            return LightLevel.LOW
        if volume_u16 < VolumeSeparatValue.HIGH:
            return LightLevel.MIDDLE
        if volume_u16 < VolumeSeparatValue.MAX:
            return LightLevel.HIGH
        return LightLevel.MAX


class ColorLevelConvertorForEasy(ColorLevelConvertor):
    """EASY用カラーレベル変換クラス"""

    def get_colr_level(self, volume_u16: int) -> int:
        if volume_u16 < VolumeSeparatValue.MIDDLE:
            return LightLevel.OFF
        else:
            return LightLevel.MAX


class ColorLevelConvertorForNormal(ColorLevelConvertor):
    """NORMAL用カラーレベル変換クラス"""

    def get_colr_level(self, volume_u16: int) -> int:
        if volume_u16 < VolumeSeparatValue.LOW:
            return LightLevel.OFF
        elif volume_u16 < VolumeSeparatValue.HIGH:
            return LightLevel.MIDDLE
        else:
            return LightLevel.MAX


class ColorLevelConvertorForHard(ColorLevelConvertor):
    """HARD用カラーレベル変換クラス"""

    def get_colr_level(self, volume_u16: int) -> int:
        if volume_u16 < VolumeSeparatValue.POOR:
            return LightLevel.OFF
        elif volume_u16 < VolumeSeparatValue.MIDDLE:
            return LightLevel.MIDDLE
        elif volume_u16 < VolumeSeparatValue.HIGH:
            return LightLevel.HIGH
        else:
            return LightLevel.MAX


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    from machine import ADC
    import time

    print("test start ----")
    cnv_list = [
        ColorLevelConvertor(),
        ColorLevelConvertorForEasy(),
        ColorLevelConvertorForNormal(),
        ColorLevelConvertorForHard(),
    ]
    volume_1 = ADC(0)
    volume_2 = ADC(1)
    volume_3 = ADC(2)
    for cnv in cnv_list:
        print(cnv)
        for i in range(20):
            v1 = volume_1.read_u16()
            v2 = volume_2.read_u16()
            v3 = volume_3.read_u16()
            l1 = cnv.get_colr_level(v1)
            l2 = cnv.get_colr_level(v2)
            l3 = cnv.get_colr_level(v3)
            print(f"R:{v1}-{l1}|G:{v2}-{l2}|B:{v3}-{l3}")
            time.sleep(1)
    print("test end   ----")
