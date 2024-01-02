import time
from ctypes import *
import os

key_mapping = {
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    "a": 65,
    "b": 66,
    "c": 67,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "l": 76,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "v": 86,
    "w": 87,
    "x": 88,
    "y": 89,
    "z": 90,
    "delete": 46,
    "space": 32,
    "tab": 9,
    "enter": 13,
    "backSpace": 8,
    "esc": 27,
    "capsLock": 20,
    "printscreen": 44,
    "scrolllock": 145,
    "pause": 19,
    "insert": 45,
    "home": 36,
    "end": 35,
    "pageUp": 33,
    "pageDown": 34,
    "eight": 39,
    "left": 37,
    "down": 40,
    "up": 38,
    "numLock": 144,
    "num0": 96,
    "num1": 97,
    "num2": 98,
    "num3": 99,
    "num4": 100,
    "num5": 101,
    "num6": 102,
    "num7": 103,
    "num8": 104,
    "num9": 105,
    "numDot": 110,
    "numEnter": 13,
    "numAdd": 107,
    "numDec": 109,
    "numMul": 106,
    "numDiv": 111,
    "ctrl": 17,
    "shift": 16,
    "alt": 18,
    "win": 91,
    "rctrl": 17,
    "rshift": 16,
    "ralt": 18,
    "RGUI": 93
}


os.add_dll_directory(os.getcwd())
try:
    dll = windll.LoadLibrary(r"gbild64.dll")
    print('正在加载64位DLL')
except OSError:
    dll = windll.LoadLibrary(r"gbild32.dll")
    print('正在加载32位DLL')
dll.getmodel.restype = c_char_p
dll.getserialnumber.restype = c_char_p
dll.getproductiondate.restype = c_char_p
dll.getfirmwareversion.restype = c_char_p


class s_device:

    def __init__(self):
        dll.opendevice(0)
        connection = dll.isconnected()
        if connection:
            print('设备连接成功')
        else:
            print('设备连接失败')
            dll.closedevice()
            return
        device_name = dll.getmodel().decode("utf-8")
        print(f'正在使用的设备为：{device_name}')
        serialnumber = dll.getserialnumber().decode("utf-8")
        print(f'设备序列号为：{serialnumber}')
        productiondate = dll.getproductiondate().decode("utf-8")
        print(f'设备生产日期为：{productiondate}')
        firmwareversion = dll.getfirmwareversion().decode("utf-8")
        print(f'设备固件版本为：{firmwareversion}')


    def end(self):
        code = dll.closedevice()
        print(f'设备关闭{code}')
        return code

    def reset(self):
        code = dll.resetdevice()
        print(f'设备重置{code}')
        return code

    """鼠标操作"""

    def set_click_delay(self, delay: tuple):
        """
        设置点击延迟
        :param delay: tuple 默认：(30, 100) 单位：ms
        :return:
        """
        code = dll.setpressmousebuttondelay(delay[0], delay[1])
        return code

    def set_move_delay(self, delay: tuple):
        """
        设置移动延迟
        :param delay: tuple 默认：(4, 8) 单位：ms
        :return:
        """
        code = dll.setmousemovementdelay(delay[0], delay[1])
        return code

    def setmouse_speed(self, speed: int):
        """
        设置鼠标移动速度
        :param speed: int 默认：7 范围：1-10
        :return:
        """
        code = dll.setmousemovementspeed(speed)
        return code

    def set_move_method(self, method: int):
        """
        设置鼠标移动方式
        :param method: int 默认：1 范围：1-3
        :return:
        1 直线移动（原移动方式，默认）

        2 曲线移动（贝塞尔曲线）

        3 极速移动（以最快速度移动到目标坐标）

        """
        code = dll.setmousemovementmode(method)
        return code

    def rel_move(self, x: int, y: int):
        """
        相对移动, 最大范围-127~127
        :param x:
        :param y:
        :return:
        """
        step = 100
        if abs(x) < step and abs(y) < step:
            code = dll.movemouserelative(x, y)
        elif abs(x) < step and abs(y) >= step:
            times = abs(y) // step
            code = dll.movemouserelative(x, y % step)
            for i in range(times):
                code = dll.movemouserelative(0, step)
        elif abs(x) >= step and abs(y) < step:
            times = abs(x) // step
            code = dll.movemouserelative(x % step, y)
            for i in range(times):
                code = dll.movemouserelative(step, 0)
        else:
            times_x = abs(x) // step
            times_y = abs(y) // step
            fx = int(x/abs(x))
            fy = int(y/abs(y))
            # print(fx, fy)
            code = dll.movemouserelative(x % step, y % step)
            min = times_x if times_x < times_y else times_y
            max = times_x if times_x > times_y else times_y
            for i in range(min):
                code = dll.movemouserelative(fx*step, fy*step)
            if times_x > times_y:
                for i in range(max - min):
                    code = dll.movemouserelative(fx*step, 0)
            else:
                for i in range(max - min):
                    code = dll.movemouserelative(0, fy*step)

        return code

    def moveto(self, x: int, y: int):
        now_pos = self.get_pos()
        dx = x - now_pos[0]
        dy = y - now_pos[1]
        code = self.rel_move(dx, dy)
        # 下面是setpos方式，部分游戏不好用
        # code = dll.movemouseto(x, y)
        return code

    def click(self):
        code = dll.pressmousebutton(1)
        return code

    def right_click(self):
        code = dll.pressmousebutton(2)
        return code

    def scroll(self, num: int):
        code = dll.movemousewheel(num)
        return code

    def get_pos(self):
        x = dll.getmousex()
        y = dll.getmousey()
        return x, y

    def set_pos(self, x: int, y: int):
        code = dll.setmouseposition(x, y)
        return code

    """键盘操作"""

    def setpresskeydelay(self, delay: tuple):
        """
        设置按键延迟
        :param delay: tuple 默认：(30, 100) 单位：ms
        :return:
        """
        code = dll.setpresskeydelay(delay[0], delay[1])
        return code

    def set_string_delay(self, delay: tuple):
        """
        设置字符串延迟
        :param delay: tuple 默认：(60, 200) 单位：ms
        :return:
        """
        code = dll.setinputstringintervaltime(delay[0], delay[1])
        return code

    def check_key_state(self, key: str):
        """
        检查某个键的状态
        :param key: str
        :return: bool
        """
        return dll.iskeypressedbyvalue(key_mapping[key])

    def keydown(self, key: str):
        code = dll.presskeybyvalue(key_mapping[key])
        return code

    def keyup(self, key: str):
        code = dll.releasekeybyvalue(key_mapping[key])
        return code

    def press(self, key: str):
        code = dll.pressandreleasekeybyvalue(key_mapping[key])
        return code

    def write_text(self, text: str):
        code = dll.inputstring(bytes(text, encoding="utf-8"))
        return code

    def release_all(self):
        code = dll.releaseallkey()
        return code

    def hold(self, key: str, time_ms: int):
        """
        按住某个键一段时间
        :param key: str
        :param time: ms
        :return:
        """
        dll.presskeybyvalue(key_mapping[key])
        time.sleep(time_ms / 1000)
        dll.releasekeybyvalue(key_mapping[key])


if __name__ == '__main__':
    d = s_device()
    # time.sleep(5)
    # d.moveto(100, 100)
    # d.write_text('xvbowen2012@gmail.com')
    # for i in range(50):
    d.moveto(100, 100)
    # d.rel_move(-100, -100)

    # while True:
    #     pos = d.get_pos()
    #     print(pos)
    d.end()