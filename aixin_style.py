#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aixin_style.py — 无锡爱信 / EPLAN 模式电气原理图绘图样式模块

按《电气原理图绘图风格规范-爱信EPLAN模式.md》实现：
A3 横幅图框、坐标网格、标题栏、标准颜色、常用标注辅助函数。

字体: ~/workspace/fonts/NotoSansSC-Regular.otf / -Bold.otf
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle, FancyArrow

_FONT_DIR = os.path.expanduser("~/workspace/fonts")
FP_REG = FontProperties(fname=os.path.join(_FONT_DIR, "NotoSansSC-Regular.otf"))
FP_BOLD = FontProperties(fname=os.path.join(_FONT_DIR, "NotoSansSC-Bold.otf"))

# ---------------- 颜色体系（规范第2节） ----------------
RED     = "#FF0000"   # 导线 / 连接线 / 跨页箭头线
BLUE    = "#0000FF"   # 设备代号 / 设备外框 / 线号 / 端子编号
GREEN   = "#008000"   # 页交叉引用 / 坐标网格 / 接地虚线
MAGENTA = "#FF00FF"   # IO 模块外框 / IO 端子
BLACK   = "#000000"   # 中文描述 / 品牌型号 / 技术参数
ORANGE  = "#E8720C"   # 布局图 DIN 导轨
TEAL    = "#2E8B8B"   # 布局图柜体
PLATE   = "#C0C0C0"   # 布局图安装板

A3_W, A3_H = 16.54, 11.69   # A3 横向, 英寸

# 图面坐标: x 0~10 (列), y 0~7 ; 标题栏 y 0~0.85, 图面区 y 0.85~6.85
TITLE_H = 0.85
FRAME_TOP = 6.85


def new_fig():
    fig = plt.figure(figsize=(A3_W, A3_H))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-0.25, 10.25)
    ax.set_ylim(-0.15, 7.15)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def draw_frame(ax):
    """外框 + 坐标网格(列0-9 / 行A-F, 绿色小字)。"""
    ax.add_patch(Rectangle((0, TITLE_H), 10, FRAME_TOP - TITLE_H,
                           fill=False, ec=BLACK, lw=1.6))
    # 列分隔线 + 列号
    for i in range(11):
        ax.plot([i, i], [TITLE_H, FRAME_TOP], color=BLACK, lw=0.4)
        if i < 10:
            ax.text(i + 0.5, FRAME_TOP + 0.12, str(i), color=GREEN, fontsize=8,
                    ha="center", va="bottom", fontproperties=FP_REG)
    # 行分隔线 + 行字母
    rows = "ABCDEF"
    rh = (FRAME_TOP - TITLE_H) / 6
    for j in range(7):
        y = TITLE_H + j * rh
        ax.plot([0, 10], [y, y], color=BLACK, lw=0.4)
    for j, ch in enumerate(rows):
        y = TITLE_H + (5 - j) * rh + rh / 2
        ax.text(-0.12, y, ch, color=GREEN, fontsize=8, ha="right", va="center",
                fontproperties=FP_REG)
        ax.text(10.12, y, ch, color=GREEN, fontsize=8, ha="left", va="center",
                fontproperties=FP_REG)


