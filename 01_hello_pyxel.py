import pyxel as pl
from pyxel import *
import math as mt

W,H=128,128
WH,HH=W//2,H//2
ar=24

def clamp(n, mn, mx):
  return max(min(n, mx), mn)

class NN:
  def __init__(S):
    init(W,H)
    mouse(True)
    run(S.update, S.draw)

  def update(S):
    ...

  def draw(S):
    global ar,dr
    cls(0)
    
    #a
    ax,ay=pl.mouse_x, pl.mouse_y
    ar+=pl.mouse_wheel
    ar = clamp(ar, 8, 32)
    #b
    bx,by=WH,HH
    br=24
    ###########################

    dis = mt.hypot(bx-ax, by-ay)
    dis= dis if ar+br < dis else ar+br
    ang=mt.atan2(by-ay, bx-ax)
    ###########################
    aaa = (mt.pi/2) + mt.asin(abs(ar-br)/dis);
    aa = aaa-ang
    if ar>br:
      aa=mt.pi-aa
    else:
      aa=-aa
    ##########################################
    bb=ang+aaa+mt.pi
    if ar<br:
      bb=bb+mt.pi
    ###########################
    
    lx = mt.cos(aa)*ar +ax
    ly = mt.sin(aa)*ar +ay
    line(ax,ay,lx,ly, 6)
    circ(int(lx),int(ly), 1, 10)

    jx = mt.cos(aa)*br +bx
    jy = mt.sin(aa)*br +by

    line(bx,by,jx,jy,2); circ(int(jx),int(jy),1, 12)
    line(lx,ly, jx,jy, 7)

    zx = mt.cos(ang)*(ar+br)+ax
    zy = mt.sin(ang)*(ar+br)+ay
    line(ax,ay, zx,zy, 3)
    #######################
    line(ax,ay,bx,by, 1)
    circb(ax,ay,abs(ar), 8)
    circb(bx,by,abs(br), 10)
    circb(ax,ay,1, 8)
    circb(bx,by,1, 10)
    #############################
    #############################
    
    llx = mt.cos(bb)*ar +ax
    lly = mt.sin(bb)*ar +ay
    jjx = mt.cos(bb)*br +bx
    jjy = mt.sin(bb)*br +by

    line(ax,ay,llx,lly,9)
    line(bx,by,jjx,jjy,9)
    line(llx,lly,jjx,jjy, 9); circ(int(lx),int(ly), 1, 10)
    ...

NN()
