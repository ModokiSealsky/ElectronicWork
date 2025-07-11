class NoteValue:
    """音符の値を保持するクラス"""

    def __init__(self, length: int, hz: float, is_staccato: bool=False):
        """コンストラクタ

        Args:
            length: 音符の長さ
            hz: 周波数
            is_staccato: スタッカート付きフラグ
        """
        self._length = length
        self._hz = hz
        self._is_staccato = is_staccato

    def get_length(self):
        """音符の長さを取得する

        Returns:
            int: 音符の長さ
        """
        return self._length

    def get_hz(self):
        """音の周波数を取得する

        Returns:
            str: 周波数
        """
        return self._hz

    def is_staccato(self):
        """スタッカート付きフラグを取得する

        Returns:
            bool: スタッカート付きフラグ
        """
        return self._is_staccato

    def __str__(self):
        """音符の情報文を取得する"""
        return "len:{0} score:{1} st:{2}".format(self._length, self._hz, self._is_staccato)