def draw_title_block(ax, date="", checker="", reviewer="",
                     project="", client="", page_desc="",
                     func_loc="= RK6T", inst_loc="+ MCP",
                     proj_no="", page_n=1, page_count=36, total=167,
                     prev="", nxt=""):
    """底部标题栏。"""
    y0, h = 0, TITLE_H
    ax.add_patch(Rectangle((0, y0), 10, h, fill=False, ec=BLACK, lw=1.6))
    # 列边界
    xs = [0, 1.3, 2.6, 4.4, 5.6, 7.2, 8.2, 9.0, 10.0]
    for x in xs[1:-1]:
        ax.plot([x, x], [y0, y0 + h], color=BLACK, lw=0.8)

    def cell(x0, x1, title, value, vy=0.28, tsize=8, vsize=9, vcolor=GREEN):
        ax.text(x0 + 0.06, y0 + 0.58, title, fontsize=tsize, color=BLACK,
                va="center", fontproperties=FP_REG)
        ax.text(x0 + 0.06, y0 + vy, value, fontsize=vsize, color=vcolor,
                va="center", fontproperties=FP_REG)

    # Previous / Next
    ax.text(0.06, y0 + 0.62, f"Previous:{prev}", fontsize=8, color=GREEN,
            va="center", fontproperties=FP_REG)
    ax.text(0.06, y0 + 0.25, f"Next:{nxt}", fontsize=8, color=GREEN,
            va="center", fontproperties=FP_REG)
    # 日期/校对/审核 三行
    for k, (t, v) in enumerate([("日期", date), ("校对", checker), ("审核", reviewer)]):
        yy = y0 + 0.62 - k * 0.27
        ax.text(1.36, yy, t, fontsize=7.5, color=BLACK, va="center", fontproperties=FP_REG)
        ax.text(1.75, yy, v, fontsize=8, color=GREEN, va="center", fontproperties=FP_REG)
    ax.plot([1.3, 2.6], [y0 + 0.44, y0 + 0.44], color=BLACK, lw=0.5)
    ax.plot([1.3, 2.6], [y0 + 0.20, y0 + 0.20], color=BLACK, lw=0.5)

    cell(2.6, 4.4, "项目描述", project, vsize=8.5)
    cell(4.4, 5.6, "客户", client)
    cell(5.6, 7.2, "页描述", page_desc)
    ax.text(7.26, y0 + 0.58, func_loc, fontsize=8, color=GREEN, va="center",
            fontproperties=FP_REG)
    ax.text(7.26, y0 + 0.28, inst_loc, fontsize=8, color=GREEN, va="center",
            fontproperties=FP_REG)
    cell(8.2, 9.0, "项目编号", proj_no, vsize=8)
    ax.text(9.06, y0 + 0.58, f"页数  {page_n} / {page_count}", fontsize=8,
            color=GREEN, va="center", fontproperties=FP_REG)
    ax.text(9.06, y0 + 0.28, f"总页数  {total}", fontsize=8, color=GREEN,
            va="center", fontproperties=FP_REG)


# ---------------- 绘图辅助 ----------------

def wire(ax, pts, color=RED, lw=1.4, ls="-"):
    """红色导线折线。pts: [(x,y), ...]"""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls)


def wire_label(ax, x, y, text, color=BLUE, size=9, bold=False):
    """导线旁蓝色线色标注, 如 'BK 2.5mm²'。"""
    ax.text(x, y, text, fontsize=size, color=color, va="center",
            fontproperties=FP_BOLD if bold else FP_REG)


