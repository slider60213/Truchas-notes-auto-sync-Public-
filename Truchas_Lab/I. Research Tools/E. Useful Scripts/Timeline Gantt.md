---
type: 📝 Research
created: 2026-08-12 22:28
modified: 2026-08-12 22:41
tags:
  - "#Truchas"
---
## 📂 本文關聯檔案索引
```dataview
LIST
WHERE contains(this.file.outlinks, file.link)
AND !icontains(file.name, ".png")
AND !icontains(file.name, ".jpg") 
AND !icontains(file.name, ".pdf")
AND !icontains(file.name, "excalidraw")
```

---
# 📌 摘要

1. Create a `timeline_data.yaml` based on the template below.
2. Execute `generate_timeline.py` to generate the `timeline_gantt.png`.

---
# 🦖 以前


---
# 👨‍💻 以後


---
# 📝 內容紀錄


- timeline_data.yaml
```
- start: "2026-02-25"
  end: "2026-02-25"
  title: "Solo Work Begins"
  subtitle: ""

- start: "2026-02-26"
  end: "2026-03-13"
  title: "Tool Learning"
  subtitle: "Obsidian, Gemini, NotebookLM"

- start: "2026-03-15"
  end: "2026-04-07"
  title: "Truchas-WSL"
  subtitle: "v2.0.2 (116-parallel)"

- start: "2026-04-12"
  end: "2026-05-14"
  title: "Tool Learning"
  subtitle: "GitHub, Obsidian"

- start: "2026-05-06"
  end: "2026-05-13"
  title: "Tool Learning"
  subtitle: "VS Code"

- start: "2026-05-06"
  end: "2026-06-16"
  title: "Truchas-WSL"
  subtitle: "VFIFE Reconstruction"

- start: "2026-06-19"
  end: "2026-06-29"
  title: "Truchas-WSL"
  subtitle: "Python GUI"

- start: "2026-06-30"
  end: "2026-07-23"
  title: "Truchas-WSL"
  subtitle: "DBM+ Workflow Automation"

- start: "2026-07-02"
  end: "2026-07-25"
  title: "Truchas-WSL"
  subtitle: "AI Agent (LangGraph)"

- start: "2026-07-27"
  end: "2026-08-12"
  title: "Truchas-WSL"
  subtitle: "V5Slider"
```

