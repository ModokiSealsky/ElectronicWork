from matrixlib.MatrixCharactor8px import MatrixCharactor8px
from matrixlib.MatrixCharactor16px import MatrixCharactor16px


class MatrixCharactor:
    def __init__(self, is_16px: bool = False):
        """コンストラクタ

        Args:
            is_16px: マトリクスサイズを16pxに設定するか(デフォルトは8px)
        """
        if is_16px:
            self.set_size_16px()
        else:
            self.set_size_8px()

    def set_size_8px(self):
        """マトリクスサイズを8pxに設定する"""
        self.__pettern = MatrixCharactor8px()

    def set_size_16px(self):
        """マトリクスサイズを16pxに設定する"""
        self.__pettern = MatrixCharactor16px()

    def get_pattern(self, key: str) -> list[int]:
        """文字のビットパターンを取得する

        Args:
            key (str): 文字
        """
        return self.__pettern.get_pattern(key)
