import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import numpy as np


class fi:
    def __init__(self, findimgname, sx, sy, ex, ey, masktf=True):

        self.sx, self.sy, self.ex, self.ey = sx, sy, ex, ey
        self.masktf = masktf
        self.find = cv.imread(f'{findimgname}', cv.IMREAD_GRAYSCALE)
        if self.masktf:
            self.ms = cv.imread(f'{findimgname}', cv.IMREAD_GRAYSCALE)
        self.w, self.h = self.find.shape[::-1]

    def re(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.sy, self.ex:self.ey], cv.COLOR_BGR2GRAY)
        if self.masktf:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)
        else:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)
        mxy = list(mxy)

        return mxy

    def rei(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.sy, self.ex:self.ey], cv.COLOR_BGR2GRAY)
        if self.masktf:
            res = cv.matchTemplate(cutimgy, self.find,
                                   cv.TM_CCORR_NORMED, mask=self.ms)
        else:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy


def creen():
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hdc = win32gui.GetWindowDC(hwnd)

    uihdc = win32ui.CreateDCFromHandle(hdc)

    cDC = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w, h)

    cDC.SelectObject(cbmp)
    cDC.BitBlt((0, 0), (w, h), uihdc, (0, 0), win32con.SRCCOPY)
    signedIntsArray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    win32gui.DeleteObject(cbmp.GetHandle())
    cDC.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img


hwnd = win32gui.FindWindow(None, 'Grand Theft Auto V')
left, top, right, bot = win32gui.GetWindowRect(hwnd)
hdc = win32gui.GetDC(hwnd)

while True:
    cren = creen()
    for i in range(4):
        find = cv.imread(f'gta\\fp{i}.png', cv.IMREAD_GRAYSCALE)
        w, h = find.shape[::-1]
        cutimgy = cv.cvtColor(cren[170:690, 970:1320], cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(cutimgy, find, cv.TM_CCOEFF_NORMED)
        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)


        if maxval > 0.9:
            for e in range(4):
                resul = fi(f'gta\\fp{i}\\{e}.png', 270, 860, 450, 780, False).rei(cren)
                sx = int(resul[2][0]) + 450
                sy = int(resul[2][1]) + 270
                win32gui.Rectangle(hdc, sx, sy, sx + 50, sy + 50)
    cv.waitKey(1)
