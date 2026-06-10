import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime

# ================= Configuration =================
YEAR = 2026
MEETING_DATE = datetime.date(2026, 6, 12)
PAST_DAYS = 14

# ================= Color palette =================
COLOR_BG = '#FFFFFF'
COLOR_OUTSIDE = '#F7F9FA'     # Days outside current year (very light gray — nearly transparent)
COLOR_EMPTY = '#EBEDF0'       # Regular days within the year (light gray)
COLOR_RECENT = '#BFDBFE'      # Recent two weeks before the meeting (soft blue)
COLOR_MEETING = '#2563EB'     # Meeting day (vivid blue)
COLOR_TEXT = '#374151'        # Axis labels (dark gray)
COLOR_LEGEND_TEXT = '#6B7280' # Legend text (medium gray)

CELL_SIZE = 12
GAP = 2
ROWS = 7   # Days of the week (Mon–Sun)
COLS = 53  # Weeks in a year (including partial weeks)

# ================= Date computation =================
# Snap to the Sunday on or before Jan 1 so the grid aligns to ISO weeks
first_day = datetime.date(YEAR, 1, 1)
days_to_sunday = (first_day.weekday() + 1) % 7
start_date = first_day - datetime.timedelta(days=days_to_sunday)

# ================= Set up the figure =================
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_facecolor(COLOR_BG)
ax.set_xlim(0, COLS * (CELL_SIZE + GAP) + 150)
ax.set_ylim(0, ROWS * (CELL_SIZE + GAP) + 100)

offset_x, offset_y = 75, 50
ax.set_aspect('equal')

# ================= Draw the contribution grid =================
for col in range(COLS):
    for row in range(ROWS):
        current_date = start_date + datetime.timedelta(days=col * 7 + row)

        x = col * (CELL_SIZE + GAP) + offset_x
        y = (ROWS - 1 - row) * (CELL_SIZE + GAP) + offset_y

        # Cell coloring logic
        if current_date.year == YEAR + 1:
            color = COLOR_OUTSIDE  # Next year
        elif current_date.year == YEAR:
            if current_date == MEETING_DATE:
                color = COLOR_MEETING
            elif MEETING_DATE - datetime.timedelta(days=PAST_DAYS) <= current_date < MEETING_DATE:
                color = COLOR_RECENT
            else:
                color = COLOR_EMPTY
        else:
            color = COLOR_OUTSIDE  # Previous year or earlier

        rect = patches.FancyBboxPatch(
            (x, y), CELL_SIZE, CELL_SIZE,
            boxstyle=f"round,pad=0.2,rounding_size=1.5",
            facecolor=color, edgecolor='none'
        )
        ax.add_patch(rect)

# ================= Month labels (top axis) =================
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i, label in enumerate(month_labels):
    date_obj = datetime.date(YEAR, i+1, 1)
    delta = (date_obj - start_date).days
    col_idx = delta // 7

    if 0 <= col_idx < COLS:
        # Left-align the label with the first cell of that month
        x = col_idx * (CELL_SIZE + GAP) + offset_x + 0.1
        # Place labels just above the grid
        y = ROWS * (CELL_SIZE + GAP) + offset_y + 5
        ax.text(x, y, label, ha='left', va='bottom',
                fontsize=16, fontweight='medium', fontfamily='sans-serif', color=COLOR_TEXT)

# ================= Weekday labels (left axis) =================
day_labels = [('Mon', 1), ('Wed', 3), ('Fri', 5)]
for label, row_idx in day_labels:
    x = offset_x - 48
    y = (ROWS - 1 - row_idx) * (CELL_SIZE + GAP) + offset_y + CELL_SIZE / 2
    ax.text(x, y, label, ha='left', va='center',
            fontsize=16, fontweight='medium', fontfamily='sans-serif', color=COLOR_TEXT)

# ================= Legend (bottom-right, aligned with the grid) =================
legend_y = 20
# Right-align the legend with the grid
grid_right = offset_x + COLS * (CELL_SIZE + GAP)
legend_x = grid_right - 142

ax.text(legend_x, legend_y, 'Muted', ha='left', va='center',
        fontsize=12, color=COLOR_LEGEND_TEXT, fontweight='medium', fontfamily='sans-serif')

# Legend swatches use the same cell size as the grid
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

# ================= Export =================
ax.axis('off')
plt.tight_layout()
plt.savefig('contribution_grid.svg', format='svg', dpi=300, bbox_inches='tight', facecolor=COLOR_BG)
plt.savefig('contribution_grid.png', format='png', dpi=300, bbox_inches='tight', facecolor=COLOR_BG)
print("Done: contribution_grid.svg and contribution_grid.png generated.")