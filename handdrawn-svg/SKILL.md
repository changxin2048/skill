---
name: handdrawn-svg
description: 生成手绘/涂鸦/马克笔风格（hand-drawn, sketchy, marker style）的 SVG 矢量图：架构图、系统图、流程图、结构图、思维导图等，也可把用户已有的普通 SVG 框图重绘成手绘风。当用户提到"手绘风""手账风""涂鸦风""sketch 风""像手画的""马克笔效果""更随性/别太死板""hand-drawn""wobbly"等字眼，或要求把架构图/流程图改造成手绘风格时，务必使用本 Skill。产出带手写字体、抖动线条、双描边叠线、网格纸背景的手绘 SVG（可选渲染 PNG 预览）。注意：用户要的是普通正式风格（整齐、无滤镜）的 SVG 时不要使用本 Skill。
---

# 手绘风 SVG 生成器 (Hand-Drawn SVG)

把结构化的框图（架构图 / 流程图 / 思维导图 / 系统图等）变成"像用马克笔在网格纸上手绘"的 SVG 矢量图。

## 核心思路（先理解 Why）

手绘感 = **笔迹抖动 + 手写字体 + 纸张质感 + 不完美的线条**，四者缺一效果都不对。不要画完美直线、直角、正圆——所有"生硬感"都要靠滤镜和字形消除。结构内容由用户需求决定，风格统一由本 Skill 决定。

## 工作流

1. **解析需求**：确定图的类型、层/模块、连接关系、文案。布局与内容跟着用户需求走。
2. **布局**：画布建议 1100×960（可等比缩放）。自上而下分层：大容器包小块。每个元素都要精确坐标。可参照 `assets/example_agent_architecture.svg` 的排版结构改坐标。
3. **生成 SVG**：按 `references/sketch_recipe.md` 的配方写。文件结构固定为：
   - `<defs>`：两个抖动滤镜 `sketchA`/`sketchB`（**不同 seed**）、纸张点阵 pattern、各层排线 pattern、CSS `@import` 手写字体
   - 纸张背景 rect（米黄底 + 点阵）
   - **形状组** `<g filter="url(#sketchA)">`：所有矩形、连线、箭头、涂鸦装饰
   - **描边组** `<g filter="url(#sketchB)">`：各大容器的第二遍描边（与第一遍错开形成"画了两笔"的叠线）
   - **文字组**（无滤镜）：所有文字
4. **校验 XML**：用 `python3 -c "import xml.etree.ElementTree as ET; ET.parse('文件')"` 确认合法。最常见坑：CSS `@import` 里的 `&` 必须写成 `&amp;`。
5. **渲染预览（可选）**：运行 `scripts/render_preview.py <svg>` 生成 PNG（cairosvg 缺失时自动建 venv 安装，用户环境不允许往全局 site-packages 装包时也能用）。
6. **交付**：给出 `.svg` 路径；有预览则同时给出 `.png` 路径，并说明"预览图字体可能走回退字体，以浏览器打开 SVG 为准"。

## 关键规则

- **文字永远不进抖动滤镜**（会糊掉），形状全部进；滤镜只作用在形状组和描边组上。
- 字体族：`'ZCOOL KuaiLe','Liu Jian Mao Cao','Kaiti SC','STKaiti','KaiTi','Comic Sans MS','Bradley Hand',cursive`。在线时浏览器自动加载快乐体/草书，离线回退楷体/Comic Sans。
- 默认**不做微旋转**（已确认的用户偏好）；只有当用户明确要"更随意、歪歪扭扭"时才给大容器加 -1.5°~1.5° 的 rotate。
- 配色用马克笔低饱和色板（见 recipe 的色板表）：大容器浅色底 + 同色系排线 + 深色双描边；内部小块用近白 `#fffdf7` 底。
- 连接线用轻微 S 形曲线 + 手绘箭头（不规则三角形，不要等腰标准三角形）；返回/辅助路径用虚线 `stroke-dasharray="7,6"`。
- 字号：大标题 26-30，层标题 15-16，块标题 12.5-13，说明 10-11.5；中英对照（中文主 + 英文副）提升专业感。
- 流程编号（①②③…）用手绘圆圈 + 数字，不要默认的实心圆点。
- 可加少量涂鸦装饰（四角小星星、标题波浪下划线）增加手账感，但不要喧宾夺主。

## 参考与资产

- `references/sketch_recipe.md` — 完整配方：滤镜参数、pattern 定义、手绘箭头、XML 片段、色板、避坑清单（生成前必读）
- `assets/example_agent_architecture.svg` — 最终版示例（智能体架构图，手绘风、无旋转），新图可照此结构改坐标与文案
- `scripts/render_preview.py` — PNG 预览渲染脚本，用法见文件头部注释
