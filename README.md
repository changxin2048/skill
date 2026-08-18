# handdrawn-svg · 手绘风 SVG 生成器

把结构化的框图（架构图 / 流程图 / 思维导图 / 系统图等）变成「像用马克笔在网格纸上手绘」的 SVG 矢量图。本仓库是一个可直接被 AI Agent（Proma / 类 Claude 智能体）加载使用的 **Skill**。

## 特性

- **手绘质感三件套**：笔迹抖动滤镜（`feTurbulence` + `feDisplacementMap`）、手写字体（ZCOOL KuaiLe / Liu Jian Mao Cao，离线回退楷体与 Comic Sans）、米黄网格纸点阵背景。
- **双描边叠线**：用两个不同 seed 的抖动滤镜给大容器描两遍边，形成马克笔「画了两笔」的错位叠线效果。
- **铅笔排线**：每层容器叠加同色系低透明度排线 pattern，增强手账质感。
- **手绘箭头与曲线连接**：不规则三角形箭头 + 轻微 S 形曲线，配合虚线区分返回/辅助路径。
- **马克笔低饱和色板**：预置 7 层配色（用户/编排/LLM/工具/记忆/知识/安全），中文主 + 英文副双语文案排版。
- **可选 PNG 预览**：`scripts/render_preview.py` 一键渲染，cairosvg 缺失时自动创建临时 venv 安装，不污染全局环境。

## 使用方式

本 Skill 面向 AI Agent。当用户表达手绘/涂鸦/马克笔/Sketch 风格制图需求，或要求把已有 SVG 框图重绘成手绘风时，加载 `handdrawn-svg/SKILL.md` 即可获得完整生成流程。

### 工作流概览

1. 解析用户需求，确定图类型、分层结构与文案。
2. 布局（画布建议 1100×960），可参照 `assets/example_agent_architecture.svg` 排版。
3. 按 `references/sketch_recipe.md` 配方生成 SVG（滤镜 / 双描边 / 排线 / 手绘箭头 / 色板均有精确参数）。
4. 用 XML 解析校验文件合法性。
5. （可选）渲染 PNG 预览后交付。

```bash
# XML 校验
python3 -c "import xml.etree.ElementTree as ET; ET.parse('输出.svg'); print('OK')"

# 渲染 PNG 预览（自动处理 cairosvg 缺失）
python3 scripts/render_preview.py 输出.svg
```

## 目录结构

```
handdrawn-svg/
├── SKILL.md                        # Skill 入口：触发条件、工作流、关键规则
├── references/
│   └── sketch_recipe.md            # 完整配方：滤镜参数、色板、手绘箭头、避坑清单
├── assets/
│   └── example_agent_architecture.svg  # 最终版示例（智能体架构图）
└── scripts/
    └── render_preview.py           # PNG 预览渲染脚本
```

## 示例

`assets/example_agent_architecture.svg` 是一张智能体架构图示例（手绘风、无旋转），展示了完整的排版结构、配色与叠线效果，可照此结构修改坐标与文案生成新图。

> 注：cairosvg 渲染的 PNG 预览图会使用回退字体，最终效果以浏览器打开 SVG 为准。

## 许可

本项目未指定许可证，默认保留所有权利。如需复用，请先与作者联系。
