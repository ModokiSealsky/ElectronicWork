import utime
import  _thread

from machine import Pin, I2C

class ScoreBord:
    """I2Cを利用するスコアボードのインターフェース"""
    def __init__(self,
                 i2c_ch: int,
                 scl_pin_no: int,
                 sda_pin_no: int):
        """初期化

            Args:
                i2c_ch: I2Cチャネル
                scl_pin_no: 使用するSCLピン番号
                sda_pin_no: 使用するSDAピン番号
        """
        print("Use Empty ScoreBord")

    def set_i2c_addr(self, addr: int):
        """ I2Cスレーブアドレス設定
        
            Args:
                addr: I2Cスレーブアドレス
        """
        print("O2C Address:{0}".format(addr))

    def display_off(self):
        """ ディスプレイ消灯 """
        print("Display Off")

    def output_score(self, score: int):
        """スコア更新

            Args:
                score: 現在の点数
        """
        print("score:{0}".format(score))

    def score_update_thread_start(self):
        """スコア更新スレッド開始"""
        print("Score Update Start")

    def scre_update_thread_stop(self):
        """スコア更新スレッド停止"""
        print("Score Update Stop")

    def output_message(self, message: str):
        """メッセージ表示"""
        print("message:{0}".format(message))

    def output_foul(self):
        """失敗表示"""
        print("FOUL!!")

    def display_check(self):
        """全ビット表示確認"""
        print("Display Check")
