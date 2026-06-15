# EPC Show 2026 · 展位 3D 平面图 / Interactive Booth Map

[**▶ 在线查看 / Live demo**](https://steven-8.github.io/epc-show-2026-booth-map/)

面向 **EPC Show 2026 — Energy Projects Conference & Expo**（2026‑06‑16/17，休斯敦 George R. Brown Convention Center）的参展商展位 **3D 可视化**。鼠标/手指拖动旋转、缩放，悬停或点击展位查看公司信息与联系方式。已适配手机。

An interactive 3D booth map for the EPC Show 2026 (Houston). Drag to orbit, pinch/scroll to zoom, tap a booth for details. Mobile‑friendly.

## 功能 Features
- **真实参展商**：从官网抓取 **373 家** 参展商 + 展位号（A–T 共 17 个分区）。
- **按比例 3D 展厅**：展厅按 GRB 真实尺寸（Hall A 327×429 ft、35 ft 净高）建模。
- **悬停看简介，点击看详情**：公司简介 / 官网 / 公开商务邮箱（372 家，来源已标注）。
- **★ 重点公司**：标注 15 家燃机 / 发电 / 大型 EPC 同业（侧边引线标注），并附公开商务对接人。
- 搜索、分区跳转、展位号显示、3D/俯视切换。

## 数据来源与免责声明 Data & disclaimer
- **参展商名单与展位号**：来自官网 `epcshow.com` 公开名录（真实）。
- **展位位置与尺寸**：官网不公开真实坐标/尺寸，故按**展位号近似重建**（标准 10×10 ft）。拿到官方平面图(PDF/CAD)可替换 `booths.json` 为精确几何。
- **公司简介 / 网站 / 邮箱**：公开资料检索，按来源可信度标注。
- **参展人员**：仅对"重点公司"做了**公开对接人**检索（LinkedIn/官网/新闻稿），**非官方到场名单、未逐条独立核实**，仅供参考。

> 本项目仅用于商业情报/对接参考，所有信息均来自公开来源。

## 运行 Run
纯静态页面，直接打开 `index.html` 即可（已本地化 Three.js，无需联网/服务器）。
Pure static — just open `index.html` (Three.js is vendored locally).

## 文件 Structure
- `index.html` — 主应用（Three.js 渲染 + 交互）
- `booths.js` — 展位几何 + 公司（渲染只读这个）
- `enrich.js` — 公司简介/网站/邮箱
- `people.js` — 重点公司公开对接人
- `vendor/` — 本地 Three.js (r0.137 UMD)
- `*.py` / `*_wf.js` / `*.json` — 数据抓取与重建脚本（provenance）
