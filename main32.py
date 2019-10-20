import time
import adafruit_ht16k33.matrix
import board
import busio as io
import touchio

touch = touchio.TouchIn(board.D1)

i2c = io.I2C(board.SCL, board.SDA)
matrix = adafruit_ht16k33.matrix.Matrix8x8(i2c)

x_pix = y_pix = 8
matrix.fill(0)

xMask = [
  0b10000000,
  0b01000000,
  0b00100000,
  0b00010000,
  0b00001000,
  0b00000100,
  0b00000010,
  0b00000001,
]

f = [[
  0x01,
  0x02,
  0x04,
  0x08,
  0x10,
  0x20,
  0x40,
  0x80,
]]

def standard(x, y, pixel):
  return x, y, pixel


def invertPixel(x, y, pixel):
  return x, y, not pixel


def rotateLeft(x, y, pixel):
  return 7 - y, x, pixel


def rotateRight(x, y, pixel):
  return y, 7 - x, pixel

def rotate180(x, y, pixel):
  return 7 - x, 7 - y, pixel

def play(frames=f, delay=.05, rotate=standard):
  for frame in frames:
    for y, row in enumerate(frame):
      for x, mask in enumerate(xMask):
        pixel = row & mask == mask
        xPix, yPix, pixel = rotate(x, y, pixel)
        if pixel:
          matrix.pixel(xPix, yPix, 1)
        else:
          matrix.pixel(xPix, yPix, 0)
  matrix.show()
  time.sleep(delay)

stopped = False
sleepCount = 0
touchCount = 0
while True:
  if not stopped:
    play()
    play(f[::-1])
    play(rotate=invertPixel)
    play(f[0:5], .1, rotate=rotateRight)
    play(f[0:5], .1, rotate=rotate180)
    play(f[0:5], .1, rotate=rotateLeft)
    play()
    stopped = True
  else:
    matrix.fill(0)
    matrix.show()
    time.sleep(2)
    sleepCount = sleepCount + 1
    if touch.value:
      stopped = False
      if touchCount == 0:
        play(smile, delay=2)
      else:
        play(alien, delay=1)
      touchCount = 1 - touchCount
      sleepCount = 0
    if sleepCount >= 15:
      stopped = False
      sleepCount = 0
