import random
from micropython import const


from color_matching_game.game_const import LightLevel


class QuestionGenerator:
    """問題生成クラス"""

    __PATTERN_CNT = [const(2), const(3), const(4), const(6)]
    """パターン数[EASY, NORMAL, HARD, EXPERT]"""

    def __init__(self):
        self.__befor_color_lv = [LightLevel.OFF, LightLevel.OFF, LightLevel.OFF]

    def get_question_rgb_level(self) -> list[int]:
        """問題色取得"""
        off_cnt = 0
        dep_cnt = 0
        while True:
            q = [
                self.__get_convert_level(),
                self.__get_convert_level(),
                self.__get_convert_level(),
            ]
            if q == [LightLevel.OFF, LightLevel.OFF, LightLevel.OFF]:
                off_cnt += 1
            elif q == self.__befor_color_lv:
                dep_cnt += 1
            else:
                self.__befor_color_lv = q
                print(f"off:{off_cnt}, dep:{dep_cnt}, rgb:{q[0]},{q[1]},{q[2]}")
                return q

    def __get_convert_level(self) -> int:
        """カラーレベル取得"""
        return random.randrange(self.__PATTERN_CNT[3])


class QuestionGeneratorForEasy(QuestionGenerator):
    """EASY用問題生成クラス"""

    def __get_convert_level(self) -> int:
        return (
            LightLevel.OFF
            if random.randrange(self.__PATTERN_CNT[0])
            else LightLevel.MAX
        )


class QuestionGeneratorForNormal(QuestionGenerator):
    """NORMAL用問題生成クラス"""

    def __get_convert_level(self) -> int:
        level = random.randrange(self.__PATTERN_CNT[1])
        if level < 1:
            return LightLevel.OFF
        elif level < 2:
            return LightLevel.MIDDLE
        else:
            return LightLevel.MAX


class QuestionGeneratorForHard(QuestionGenerator):
    """HARD用問題生成クラス"""

    def __get_convert_level(self) -> int:
        level = random.randrange(self.__PATTERN_CNT[2])
        if level < 2:
            if level < 1:
                return LightLevel.OFF
            else:
                return LightLevel.LOW
        else:
            if level < 3:
                return LightLevel.HIGH
            else:
                return LightLevel.MAX


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    print("easy ----")
    e = QuestionGeneratorForEasy()
    for i in range(20):
        e.get_question_rgb_level()
    print("normal ----")
    n = QuestionGeneratorForNormal()
    for i in range(30):
        n.get_question_rgb_level()
    print("hard ----")
    h = QuestionGeneratorForHard()
    for i in range(50):
        h.get_question_rgb_level()
    print("expart ----")
    e = QuestionGenerator()
    for i in range(100):
        e.get_question_rgb_level()
    print("test end   ----")
