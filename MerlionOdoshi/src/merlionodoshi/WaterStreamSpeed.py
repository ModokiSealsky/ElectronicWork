from micropython import const

class WaterStreamSpeed:
    """水流速度の定数"""
    SLOW = const(0)
    """低速"""
    FAST = const(1)
    """高速"""
    HYPER = const(2)
    """爆速"""