def xref(ax, x, y, line, page, direction="right", size=9):
    """跨页引用: 红色箭头 + 蓝色线号 + 绿色页码。"""
    dx = 0.55 if direction == "right" else -0.55
    ax.annotate("", xy=(x + dx, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.text(x + dx + (0.08 if direction == "right" else -0.08), y,
            line, fontsize=size, color=BLUE, va="center",
            ha="left" if direction == "right" else "right",
            fontproperties=FP_BOLD)
    ax.text(x - (0.08 if direction == "right" else -0.08), y,
            page, fontsize=size - 1, color=GREEN, va="center",
            ha="right" if direction == "right" else "left",
            fontproperties=FP_REG)


def device_tag(ax, x, y, code, spec="", brand="", func="", size=10, dy=0.28):
    """设备代号堆叠标注: 蓝色加粗代号 + 规格 + 品牌 + 中文功能。"""
    ax.text(x, y, code, fontsize=size + 1, color=BLUE, va="center",
            fontproperties=FP_BOLD)
    yy = y - dy
    for t in (spec, brand, func):
        if t:
            ax.text(x, yy, t, fontsize=size - 1.5, color=BLACK, va="center",
                    fontproperties=FP_REG)
            yy -= dy


def func_box(ax, x, y, w, h, rows):
    """现场设备功能盒(蓝色框): rows 为文本行列表, 第一行蓝色。"""
    ax.add_patch(Rectangle((x, y - h), w, h, fill=False, ec=BLUE, lw=1.2))
    n = len(rows)
    for i, t in enumerate(rows):
        c = BLUE if i == 0 else BLACK
        fp = FP_BOLD if i == 0 else FP_REG
        ax.text(x + w / 2, y - h * (i + 0.7) / n, t, fontsize=8.5, color=c,
                ha="center", va="center", fontproperties=fp)


def relay_coil(ax, x, y, code="-DJ1", spec="DC24V 1CO", brand="RSL1PVBU"):
    """继电器线圈符号(A1/A2)。"""
    ax.add_patch(Rectangle((x - 0.18, y - 0.12), 0.36, 0.24,
                           fill=False, ec=BLUE, lw=1.2))
    ax.text(x + 0.24, y + 0.02, "A1", fontsize=7, color=BLACK,
            ha="left", va="center", fontproperties=FP_REG)
    ax.text(x + 0.24, y - 0.22, "A2", fontsize=7, color=BLACK,
            ha="left", va="center", fontproperties=FP_REG)
    device_tag(ax, x - 0.55, y + 0.28, code, spec, brand, size=9)


def relay_contact(ax, x, y, n1="11", n2="14", xref_page=""):
    """继电器常开触点(11/14)+绿色交叉引用。"""
    ax.plot([x, x + 0.35], [y, y], color=RED, lw=1.4)
    ax.plot([x + 0.35, x + 0.5], [y, y + 0.12], color=RED, lw=1.4)
    ax.text(x - 0.06, y + 0.06, n1, fontsize=7, color=BLACK, ha="right",
            fontproperties=FP_REG)
    ax.text(x - 0.06, y - 0.12, n2, fontsize=7, color=BLACK, ha="right",
            fontproperties=FP_REG)
    if xref_page:
        ax.text(x + 0.55, y - 0.10, xref_page, fontsize=7.5, color=GREEN,
                fontproperties=FP_REG)


def motor_symbol(ax, x, y, code="-M1", spec="380V 0.55KW 1.5A 3~", func="转阀",
               tag_xy=None):
    """电机符号: 圆圈 M 3~。"""
    ax.add_patch(plt.Circle((x, y), 0.28, fill=False, ec=BLUE, lw=1.4))
    ax.text(x, y + 0.05, "M", fontsize=14, color=BLACK, ha="center",
            va="center", fontproperties=FP_BOLD)
    ax.text(x, y - 0.13, "3~", fontsize=8, color=BLACK, ha="center",
            va="center", fontproperties=FP_REG)
    tx, ty = tag_xy if tag_xy else (x - 0.62, y + 0.55)
    device_tag(ax, tx, ty, code, spec, "", func, size=9)
    # PE
    ax.plot([x, x], [y - 0.28, y - 0.45], color=RED, lw=1.4)
    ax.text(x + 0.08, y - 0.45, "PE", fontsize=8, color=BLACK,
            fontproperties=FP_REG)


def breaker(ax, x, y, code="-Q1", spec="2P/D4", brand="Schneider",
            order="A9F19204", poles=2, tag_xy=None):
    """小型断路器符号。tag_xy 为代号标注位置, 缺省在符号左上。"""
    for p in range(poles):
        px = x + p * 0.30
        ax.plot([px, px], [y - 0.15, y + 0.15], color=RED, lw=1.4)
        ax.plot([px - 0.08, px + 0.08], [y + 0.02, y + 0.14], color=RED, lw=1.4)
        ax.text(px, y + 0.24, str(2 * p + 1), fontsize=7, color=BLACK,
                ha="center", fontproperties=FP_REG)
        ax.text(px, y - 0.24, str(2 * p + 2), fontsize=7, color=BLACK,
                ha="center", fontproperties=FP_REG)
    tx, ty = tag_xy if tag_xy else (x - 0.28, y + 0.55)
    device_tag(ax, tx, ty, code, spec, f"{brand}", order, size=9)


def io_module_frame(ax, x, y, w, h, code, order, kind, brand="SIEMENS"):
    """IO 模块品红虚线框 + 顶部标注。"""
    ax.add_patch(Rectangle((x, y - h), w, h, fill=False, ec=MAGENTA,
                           lw=1.2, ls=(0, (6, 4))))
    ax.text(x + 0.1, y + 0.28, code, fontsize=11, color=BLUE,
            fontproperties=FP_BOLD)
    ax.text(x + 0.1, y + 0.62, order, fontsize=8, color=BLUE,
            fontproperties=FP_REG)
    ax.text(x + w / 2, y + 0.10, kind, fontsize=10, color=BLUE, ha="center",
            fontproperties=FP_REG)
    ax.text(x + w - 0.1, y + 0.10, brand, fontsize=10, color=BLUE, ha="right",
            fontproperties=FP_REG)
