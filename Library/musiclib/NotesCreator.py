from micropython import const

from picolib import PwmBuzzer
from musiclib import NoteDict, NoteValue

class NotesCreator:
    """楽曲配列生成クラス"""

    __Q_LEN = 480
    """4分音符分解能(MIDI規格の480)"""
    __ST_LEN = 50
    """スタッカートの長さ(ミリ秒)"""

    __bpm: int = 120
    """BPM(デフォルトは120)"""
    __wight_len: int = 50
    """音符終端の空白長(ミリ秒)"""

    """BPM(デフォルトは120)"""

    def set_bpm(self, bpm: int):
        """BPMを設定する

        Args:
            bpm (int): BPM
        """
        self.__bpm = bpm

    def set_wight_len(self, len: int):
        """音符終端の空白長を設定する

        Args:
            len (int): 音符終端の空白長(ミリ秒)
        """
        self.__wight_len = len

    def create_for_pwm(self, notes: list[NoteValue]):
        """PwmBuzzer向け楽曲配列を作成する

        Args:
            notes: NoteValue配列
        """
        print("bpm:{0}".format(self.__bpm))
        # 1分に4分音符が何個入るのかを求め、4分音符の分解能で除算して音符の長さを求めるための比率を出す
        len_ratio: float = const((60 * 1000 / self.__bpm) / self.__Q_LEN)
        print("len_ratio:{0}".format(len_ratio))
        w_len = self.__wight_len
        music_array = []
        for note in notes:
            len = int(note.get_length() * len_ratio)
            if len < self.__wight_len:
                len = self.__wight_len
            print("{0} -> len:{1}".format(note, len))
            if note.is_staccato():
                # スタッカートの場合は鳴る長さ固定
                music_array.append(
                    PwmBuzzer.Note(self.__ST_LEN, int(note.get_hz()), len - self.__ST_LEN))
            else:
                music_array.append(
                    PwmBuzzer.Note(len - w_len, int(note.get_hz()), w_len))
        return music_array

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    dic = NoteDict()
    notes_input = [
        NoteValue(dic.get_length("QP"), dic.get_hz_by_scale("D#6")),
        NoteValue(dic.get_length("Q"), dic.get_hz_by_scale("D6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("D6"), True),
        NoteValue(dic.get_length("H"), dic.get_hz_by_scale("C6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("D#6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("D6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("C6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("D#6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("D6")),
        NoteValue(dic.get_length("E"), dic.get_hz_by_scale("C6")),
        NoteValue(dic.get_length("QP"), dic.get_hz_by_scale("G6")),
        NoteValue(dic.get_length("QP"), dic.get_hz_by_scale("G6")),
        NoteValue(dic.get_length("W"), dic.get_hz_by_scale("G6"))
    ]
    creator = NotesCreator()
    creator.set_bpm(156)
    music_notes = creator.create_for_pwm(notes_input)
    p_buzzer = PwmBuzzer(0)
    p_buzzer.play_music(music_notes)
    print("test end   ----")
