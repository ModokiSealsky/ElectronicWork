"""ヒント生成クラスパッケージ"""


class HintGenerator:
    """ヒント生成クラス"""

    def getHint(self, r, g, b):
        """ヒント取得
        Args:
            r: 赤色値
            g: 緑色値
            b: 青色値
        """
        # グレースケール変換(BT.601)して返す
        gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
        return (gray_value, gray_value, gray_value)


class HintGeneratorForEasy(HintGenerator):
    """EASY用ヒント生成クラス"""

    def getHint(self, r, g, b):
        # 赤のみを返す
        return (r, 0x00, 0x00)


class HintGeneratorForNormal(HintGenerator):
    """NORMAL用ヒント生成クラス"""

    def getHint(self, r, g, b):
        # 緑のみを返す
        return (0x00, g, 0x00)


class HintGeneratorForHard(HintGenerator):
    """HARD用ヒント生成クラス"""

    def getHint(self, r, g, b):
        # 青のみを返す
        return (0x00, 0x00, b)
