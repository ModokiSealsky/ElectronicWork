from machine import ADC
import time

from picolib import ColorLed, PwmBuzzer, TriggerButton

from .color_level_converter import (
    ColorLevelConvertor,
    ColorLevelConvertorForEasy,
    ColorLevelConvertorForNormal,
    ColorLevelConvertorForHard,
)
from .display import ScoreBord, TimeBord
from .game_const import GameMode
from .question_generator import (
    QuestionGeneratorForEasy,
    QuestionGeneratorForNormal,
    QuestionGeneratorForHard,
    QuestionGenerator,
)
from .hint_generator import (
    HintGenerator,
    HintGeneratorForEasy,
    HintGeneratorForNormal,
    HintGeneratorForHard,
)


class ColorMatchingGame:
    """色合わせゲームクラス"""

    __GAME_TIME_MS = 9999
    """ゲーム時間ミリ秒"""

    __FLIP_MS = 10
    """処理間隔ミリ秒"""

    __color_values: list[int] = [0x00, 0x33, 0x66, 0x99, 0xCC, 0xFF]
    """色値のセット"""

    __mastere_color: list[int] = [0x00, 0x00, 0x00]
    """マスターおばけの色"""

    __player_color: list[int] = [0x00, 0x00, 0x00]
    """プレイヤーおばけの色"""

    __game_level = GameMode.NORMAL
    """ゲームレベル"""

    __color_level_converters: dict[int, ColorLevelConvertor] = {
        GameMode.EASY: ColorLevelConvertorForEasy(),
        GameMode.NORMAL: ColorLevelConvertorForNormal(),
        GameMode.HARD: ColorLevelConvertorForHard(),
        GameMode.EXPERT: ColorLevelConvertor(),
    }
    """カラーレベル変換クラス種類"""
    __color_level_converter: ColorLevelConvertor = __color_level_converters[
        GameMode.NORMAL
    ]
    """カラーレベル変換クラス"""

    __question_generators: dict[int, QuestionGenerator] = {
        GameMode.EASY: QuestionGeneratorForEasy(),
        GameMode.NORMAL: QuestionGeneratorForNormal(),
        GameMode.HARD: QuestionGeneratorForHard(),
        GameMode.EXPERT: QuestionGenerator(),
    }
    """問題生成クラス種類"""
    __question_generator: QuestionGenerator = __question_generators[GameMode.NORMAL]
    """問題生成クラス"""

    __hint_generators: dict[int, HintGenerator] = {
        GameMode.EASY: HintGeneratorForEasy(),
        GameMode.NORMAL: HintGeneratorForNormal(),
        GameMode.HARD: HintGeneratorForHard(),
        GameMode.EXPERT: HintGenerator(),
    }
    """ヒント生成クラス種類"""
    __hint_generator: HintGenerator = __hint_generators[GameMode.NORMAL]
    """ヒント生成クラス"""

    def __init__(self):
        """コンストラクタ"""
        self.__setting_status = {
            "volume": False,
            "color_led": False,
            "buzzer": False,
            "button": False,
            "score_bord": False,
            "time_bord": False,
        }

    # 初期化 ===========================================================
    def set_game_level(self, game_mode: int):
        """ゲームレベル設定
        Args:
            game_level: ゲームレベル("EASY", "NORMAL", "HARD", "EXPERT")
        """
        self.__game_level = game_mode
        self.__color_level_converter = self.__color_level_converters[game_mode]
        self.__hint_generator = self.__hint_generators[game_mode]

    def setInputVaolumes(self, red_volume: ADC, green_volume: ADC, blue_volume: ADC):
        """入力ボリュームピン設定
        Args:
            red_volume: 赤用ボリュームピンオブジェクト
            green_volume: 緑用ボリュームピンオブジェクト
            blue_volume: 青用ボリュームピンオブジェクト
        """
        self.__red_volume = red_volume
        self.__blue_volume = blue_volume
        self.__green_volume = green_volume
        self.__setting_status["volume"] = True

    def setColorLeds(
        self, master_led: ColorLed, player_led: ColorLed, support_led: ColorLed
    ):
        """色LEDピン設定
        Args:
            master_led: マスターおばけ用LEDオブジェクト
            player_led: プレイヤーおばけ用LEDオブジェクト
            support_led: ヒントおばけ用LEDオブジェクト
        """
        self.__char_master = master_led
        self.__char_player = player_led
        self.__char_support = support_led
        self.__char_master.off()
        self.__char_player.off()
        self.__char_support.off()
        self.__setting_status["color_led"] = True

    def setBuzzer(self, buzzer: PwmBuzzer):
        """ブザー設定
        Args:
            buzzer: ブザーオブジェクト
        """
        self.__buzzer = buzzer
        self.__setting_status["buzzer"] = True

    def set_button(self, button: TriggerButton):
        """ボタン設定
        Args:
            button: ボタンオブジェクト
        """
        self.__anser_button = button
        self.__setting_status["button"] = True

    def set_scorebord(self, scorebord: ScoreBord):
        """スコアボード設定
        Args:
            scorebord: スコアボードオブジェクト
        """
        self.__scorebord = scorebord
        self.__setting_status["score_bord"] = True

    def set_timebord(self, timebord: TimeBord):
        """タイムボード設定
        Args:
            timebord: タイムボードオブジェクト
        """
        self.__timebord = timebord
        self.__setting_status["time_bord"] = True

    def __init_chek(self):
        """初期設定確認"""
        if (
            not self.__setting_status["volume"]
            or not self.__setting_status["color_led"]
            or not self.__setting_status["buzzer"]
            or not self.__setting_status["button"]
            or not self.__setting_status["score_bord"]
            or not self.__setting_status["time_bord"]
        ):
            print("初期設定不足")
            return False
        return True

    # 色設定 ===========================================================
    def __setPlayerColor(self):
        """プレイヤー色設定"""
        r_u16 = self.__red_volume.read_u16()
        g_u16 = self.__green_volume.read_u16()
        b_u16 = self.__blue_volume.read_u16()

        red_value = self.__color_level_converter.get_color_level(r_u16)
        green_value = self.__color_level_converter.get_color_level(g_u16)
        blue_value = self.__color_level_converter.get_color_level(b_u16)
        print(
            f"player color r:{r_u16:05}->{red_value}, {g_u16:05}->g:{green_value}, b:{b_u16:05}->{blue_value}"
        )
        self.__char_player.on_rgb(
            self.__color_values[red_value],
            self.__color_values[green_value],
            self.__color_values[blue_value],
        )

    def __nextQuestion(self):
        """次の問題設定"""
        q_rgb = self.__question_generator.get_question_rgb_level()
        h_rgb = self.__hint_generator.get_hint(q_rgb[0], q_rgb[1], q_rgb[2])
        self.__char_master.on_rgb(
            self.__color_values[q_rgb[0]],
            self.__color_values[q_rgb[1]],
            self.__color_values[q_rgb[2]],
        )
        self.__char_support.on_rgb(
            self.__color_values[h_rgb[0]],
            self.__color_values[h_rgb[1]],
            self.__color_values[h_rgb[2]],
        )

    # 効果音処理 =========================================================
    def __ok_sound(self):
        """正解効果音"""
        self.__buzzer.hz_beep(100, 3000)
        self.__buzzer.hz_beep(100, 1000)

    def __ng_sound(self):
        """不正解効果音"""
        self.__buzzer.hz_beep(100, 1000)
        time.sleep_ms(100)
        self.__buzzer.hz_beep(100, 1000)

    # ゲーム処理 =========================================================
    def __start_animation(self):
        """ゲーム開始アニメーション"""
        print("start animation")

    def __end_animation(self):
        """ゲーム終了アニメーション"""
        print("end animation")

    def game_start(self):
        """ゲーム開始"""
        if not self.__init_chek():
            return
        print(f"game level:{self.__game_level}")
        last_time = self.__GAME_TIME_MS
        score = 0
        self.__scorebord.set_score(score)
        self.__start_animation()
        self.__nextQuestion()
        while last_time > 0:
            self.__timebord.set_time(last_time)
            self.__setPlayerColor()
            self.__anser_button.refresh()
            if self.__anser_button.is_on_trriger:
                if self.__mastere_color == self.__player_color:
                    self.__ok_sound()
                    score += 1
                    self.__scorebord.set_score(score)
                    print(f"score:{score}")
                    self.__nextQuestion()
                else:
                    self.__ng_sound()
            time.sleep_ms(self.__FLIP_MS)
            last_time -= self.__FLIP_MS
        # 終了処理
        self.__end_animation()
        self.__char_master.off()
        self.__char_player.off()
        self.__char_support.off()
