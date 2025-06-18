import utime
import  _thread

from machine import Pin, I2C

class ScoreBord:
    """スコアボードクラス

        ４桁7SEGディスプレイへの表示を行う
    """
    _DIGIT = 4 # 4桁7SEG
    """ 表示桁数(4固定) """

    _DIG_ADDR_1 = 0
    """ 桁別addr:左から1桁目 """
    _DIG_ADDR_2 = 2
    """ 桁別addr:左から1桁目 """
    _DIG_ADDR_3 = 4
    """ 桁別addr:左から1桁目 """
    _DIG_ADDR_4 = 6
    """ 桁別addr:左から1桁目 """

    _score = 9999
    """スコア保持変数"""
    _score_upd_thread_status = False
    """スコア更新スレッド稼働状態"""

    _CHAR = {# .GFEDCBA
        "0": 0b00111111,
        "1": 0b00000110,
        "2": 0b01011011,
        "3": 0b01001111,
        "4": 0b01100110,
        "5": 0b01101101,
        "6": 0b01111101,
        "7": 0b00000111,
        "8": 0b01111111,
        "9": 0b01101111,
        "-": 0b01000000,
        " ": 0b00000000,
        "_": 0b00001000,
        "=": 0b01001000,
        "#": 0b01001001, # 三本横線
        "!": 0b10000010,
        "A": 0b01110111,
        "C": 0b00111001,
        "E": 0b01111001,
        "F": 0b01110001,
        "G": 0b00111101,
        "H": 0b01110110,
        "L": 0b00111000,
        "O": 0b00111111,
        "U": 0b00111110,
        }
    """ 表示可能文字辞書 """

    _FULLBIT = 0b11111111
    """全セグ点灯"""

    def __init__(self,
                 i2c_ch: int,
                 scl_pin_no: int,
                 sda_pin_no: int,
                 is_debug: bool = False):
        """初期化

            Args:
                i2c_ch: I2Cチャネル
                scl_pin_no: 使用するSCLピン番号
                sda_pin_no: 使用するSDAピン番号
                is_debug: デバッグモード(I2C出力無し)
        """
        if is_debug:
            return
        self._i2c = I2C(i2c_ch, scl=Pin(scl_pin_no), sda=Pin(sda_pin_no), freq=100000)
        print("I2C_ADDR:{0}".format(self._i2c.scan()))

    def set_eng_pin(self, eng_pin_no: int):
        """電圧出力ピン設定(GPIOで代用する場合)"""
        Pin(eng_pin_no, Pin.OUT).on()

    def set_i2c_addr(self, addr: int, is_debug: bool = False):
        """ I2Cスレーブアドレス設定
        
            Args:
                addr: I2Cスレーブアドレス
                is_debug: デバッグモード(I2C出力無し)
        """
        self._addr = addr
        if is_debug:
            return
        self._i2c.writeto_mem(self._addr, 0x21, bytes(0x01)) # システムクロック有効
        self._i2c.writeto_mem(self._addr, 0x81, bytes(0x01)) # ディスプレイON

    def display_off(self):
        """ ディスプレイ消灯 """
        self._i2c.writeto_mem(self._addr, 0x80, bytes(0x01)) # ディスプレイOFF

    def output_score(self, score: int, is_debug: bool = False):
        """スコア更新

            Args:
                is_debug: デバッグモード(I2C出力無し)
        """
        self._score = score
        if not self._score_upd_thread_status:
            # スレッド未起動の場合は同期更新
            self._output_score(score, is_debug)

    def _score_update_on_thread(self):
        """スレッド用スコア更新処理
        
            更新を止める場合はself._score_upd_thread_statusをFalseに変更する
        """
        print("Score Update Start")
        while self._score_upd_thread_status:
            self._output_score(self._score)
        self._output_score(self._score)
        print("Score Update Stop")

    def score_update_thread_start(self):
        """スコア更新スレッド開始"""
        if self._score_upd_thread_status:
            # 多重起動防止
            return
        self._score_upd_thread_status = True
        self._score_upd_thread = _thread.start_new_thread(self._score_update_on_thread, ())

    def scre_update_thread_stop(self):
        """スコア更新スレッド停止"""
        self._score_upd_thread_status = False
        print("Score Update Stop")

    def _output_score(self, score: int, is_debug: bool = False):
        """ 点数出力
        
            Args:
                score: 点数(-999 <= score <= 9999のみ表示可能)
                is_debug: デバッグモード(I2C出力無し)
        """
        if is_debug:
            return
        if score > 9999:
            print("OVER")
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR["H"]]))
            return
        elif score < -999:
            print("UNDER")
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR[" "]]))
            self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR["U"]]))
            return
        score_digit = list("{0:04}".format(score))
        # print(score_digit)
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR[score_digit[0]] | 0x80]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR[score_digit[1]]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR[score_digit[2]]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR[score_digit[3]]]))

    def output_message(self, message: str):
        """メッセージ表示"""
        char_list = list("{:4}".format(message))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR[char_list[0]]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR[char_list[1]]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR[char_list[2]]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR[char_list[3]]]))

    def output_foul(self):
        """失敗表示"""
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR["F"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR["O"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR["U"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR["L"]]))

    def display_check(self):
        """全ビット表示確認"""
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes(self._FULLBIT))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes(self._FULLBIT))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes(self._FULLBIT))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes(self._FULLBIT))
        utime.sleep(2)
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR[" "]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR[" "]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR[" "]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR[" "]]))

# ==================
# テストコード
# ================== 
def countup(cls: ScoreBord):
    """ カウントアップ表示確認 """
    print("Count Up Start")
    for cnt in range(10000):
        cls.output_score(cnt)
        utime.sleep_ms(1)
    print("Count Up End")

def countup_on_thread(cls: ScoreBord):
    """カウントアップ表示スレッド確認"""
    print("Count Up Thread Start")
    cls.output_score(0)
    cls.score_update_thread_start()
    for cnt in range(10000):
        cls.output_score(cnt)
        utime.sleep_ms(1)
    cls.scre_update_thread_stop()
    print("Count Up Thread End")

if __name__  == "__main__":
    print("test start ----")
    # ==================
    # I2C確認
    # ================== 
    cls = ScoreBord(0 , 21, 20)
    #clz.setEngPin(22)
    i2c_addr_list = cls._i2c.scan()
    i2c_addr = i2c_addr_list[0]
    print("i2c_addr:{:#x}".format(i2c_addr))
    cls.set_i2c_addr(0x70)
    print("addr:{:#x}".format(cls._addr))
    # ==================
    # 表示確認
    # ==================
    cls.display_check()
    utime.sleep(1)
    cls.output_score(-1000)
    utime.sleep(1)
    cls.output_score(-999)
    utime.sleep(1)
    cls.output_score(0)
    utime.sleep(1)
    cls.output_score(1)
    utime.sleep(1)
    cls.output_score(10000)
    utime.sleep(1)
    cls.output_foul()
    utime.sleep(1)
    # ==================
    # カウントアップ確認
    # ==================
    countup(cls)
    utime.sleep(1)
    countup_on_thread(cls)
    utime.sleep(1)
    cls.display_off()
    print("test end   ----")
