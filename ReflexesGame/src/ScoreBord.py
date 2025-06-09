from machine import Pin,I2C
import utime

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
        "A": 0b01110111,
        "C": 0b00111001,
        "E": 0b01111001,
        "F": 0b01110001,
        "H": 0b01110110,
        "L": 0b00111000,
        "O": 0b00111111,
        "U": 0b00111110,
        }
    """ 表示可能文字設定 """

    def __init__(self, i2c_ch:int, scl_pin_no:int, sda_pin_no:int, is_debug = False):
        """初期化

            Args:
                i2c_ch: I2Cチャネル
                scl_pin_no: 使用するSCLピン番号
                sda_pin_no: 使用するSDAピン番号
        """
        if is_debug:
            return
        self._i2c = I2C(i2c_ch, scl=Pin(scl_pin_no), sda=Pin(sda_pin_no), freq=100000)

    def setI2cAddr(self, addr):
    def setI2cAddr(self, addr, is_debug = False):
        """ I2Cスレーブアドレス設定
        
            Args:
                addr: I2Cスレーブアドレス
        """
        self._addr = addr
        if is_debug:
            return
        self._i2c.writeto_mem(self._addr, 0x21, bytes(0x01)) # システムクロック有効
        self._i2c.writeto_mem(self._addr, 0x81, bytes(0x01)) # ディスプレイON

    def displayOff(self):
        """ ディスプレイ消灯 """
        self._i2c.writeto_mem(self._addr, 0x80, bytes(0x01)) # ディスプレイOFF

    def output(self, score:int, is_debug = False):
        """ 点数出力
        
            Args:
                score: 点数(-999 <= score <= 9999のみ表示可能)
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

    def outputFoul(self):
        """失敗表示"""
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_1, bytes([self._CHAR["F"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_2, bytes([self._CHAR["O"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_3, bytes([self._CHAR["U"]]))
        self._i2c.writeto_mem(self._addr, self._DIG_ADDR_4, bytes([self._CHAR["L"]]))


# ==================
# テストコード
# ================== 
def countup(clz:ScoreBord):
    """ カウントアップ表示確認 """
    for cnt in range(10000):
        clz.output(cnt)
        utime.sleep_ms(1)

if __name__  == "__main__":
    print("test start ----")
    # ==================
    # I2C確認
    # ================== 
    clz = ScoreBord(0 , 1, 0)
    i2c_addr_list = clz._i2c.scan()
    i2c_addr = i2c_addr_list[0]
    print("i2c_addr:{:#x}".format(i2c_addr))
    clz.setI2cAddr(0x70)
    print("addr:{:#x}".format(clz._addr))
    # ==================
    # 表示確認
    # ==================
    clz.output(-1000)
    utime.sleep(1)
    clz.output(-999)
    utime.sleep(1)
    clz.output(0)
    utime.sleep(1)
    clz.output(1)
    utime.sleep(1)
    clz.output(1234)
    utime.sleep(1)
    clz.output(0000)
    utime.sleep(1)
    clz.output(1111)
    utime.sleep(1)
    clz.output(2222)
    utime.sleep(1)
    clz.output(3333)
    utime.sleep(1)
    clz.output(4444)
    utime.sleep(1)
    clz.output(5555)
    utime.sleep(1)
    clz.output(6666)
    utime.sleep(1)
    clz.output(7777)
    utime.sleep(1)
    clz.output(8888)
    utime.sleep(1)
    clz.output(9999)
    utime.sleep(1)
    clz.output(10000)
    utime.sleep(1)
    clz.displayOff()
    print("test end   ----")