-  generate_timeline.py
```python 
import datetime
import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import yaml

# 配色設定 (嚴格維持指定風格)
COLOR_MAIN_AXIS = "#0B4F6C"  # 深藍色 (主標題 / 網格線)
COLOR_BAR_FILL = "#81A1C1"  # 淡藍色 (任務時間橫條)
COLOR_BAR_BORDER = "#0B4F6C"  # 深藍色 (橫條邊框)
COLOR_MONTH_NODE = "#FFC000"  # 金黃色 (月份圓圈節點)
COLOR_SUBTITLE = "#1E73BE"  # 藍色 (細項副標題)
COLOR_DATE_TEXT = "#8C92AC"  # 淺灰色 (獨立日期標示)
COLOR_TEXT_MAIN = "#000000"  # 黑色 (主標題與天數)


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def generate_gantt_timeline(
    data_path="timeline_data.yaml", output_path="timeline_gantt.png"
):
    # 1. 載入 YAML 資料
    with open(data_path, "r", encoding="utf-8") as f:
        tasks = yaml.safe_load(f)

    parsed_tasks = []
    for item in tasks:
        s_date = parse_date(item["start"])
        e_date = parse_date(item["end"])
        days = (e_date - s_date).days + 1
        parsed_tasks.append(
            {
                "start": s_date,
                "end": e_date,
                "days": days,
                "title": item["title"],
                "subtitle": item.get("subtitle", ""),
            }
        )

    # 按起始日期由早到晚排序
    parsed_tasks.sort(key=lambda x: x["start"])

    # 2. 計算時間範圍與月份節點
    min_date = min(t["start"] for t in parsed_tasks)
    max_date = max(t["end"] for t in parsed_tasks)

    start_month = datetime.date(min_date.year, min_date.month, 1)
    if max_date.month == 12:
        end_month = datetime.date(max_date.year + 1, 1, 1)
    else:
        end_month = datetime.date(max_date.year, max_date.month + 1, 1)

    print("=== [驗證 1] 時程與天數統計 ===")
    for t in parsed_tasks:
        print(
            f"任務: {t['title']:<15} | 細項: {t['subtitle']:<25} | 耗時: {t['days']:>2} 天 ({t['start']} ~ {t['end']})"
        )
    print(f"\n時間軸繪製範圍: {start_month} 至 {end_month}\n")

    # 3. 初始化圖表 (橫向寬螢幕比例 16:9 適合報告展示)
    num_tasks = len(parsed_tasks)
    fig, ax = plt.subplots(figsize=(14, max(6, num_tasks * 0.75)), dpi=300)

    num_start = mdates.date2num(start_month)
    num_end = mdates.date2num(end_month)

    # 配合延伸的左側箭頭與三行式文字排版，調整 X 與 Y 軸邊界
    ax.set_xlim(num_start - 25, num_end + 18)
    ax.set_ylim(-1.5, num_tasks + 0.8)
    ax.invert_yaxis()

    # 4. 繪製背景月份垂直網格線與頂部月份黃圈標籤
    curr = start_month
    month_dates = []
    while curr <= end_month:
        month_dates.append(curr)
        if curr.month == 12:
            curr = datetime.date(curr.year + 1, 1, 1)
        else:
            curr = datetime.date(curr.year, curr.month + 1, 1)

    for m_date in month_dates:
        m_num = mdates.date2num(m_date)
        m_str = m_date.strftime("%b.")

        # 垂直虛網格線
        ax.axvline(
            x=m_num, color="#E5E9F0", linestyle="--", linewidth=1, zorder=1
        )

        # 頂部黃色月份標籤
        ax.scatter(
            m_num,
            -0.6,
            s=3000,
            color=COLOR_MONTH_NODE,
            edgecolors="#000000",
            linewidth=1.5,
            zorder=4,
        )
        ax.text(
            m_num,
            -0.6,
            m_str,
            ha="center",
            va="center",
            fontsize=16.0,
            fontweight="bold",
            color="#000000",
            zorder=5,
        )

    # 頂部貫穿時間主軸線 (大幅延伸左側起點，加粗實心箭頭)
    arrow_x_start = num_start - 22
    arrow_x_end = num_end + 12
    arrow_dx = arrow_x_end - arrow_x_start

    main_arrow = patches.FancyArrow(
        x=arrow_x_start,
        y=-0.7,
        dx=arrow_dx,
        dy=0,
        width=0.08,
        head_width=0.25,
        head_length=3.5,
        shape="full",
        overhang=0.1,
        facecolor=COLOR_MAIN_AXIS,
        edgecolor="#000000",
        linewidth=1.2,
        zorder=3,
    )
    ax.add_patch(main_arrow)

    print("=== [驗證 2] 甘特圖列渲染驗證 ===")

    # 5. 繪製任務甘特圖橫條與說明 (改為三行式文字結構)
    for y_idx, task in enumerate(parsed_tasks):
        y_pos = y_idx + 0.8  # 整體任務下移，拉開與主時間軸距離

        s_num = mdates.date2num(task["start"])
        e_num = mdates.date2num(task["end"]) + 0.9

        bar_width = max(e_num - s_num, 0.8)

        # A. 繪製淡藍色時間區間橫條
        bar_rect = patches.FancyBboxPatch(
            (s_num, y_pos - 0.22),
            bar_width,
            0.44,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor=COLOR_BAR_FILL,
            edgecolor=COLOR_BAR_BORDER,
            lw=1,
            zorder=3,
        )
        ax.add_patch(bar_rect)

        # B. 橫條右側：標註耗費天數
        day_text = (
            f"{task['days']} day" if task["days"] == 1 else f"{task['days']} days"
        )
        ax.text(
            s_num + bar_width + 1.5,
            y_pos,
            day_text,
            ha="left",
            va="center",
            fontsize=14.0,
            fontweight="bold",
            color="#4C566A",
            zorder=4,
        )

        # C. 橫條左側：計算最寬文字長度以精確置中，動態切換兩行/三行排版
        sub_str = task["subtitle"] if task["subtitle"] else ""
        date_range_str = (
            f"({task['start'].strftime('%m/%d')})"
            if task["days"] == 1
            else f"({task['start'].strftime('%m/%d')} ~ {task['end'].strftime('%m/%d')})"
        )

        # 1. 測量各行文字像素寬度，找出最寬的一行
        from matplotlib.textpath import TextPath
        from matplotlib.font_manager import FontProperties

        fp_bold = FontProperties(size=10, weight="bold")
        fp_sub = FontProperties(size=8.5)
        fp_date = FontProperties(size=8.0)

        w_title = TextPath((0, 0), task["title"], prop=fp_bold).get_extents().width
        w_sub = TextPath((0, 0), sub_str, prop=fp_sub).get_extents().width if sub_str else 0
        w_date = TextPath((0, 0), date_range_str, prop=fp_date).get_extents().width

        max_text_width = max(w_title, w_sub, w_date)

        # 2. 推算中心 X 座標 (使用調優後的參數)
        x_center = (s_num - 4.0) - (max_text_width / 2.0) * 0.22

        # 3. 依據是否有細項 (sub_str)，動態分派 Y 軸位置與行數
        if sub_str:
            # === 三行式排版 ===
            # 第一行：主標題
            ax.text(
                x_center, y_pos - 0.22, task["title"],
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=COLOR_TEXT_MAIN, zorder=4
            )
            # 第二行：工作細項
            ax.text(
                x_center, y_pos, sub_str,
                ha="center", va="center", fontsize=8.5,
                color=COLOR_SUBTITLE, zorder=4
            )
            # 第三行：工作日期
            ax.text(
                x_center, y_pos + 0.20, date_range_str,
                ha="center", va="center", fontsize=8.0,
                color=COLOR_DATE_TEXT, zorder=4
            )
        else:
            # === 兩行式排版 (自動緊縮，消除中間空隙) ===
            # 第一行：主標題
            ax.text(
                x_center, y_pos - 0.12, task["title"],
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=COLOR_TEXT_MAIN, zorder=4
            )
            # 第二行：工作日期
            ax.text(
                x_center, y_pos + 0.12, date_range_str,
                ha="center", va="center", fontsize=8.0,
                color=COLOR_DATE_TEXT, zorder=4
            )

        print(
            f"Row {y_idx:>2}: X範圍 [{s_num:.1f} - {s_num+bar_width:.1f}] | 標題: {task['title']} | 耗時: {day_text}"
        )

    # 隱藏預設圖表外框與 Y 軸刻度
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0.3, dpi=300)
    print(f"\n[完成] 橫向甘特時間軸已成功輸出至: {output_path}")


if __name__ == "__main__":
    generate_gantt_timeline()
```


![](pics/timeline_gantt%201.png)

---
# 🔗 參考資料


---