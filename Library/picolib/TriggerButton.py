from picolib.InputSwitch import InputSwitch


class TriggerButton(InputSwitch):
    """トリガー判定付き入力スイッチクラス"""

    def __init__(self, pin_no: int, is_pull_up: bool = False, is_reverse: bool = False):
        """
        Args:
            pin_no: GPIOピン番号
            is_pull_up: PullUp指定(回路をプルアップ、スイッチの先がGNDで組む場合にTrue)
            is_reverse: ON/OFF逆転指定
        """
        super().__init__(pin_no, is_pull_up, is_reverse)
        self._is_before_on: bool = False
        self._on_torriger: bool = False
        self._off_torriger: bool = False

    def refresh(self):
        """トリガー更新"""
        is_on = self.is_on()
        if self._is_before_on == is_on:
            self._on_torriger = False
            self._off_torriger = False
        elif is_on:
            self._on_torriger = True
            self._off_torriger = False
        else:
            self._on_torriger = False
            self._off_torriger = True
        self._is_before_on = is_on

    def is_on_trriger(self):
        """スイッチがONになった瞬間かを確認

        refresh_torrigerでトリガー更新済みの状態で実行する。
        """
        return self._on_torriger

    def is_off_trriger(self):
        """スイッチがOFFになった瞬間かを確認

        refresh_torrigerでトリガー更新済みの状態で実行する。
        """
        return self._off_torriger

    def __print_value(self, cnt: int):
        self.refresh()
        print(
            "btn on:{0}/off:{1} | trriger on:{2}/off:{3} | cnt:{4}".format(
                self.is_on(),
                self.is_off(),
                self.is_on_trriger(),
                self.is_off_trriger(),
                cnt,
            )
        )


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test down normal ----")
    cls = TriggerButton(0)
    cls.test()
    print("test up normal ----")
    cls = TriggerButton(0, True)
    cls.test()
    print("test down reverse ----")
    cls = TriggerButton(0, False, True)
    cls.test()
    print("test up reverse ----")
    cls = TriggerButton(0, True, True)
    cls.test()
