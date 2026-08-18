# 手绘 SVG 完整配方（Sketch Recipe）

生成前必读。所有坐标、参数、色板都来自经过验证的最终版示例（`assets/example_agent_architecture.svg`）。

## 1. 文件骨架

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="960" viewBox="0 0 1100 960">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&amp;family=Liu+Jian+Mao+Cao&amp;display=swap');
    .text { font-family: 'ZCOOL KuaiLe','Liu Jian Mao Cao','Kaiti SC','STKaiti','KaiTi','Comic Sans MS','Bradley Hand',cursive; }
    .shapes { stroke-linecap: round; stroke-linejoin: round; }
  </style>
  <defs>…滤镜与 pattern…</defs>
  <!-- 纸张背景 -->
  <!-- 形状组：<g filter="url(#sketchA)" class="shapes"> -->
  <!-- 描边组：<g filter="url(#sketchB)" class="shapes"> -->
  <!-- 文字组：<g class="text"> -->
</svg>
```

## 2. 抖动滤镜（两个，seed 必须不同）

```xml
<filter id="sketchA" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="5.5" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="sketchB" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="13" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

- `scale` 控制抖动强度：4 轻微，8 很抖，默认 5.5~6。
- 滤镜区域必须放大到 116%，否则图形边缘会被裁切。
- 两个滤镜只是 seed 不同 → 同一图形两遍描边会错位，这是"叠线"效果的关键。

## 3. 双描边叠线（马克笔画两笔的效果）

每个**大容器**画三层：
1. 填充 rect（sketchA 组）
2. 第一遍描边 rect，`stroke-width="3"`（sketchA 组）
3. 第二遍描边 rect，`stroke-width="1.6"`（sketchB 组，seed 不同 → 与第一遍错开）

**内部小块**只画一遍描边（stroke-width 2）即可，避免画面杂乱。容器圆角 rx 12~15，小块 rx 8~10。

## 4. 纸张背景（米黄 + 点阵）

```xml
<pattern id="paperDots" width="22" height="22" patternUnits="userSpaceOnUse">
  <circle cx="3" cy="3" r="1.3" fill="#cbbfa9" opacity="0.5"/>
</pattern>
<rect width="1100" height="960" fill="#fbf7ee"/>
<rect width="1100" height="960" fill="url(#paperDots)"/>
```

## 5. 铅笔排线（叠加在大容器填充之上）

```xml
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="8" stroke="#047857" stroke-width="1" opacity="0.15"/>
</pattern>
```

每层一个 pattern，`stroke` 用该层深色，opacity 0.12~0.16。用法：`<rect … fill="url(#hatch)"/>` 叠在填充 rect 之后。

## 6. 手绘箭头（不用 marker，直接画不规则三角形）

```xml
<!-- 向下箭头 -->
<path d="M543,232 L557,234 L550,244 Z" fill="#f59e0b"/>
<!-- 向上箭头 -->
<path d="M193,551 L207,553 L200,542 Z"/>
```

要点：底边两端点高度差 1~2px、顶点偏离中线 1px，形成"随手一画"的不规则感。不要画等腰标准三角形。

## 7. 连接线

- 主连接用轻微 S 形三次曲线：`M550,198 C547,208 553,222 550,233`（中点偏移 3~4px）
- 返回 / 辅助路径用虚线：`stroke-dasharray="7,6"`，颜色 `#94a3b8`
- 分支线：先垂直一小段 → 水平段 → 垂直进目标，拐角处加微弯曲

## 8. 色板（马克笔低饱和）

| 层 | 描边（深） | 容器填充（浅） | 排线色 | 小块描边 |
|---|---|---|---|---|
| 用户层（天空蓝） | `#38bdf8` | `#dff3ff` | `#0369a1` | `#7dd3fc` |
| 编排层（靛蓝） | `#818cf8` | `#eef1ff` | `#4338ca` | `#a5b4fc` |
| LLM（紫，实心） | `#6d28d9` | `#8b5cf6` | — | 内描边 `#4c1d95` |
| 工具层（绿） | `#10b981` | `#e9fbf1` | `#047857` | `#a7f3d0` |
| 记忆层（琥珀） | `#f59e0b` | `#fef6e4` | `#b45309` | `#fde68a` |
| 知识层（青） | `#06b6d4` | `#e7fbfe` | `#0e7490` | `#a5f3fc` |
| 安全层（石板灰，虚线框） | `#94a3b8` | `#f4f1ea` | `#475569` | — |

- 小块填充统一 `#fffdf7`；块标题 `#334155`；说明文字 `#64748b`；层标题用该层深色
- 流程编号手绘圆圈描边 `#f59e0b`，数字 `#b45309`；辅助编号用 `#94a3b8`/`#64748b`
- 箭头/主连接线 `#f59e0b`，虚线返回 `#94a3b8`

## 9. 字号与排版

- 大标题 26~30 / 层标题 15~16 / 块标题 12.5~13 / 说明 10~11.5
- 中英对照：中文主 + `<tspan>` 英文副（英文降一档字号、透明度 0.75）
- 容器标签放左上角 (x+18, y+26) 左右；块内文字居中

## 10. 涂鸦装饰（适量，别喧宾夺主）

```xml
<!-- 四角星（可 translate + scale） -->
<path d="M0,-12 C1,-3 3,-1 12,0 C3,1 1,3 0,12 C-1,3 -3,1 -12,0 C-3,-1 -1,-3 0,-12 Z"
      transform="translate(150,115) scale(1.1)" fill="#f472b6" opacity="0.85"/>
<!-- 标题波浪下划线 -->
<path d="M330,60 C370,53 410,67 450,60 C490,53 530,67 570,60 C610,53 650,67 690,60 C730,53 770,67 810,60"
      fill="none" stroke="#f59e0b" stroke-width="2.5"/>
```

## 11. 避坑清单（每条都是踩过的坑）

1. **CSS `@import` 里的 `&` 必须写成 `&amp;`**，否则 XML 解析报 `not well-formed (invalid token)`。
2. **文字绝不能进滤镜组**——会糊成一团。形状组和文字组必须分离。
3. 滤镜区域必须扩大（`x="-8%" y="-8%" width="116%" height="116%"`），否则边缘被裁。
4. 双描边必须用**不同 seed** 的两个滤镜，否则两遍描边完全重合等于没画。
5. SVG 无自动排版，每个元素都要显式坐标；先算好布局再写代码。
6. 文件保存为 UTF-8，中文直接书写，无需转义。
7. 生成后**必须**用 XML 解析校验（见下），再交付。

## 12. 校验与预览

```bash
# XML 校验
python3 -c "import xml.etree.ElementTree as ET; ET.parse('输出.svg'); print('OK')"

# 渲染 PNG 预览（自动处理 cairosvg 缺失）
python3 scripts/render_preview.py 输出.svg
```

预览图字体可能走回退字体（cairosvg 不加载网页字体），告知用户以浏览器打开 SVG 为准。
