import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime

# ================= 参数设置 =================
YEAR = 2026
MEETING_DATE = datetime.date(2026, 6, 12)
PAST_DAYS = 14

# ================= 颜色配置 =================
COLOR_BG = '#FFFFFF'
COLOR_OUTSIDE = '#F7F9FA'     # 2027年及之外 (极浅灰，近似透明以区分)
COLOR_EMPTY = '#EBEDF0'       # 2026年普通日
COLOR_RECENT = '#BFDBFE'      # 过去两周 (淡蓝)
COLOR_MEETING = '#2563EB'     # 组会当日 (深蓝)
COLOR_TEXT = '#374151'        # 标签文字 (深灰)
COLOR_LEGEND_TEXT = '#6B7280' # 图例文字 (中灰)

CELL_SIZE = 12
GAP = 2
ROWS = 7
COLS = 53

# ================= 日期计算 =================
# 确保网格从2026年前最后一个周日开始
first_day = datetime.date(YEAR, 1, 1)
days_to_sunday = (first_day.weekday() + 1) % 7
start_date = first_day - datetime.timedelta(days=days_to_sunday)

# ================= 创建画布 =================
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_facecolor(COLOR_BG)
ax.set_xlim(0, COLS * (CELL_SIZE + GAP) + 150)
ax.set_ylim(0, ROWS * (CELL_SIZE + GAP) + 100)

offset_x, offset_y = 50, 50
ax.set_aspect('equal')

# ================= 绘制网格 =================
for col in range(COLS):
    for row in range(ROWS):
        current_date = start_date + datetime.timedelta(days=col * 7 + row)

        x = col * (CELL_SIZE + GAP) + offset_x
        y = (ROWS - 1 - row) * (CELL_SIZE + GAP) + offset_y

        # 关键判断逻辑
        if current_date.year == YEAR + 1:
            color = COLOR_OUTSIDE  # 2027年的日子
        elif current_date.year == YEAR:
            if current_date == MEETING_DATE:
                color = COLOR_MEETING
            elif MEETING_DATE - datetime.timedelta(days=PAST_DAYS) <= current_date < MEETING_DATE:
                color = COLOR_RECENT
            else:
                color = COLOR_EMPTY
        else:
            color = COLOR_OUTSIDE  # 2025年及之前

        rect = patches.FancyBboxPatch(
            (x, y), CELL_SIZE, CELL_SIZE,
            boxstyle=f"round,pad=0.2,rounding_size=1.5",
            facecolor=color, edgecolor='none'
        )
        ax.add_patch(rect)

# ================= 月份标签 =================
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i, label in enumerate(month_labels):
    date_obj = datetime.date(YEAR, i+1, 1)
    delta = (date_obj - start_date).days
    col_idx = delta // 7

    if 0 <= col_idx < COLS:
        # 左对齐：确保月份文字与格子的左边缘对齐，解决偏左问题
        x = col_idx * (CELL_SIZE + GAP) + offset_x + 0.1
        # 更近：距离网格顶部仅 5 个单位
        y = ROWS * (CELL_SIZE + GAP) + offset_y + 5
        ax.text(x, y, label, ha='left', va='bottom',
                fontsize=16, fontweight='medium', fontfamily='sans-serif', color=COLOR_TEXT)

# ================= 星期标签  =================
day_labels = [('Mon', 1), ('Wed', 3), ('Fri', 5)]
for label, row_idx in day_labels:
    x = offset_x - 48
    y = (ROWS - 1 - row_idx) * (CELL_SIZE + GAP) + offset_y + CELL_SIZE / 2
    ax.text(x, y, label, ha='left', va='center',
            fontsize=16, fontweight='medium', fontfamily='sans-serif', color=COLOR_TEXT)

# ================= 底部图例  =================
legend_y = 20
# 图例右对齐主网格
grid_right = offset_x + COLS * (CELL_SIZE + GAP)
legend_x = grid_right - 142

ax.text(legend_x, legend_y, 'Muted', ha='left', va='center',
        fontsize=12, color=COLOR_LEGEND_TEXT, fontweight='medium', fontfamily='sans-serif')

# 图例方格的大小与贡献图方格保持一致 (CELL_SIZE)
for i, color in enumerate([COLOR_EMPTY, COLOR_RECENT, COLOR_MEETING]):
    rect = patches.FancyBboxPatch(
        (legend_x + 42 + i * (CELL_SIZE + GAP + 5), legend_y - 6),
        CELL_SIZE, CELL_SIZE,
        boxstyle=f"round,pad=0.2,rounding_size=1.5",
        facecolor=color, edgecolor='none'
    )
    ax.add_patch(rect)

ax.text(legend_x + 42 + 3 * (CELL_SIZE + GAP + 5), legend_y, 'Bright', ha='left', va='center',
        fontsize=12, color=COLOR_LEGEND_TEXT, fontweight='medium', fontfamily='sans-serif')

# ================= 输出 SVG =================
ax.axis('off')
plt.tight_layout()
plt.savefig('contribution_grid.svg', format='svg', dpi=300, bbox_inches='tight')
print("Done: contribution_grid.svg generated.")