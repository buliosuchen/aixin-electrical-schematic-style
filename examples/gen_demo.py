#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_demo.py — 生成《电气原理图绘图风格规范》示例页 (PNG + PDF)。

电机直接启动回路, 按规范绘制, 符号符合 IEC 60617。
依赖: aixin_style.py (同目录或 PYTHONPATH), matplotlib, NotoSansSC 字体。
输出: demo_原理图风格示例页.png / .pdf (与本脚本同目录)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import aixin_style as S
from aixin_style import FP_REG, FP_BOLD, RED, BLUE, GREEN, BLACK


def xref_out(ax, x, y, line, page, size=9):
    """出页交叉引用: 绿色页码 + 红色箭头 + 蓝色线号(朝右)。"""
    ax.text(x, y, page, fontsize=size - 1, color=GREEN, ha="right",
            va="center", fontproperties=FP_REG)
    ax.annotate("", xy=(x + 0.55, y), xytext=(x + 0.08, y),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.text(x + 0.63, y, line, fontsize=size, color=BLUE, ha="left",
            va="center", fontproperties=FP_BOLD)


def main():
    fig, ax = S.new_fig()
    S.draw_frame(ax)
    S.draw_title_block(
        ax, date="2026/10/02", checker="Muse",
        project="风格示例项目", client="示例客户",
        page_desc="电机直接启动(风格示例)",
        func_loc="= DEMO", inst_loc="+ MCP",
        proj_no="STYLE-001", page_n=1, page_count=1, total=1)

    # ---------- 顶部母线 ----------
    S.wire(ax, [(4.88, 6.55), (7.70, 6.55)])          # DC24+
    S.xref(ax, 4.25, 6.55, "DC24+", "7.3:C", "right")
    xref_out(ax, 7.70, 6.55, "DC24+", "12.0:A")
    for yy, lbl, pg_l, pg_r in [(6.08, "L1", "5.8:A", "11.0:A"),
                                (5.78, "L2", "5.9:A", "11.0:A"),
                                (5.38, "L3", "5.10:A", "11.0:B")]:
        S.wire(ax, [(1.78, yy), (7.70, yy)])
        S.xref(ax, 1.15, yy, lbl, pg_l, "right")
        xref_out(ax, 7.70, yy, lbl, pg_r)
    S.wire(ax, [(4.55, 2.70), (7.70, 2.70)])          # DC24-
    xref_out(ax, 7.70, 2.70, "DC24-", "12.0:A")

    # ---------- 主回路: L1/L2/L3 -> QF1 -> KM1 -> XMT1 -> M1 ----------
    phases = [1.70, 2.15, 2.60]
    bus_y = [6.08, 5.78, 5.38]
    qf_cy, km_cy = 4.95, 4.25
    qf_yt, qf_yb = qf_cy + 0.124, qf_cy - 0.124   # iec_breaker_v size=0.20
    km_yt, km_yb = km_cy + 0.112, km_cy - 0.112   # iec_no_contact_v size=0.18
    term_y = 3.35

    for x, by, tt, tb in zip(phases, bus_y, ["1", "3", "5"], ["2", "4", "6"]):
        S.wire(ax, [(x, by), (x, qf_yt + 0.06)])
        S.iec_breaker_v(ax, x, qf_cy, tt, tb)
        S.wire(ax, [(x, qf_yb - 0.06), (x, km_yt + 0.06)])
        S.iec_no_contact_v(ax, x, km_cy, tt, tb)
        S.wire(ax, [(x, km_yb - 0.06), (x, term_y + 0.15)])
        ax.add_patch(Circle((x, term_y), 0.11, fill=True, fc="white",
                            ec=BLUE, lw=1.4))
        ax.text(x, term_y, tt, fontsize=8, color=BLUE, ha="center",
                va="center", fontproperties=FP_BOLD)
        if abs(x - 2.15) < 0.01:
            S.wire(ax, [(x, term_y - 0.15), (x, 2.30)])   # 中相到电机
        else:
            S.wire(ax, [(x, term_y - 0.15), (x, 2.55)])   # 两侧短桩头

    S.device_tag(ax, 2.95, 5.55, "-QF1", "3P/D10", "Schneider", "A9F19310",
                 size=9)
    S.device_tag(ax, 2.95, 4.42, "-KM1", size=9)
    ax.text(2.95, 4.14, "/12.1:E", fontsize=7.5, color=GREEN,
            fontproperties=FP_REG)
    ax.text(1.15, 3.52, "-XMT1", fontsize=10, color=BLUE,
            fontproperties=FP_BOLD)
    S.device_tag(ax, 3.10, 3.55, "-W1", "YJV 4*1.5", "BK BN GY GNYE",
                 "转阀电机", size=9)
    S.wire_label(ax, 1.12, 4.02, "BK 2.5mm²", size=9)
    S.motor_symbol(ax, 2.15, 2.02, "-M1", "380V 0.55KW 1.5A 3~", "转阀",
                   tag_xy=(3.10, 2.30))

    # -EB1 接地母排(绿虚线): 走触点空隙, 不穿符号
    S.wire(ax, [(1.20, 4.55), (4.35, 4.55)], color=GREEN, ls=(0, (6, 4)))
    S.wire(ax, [(1.55, 4.55), (1.55, 1.62)], color=GREEN, ls=(0, (6, 4)))
    S.wire(ax, [(1.55, 1.62), (2.15, 1.62)], color=GREEN, ls=(0, (6, 4)))
    ax.text(1.15, 5.04, "-EB1", fontsize=10, color=BLUE,
            fontproperties=FP_BOLD)
    ax.text(2.10, 5.04, "接地母排", fontsize=9, color=BLACK,
            fontproperties=FP_REG)

    # ---------- 控制回路 ----------
    # KM1 线圈支路 (x=4.9)
    S.wire(ax, [(4.90, 6.55), (4.90, 5.14)])
    S.relay_coil(ax, 4.90, 5.02, "-KM1", "LC1D09BD", "Schneider",
                 tag_xy=(4.05, 5.42))
    S.wire(ax, [(4.90, 4.90), (4.90, 4.79)])
    S.iec_no_contact_v(ax, 4.90, 4.62, "11", "14", size=0.18)
    ax.text(5.14, 4.55, "/12.2:E", fontsize=7.5, color=GREEN,
            fontproperties=FP_REG)
    S.wire(ax, [(4.90, 4.45), (4.90, 2.70)])
    S.wire_label(ax, 5.85, 5.12, "BU 1mm²", size=9)

    # DJ1 线圈支路 (x=7.35), 穿过 ET_DQ1 品红虚线框
    S.wire(ax, [(7.35, 6.55), (7.35, 4.45)])
    S.io_module_frame(ax, 6.35, 4.45, 2.00, 0.90,
                      "-ET_DQ1", "6ES7132-6BH00-0AA0", "DQ 16x24VDC BA")
    for yy, t, c, fp in [(4.20, "Q30.1", BLUE, FP_REG),
                         (4.05, "电机1启动", BLACK, FP_REG),
                         (3.90, "-DJ1", BLUE, FP_BOLD),
                         (3.75, "DQ1", BLACK, FP_REG)]:
        ax.text(7.35, yy, t, fontsize=8.5, color=c, ha="center",
                va="center", fontproperties=fp)
    S.wire(ax, [(7.35, 3.55), (7.35, 3.47)])
    S.relay_coil(ax, 7.35, 3.35, "-DJ1", "DC24V 1CO", "RSL1PVBU",
                 tag_xy=(6.65, 3.45))
    S.wire(ax, [(7.35, 3.23), (7.35, 2.70)])

    # 页脚注
    ax.text(0.35, 1.12,
            "注:本页为风格示例,按《电气原理图绘图风格规范-爱信EPLAN模式》绘制,符号符合 IEC 60617。",
            fontsize=9, color=BLACK, va="center", fontproperties=FP_REG)

    outdir = os.path.dirname(os.path.abspath(__file__))
    fig.savefig(os.path.join(outdir, "demo_原理图风格示例页.png"), dpi=150)
    fig.savefig(os.path.join(outdir, "demo_原理图风格示例页.pdf"))
    plt.close(fig)
    print("done:", outdir)


if __name__ == "__main__":
    main()
