import pyxel as pl
from pyxel import *

import math as mt
# import numpy as np
# import random as rnd

######################################################################
# SW,SH=256,256
SW,SH=128,128
SWH,SHH=SW//2,SH//2
FPS=60

######################################################################
# def blt2(x, y, img, u, v, w, h, colkey=None, angle=0, scale=1, off=0.49, tu=0,tv=0,tuu=0,tvv=0):
def blt2(x, y, img, u, v, w, h, colkey=None, angle=0, scale=1, off=0.49):
  if not scale: scale = 1e-100

  src_W = w
  src_H = h
  dst_W = round(src_W*scale)
  dst_H = round(src_H*scale)

  src_CX = src_W/2
  src_CY = src_H/2
  dst_CX = dst_W/2
  dst_CY = dst_H/2

  du_Col = mt.sin(-angle) * (1.0 / scale)
  dv_Col = mt.cos(-angle) * (1.0 / scale)
  du_Row =  dv_Col
  dv_Row = -du_Col

  start_u = src_CX - (dst_CX * dv_Col + dst_CY * du_Col) - off
  start_v = src_CY - (dst_CX * dv_Row + dst_CY * du_Row) - off
  row_u = start_u
  row_v = start_v

  for py in range(dst_H):
    s_u = row_u
    s_v = row_v
    for px in range(dst_W):
      # if (s_u-u>0 and s_v-v>0 and s_u+u<dst_W and s_v+v<dst_H):
      # if True:
      c = img.pget(round(s_u+u), round(s_v+v))
      if c != colkey:
        pset(px+x - dst_CX, py+y - dst_CY, c)
      # else:
        # pset(px+x - dst_CX, py+y - dst_CY, 0)
      s_u += du_Row
      s_v += dv_Row
    row_u += du_Col
    row_v += dv_Col
  ...

def hypot(x, y): return(x ** 2 + y ** 2) ** 0.5
def hypotsq(x, y): return(x ** 2 + y ** 2)
def dot(ax,ay,bx,by): return(ax*bx+ay*by)
def cross(ax,ay,az,bx,by,bz): return(ay*bz-az*by, ax*bz-az*bx,ax*by-ay*bx)
def clamp(n, mn, mx): return max(min(n, mx), mn)
######################################################################
def bumpcirc(ax,ay,ar, bx,by,br): return not ((bx-ax)**2+(by-ay)**2)**0.5 > (ar+br)
def bumprect(ax,ay,aw,ah, bx,by,bw,bh): return abs((ax+aw) - (bx+bw)) < (aw+bw) and abs((ay+ah) - (by+bh)) < (ah+bh)

######################################################################
######################################################################
class Seg:
  def __init__(S, x=SWH, y=SH+32, r=-mt.pi):
    S.x = x
    S.y = y
    S.r = r
    # S.scale = 1
    # S.img = None
    # S.ani = None

class Nezu:
  def __init__(S, x, y):
    S.x = x
    S.y = y

######################################################################
class T:
  def __init__(S):
    S.t_s = [Seg(rndi(0,SW), rndi(0,SH))]
    for n in range(10):
      S.t_s.append(Seg(rndi(0,SW), rndi(0,SH)))
    ...

  def update(S):
    # if
    ...

  def draw(S):
    # for t in S.t_s:
    for n, t in enumerate(S.t_s):
      circ(t.x, t.y, 2, (n%15)+1)
    ...

######################################################################
class L:
  def __init__(S, img, x=SWH, y=SH+32, r=-mt.pi):
    S.img = img

    S.seg_s = [Seg(x, y, r)]
    S.vel = 1.5
    S.acc = 0.1
    S.vel_max = 2
    S.len = len(S.seg_s)

    for n in range(32):
      S.seg_s.append(Seg())
    ...

  def update(S, nezu):
    # for s in S.seg_s:
    # for n, s in enumerate(S.seg_s):
    # for n in range(len(S.seg_s)):
    for n in range(len(S.seg_s)-1, -1, -1):

      s = S.seg_s

      if n == 0:
        sm = nezu
      else:
        sm = s[n-1]
      si = s[n]

      dx = sm.x - si.x
      dy = sm.y - si.y

      r = mt.atan2(dy, dx)

      if hypotsq(dx, dy) >= 128:
        if n == 0:
          r += mt.sin(pl.frame_count/16)/2
        s[n].x += mt.cos(r) * S.vel
        s[n].y += mt.sin(r) * S.vel
        s[n].r = r
    ...

  def draw(S):
    for n in range(len(S.seg_s)-1, -1, -1):
    # for s in S.seg_s:
      s = S.seg_s[n]
      if n==0:
        img=0
      elif n==len(S.seg_s)-1:
        img=32
      else:
         img=16

      blt2(s.x, s.y, pl.images[0], img,0, 16,16, 0, -s.r)#, 2)#s.scale)  鈍い
      ...


######################################################################
#
######################################################################
class NN:
  def __init__(S):
    init(SW, SH, fps=FPS, capture_scale=2, capture_sec=8)
    # mouse(True)

    #-----------
    S.nezu = Nezu(SWH, SHH)
    S.px = S.py = 0
    # S.l = L()
    S.r = 0
    S.z = 1

    pl.load("ox.pyxres")
    S.img = pl.images[0]
    # S.img = pl.Image.from_image("TMP.png")
    # pl.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")

    S.t = T()
    S.l = L(S.img)
    #-----------
    run(S.update, S.draw)
    ...

  def update(S):
    if not btn(MOUSE_BUTTON_LEFT):
      S.nezu.x = pl.mouse_x
      S.nezu.y = pl.mouse_y

    S.l.update(S.nezu)
    S.t.update()
    ...

  def draw(S):
    if not btn(KEY_SPACE):
      cls(0)
    circb(S.nezu.x, S.nezu.y, 2, 9)
    line(S.nezu.x, S.nezu.y, S.l.seg_s[0].x, S.l.seg_s[0].y, 1)

    S.l.draw()
    S.t.draw()
    ...


if __name__ == "__main__":
  NN()
