from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# === Color Palette ===
BG       = RGBColor(0xFF, 0xFF, 0xFF)  # white
DARK     = RGBColor(0x1A, 0x1A, 0x1A)  # near black text
GRAY     = RGBColor(0x66, 0x66, 0x66)  # secondary text
LIGHT_BG = RGBColor(0xF5, 0xF5, 0xF5)  # light gray card bg
BLUE     = RGBColor(0x25, 0x6D, 0xEB)  # primary accent
RED      = RGBColor(0xE0, 0x3E, 0x2D)  # danger/highlight
GREEN    = RGBColor(0x16, 0xA3, 0x4A)  # success
ORANGE   = RGBColor(0xE6, 0x7E, 0x22)  # warning
BORDER   = RGBColor(0xE0, 0xE0, 0xE0)  # subtle border

def add_bg(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG

def add_rect(slide, left, top, width, height, fill_color=LIGHT_BG, border=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border:
        shape.line.color.rgb = border
        shape.line.width = Pt(0.5)
    else:
        shape.line.fill.background()
    return shape

def tb(slide, left, top, width, height, text, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT):
    """Simple text box helper"""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = 'Microsoft YaHei'
    p.alignment = align
    return tf

def multi(slide, left, top, width, height, lines, size=16, color=DARK, spacing=1.3):
    """lines = list of (text, bold, color_override, size_override)"""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if isinstance(line, str):
            t, b, c, s = line, False, color, size
        else:
            t = line[0]
            b = line[1] if len(line) > 1 else False
            c = line[2] if len(line) > 2 else color
            s = line[3] if len(line) > 3 else size
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = t
        p.font.size = Pt(s)
        p.font.color.rgb = c
        p.font.bold = b
        p.font.name = 'Microsoft YaHei'
        p.space_after = Pt(s * (spacing - 1))
    return tf

def divider(slide, left, top, width):
    add_rect(slide, left, top, width, Pt(3), BLUE, None)

def page_number(slide, n):
    tb(slide, Inches(12.2), Inches(7.0), Inches(0.8), Inches(0.4),
       str(n).zfill(2), size=12, color=GRAY, align=PP_ALIGN.RIGHT)

def card(slide, left, top, width, height, title, body_lines, title_color=DARK, body_size=14):
    """A card with title and body text"""
    add_rect(slide, left, top, width, height, LIGHT_BG, BORDER)
    tb(slide, left + Inches(0.3), top + Inches(0.2), width - Inches(0.6), Inches(0.4),
       title, size=16, color=title_color, bold=True)
    multi(slide, left + Inches(0.3), top + Inches(0.65), width - Inches(0.6), height - Inches(0.8),
          body_lines, size=body_size)

# ═══════════════════════════════════════════════
# SLIDE 1: COVER
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
# Top accent line
add_rect(s, Inches(0), Inches(0), prs.slide_width, Pt(4), BLUE)
# Chapter number
tb(s, Inches(1.5), Inches(1.5), Inches(3), Inches(0.5), '第一章', size=16, color=BLUE, bold=True)
# Title
tb(s, Inches(1.5), Inches(2.1), Inches(10), Inches(1.2), '从函数到神经网络', size=48, color=DARK, bold=True)
# Subtitle
tb(s, Inches(1.5), Inches(3.3), Inches(8), Inches(0.6), '让电脑认出猫的完整旅程', size=22, color=GRAY)
# Divider
divider(s, Inches(1.5), Inches(4.1), Inches(2.5))
# Description
tb(s, Inches(1.5), Inches(4.6), Inches(8), Inches(0.8),
    '从 y=wx+b 出发，经过8个因果转折，搭建出一个能识别猫的深度神经网络。\n每一步都是对前一步困境的回应。',
    size=15, color=GRAY)
# Bottom bar
add_rect(s, Inches(0), Inches(7.2), prs.slide_width, Inches(0.3), BLUE)

# ═══════════════════════════════════════════════
# SLIDE 2: PROBLEM
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 2)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '怎样让电脑认出猫？', size=34, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

cards = [
    ('❌  方案一：写规则', RED,
     ['"如果尖耳朵、圆眼睛、长胡须 → 是猫"',
      '猫会趴着、仰着、藏在盒子里……',
      '用死板规则穷尽所有可能性 → 此路不通']),
    ('💡  方案二：找一个映射器', ORANGE,
     ['给一个黑箱：输入 300万个像素值 → 输出 猫的概率',
      '数学上，这种映射关系就叫函数',
      '但猫识别函数不可能靠人手写出来']),
    ('🎯  最终答案', GREEN,
     ['搭建一个极其灵活的函数毛坯（神经网络）',
      '用大量标注好的猫照片反复"打磨"它',
      '每看一张图，毛坯自我调整一点 → 最终长成猫识别器']),
]
for i, (title, tcolor, lines) in enumerate(cards):
    x = Inches(1.2 + i * 3.8)
    card(s, x, Inches(2.0), Inches(3.4), Inches(3.0), title, lines, title_color=tcolor)

# Bottom insight
add_rect(s, Inches(1.2), Inches(5.5), Inches(10.9), Inches(0.8), RGBColor(0xE8, 0xF0, 0xFE), BLUE)
multi(s, Inches(1.6), Inches(5.6), Inches(10), Inches(0.6),
      [('核心思想：让计算机自己把函数"造"出来 —— 不是编程，是训练。', True, BLUE, 17)])

# ═══════════════════════════════════════════════
# SLIDE 3: LINEAR AND ITS LIMITS
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 3)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '1.1  线性函数：最简单的起点，最深的瓶颈', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# Left panel: the formula
tb(s, Inches(1.2), Inches(1.8), Inches(5), Inches(0.5), '最基本的单元', size=14, color=GRAY)
tb(s, Inches(1.2), Inches(2.3), Inches(5), Inches(1.0), 'y  =  w x  +  b', size=48, color=DARK, bold=True)
multi(s, Inches(1.2), Inches(3.3), Inches(5), Inches(1.5), [
    ('w — 权重：控制影响力的大小和方向', False, DARK, 15),
    ('b — 偏置：让直线可以上下平移', False, DARK, 15),
    ('推广到300万像素： y = Σ wᵢxᵢ + b', False, GRAY, 14),
])

# Right: geometry
card(s, Inches(7.0), Inches(1.8), Inches(5.2), Inches(2.8),
     '几何意义：超平面"一刀切"', [
         '',
         '线性可分（理想）：●●●  |  ○○○  ← 一刀清',
         '线性不可分（现实）：●○●  |  ○●○  ← 任何直线都切错！',
         '',
         '只有两个自由度（w和b），无法表达猫的复杂视觉模式。',
     ], title_color=DARK)

# Conclusion box
add_rect(s, Inches(1.2), Inches(5.3), Inches(10.9), Inches(0.8), RGBColor(0xFD, 0xED, 0xEC), RED)
multi(s, Inches(1.6), Inches(5.4), Inches(10), Inches(0.6),
      [('单层线性函数，表达能力太弱。', True, RED, 18)])

# ═══════════════════════════════════════════════
# SLIDE 4: LINEAR + LINEAR = LINEAR
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 4)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '多叠几层行不行？', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# Proof
tb(s, Inches(1.2), Inches(1.9), Inches(5), Inches(0.5), '代数证明', size=16, color=BLUE, bold=True)
multi(s, Inches(1.2), Inches(2.5), Inches(5.5), Inches(2.5), [
    ('第一层（n个线性函数并行）：', False, GRAY, 14),
    ('h₁ = w₁₁x₁ + w₁₂x₂ + … + b₁', False, DARK, 15),
    ('h₂ = w₂₁x₁ + w₂₂x₂ + … + b₂', False, DARK, 15),
    ('...', False, DARK, 15),
    ('', False, DARK, 6),
    ('第二层（加权组合）：', False, GRAY, 14),
    ('y = v₁h₁ + v₂h₂ + … + vₙhₙ + c', False, DARK, 15),
    ('', False, DARK, 6),
    ('展开合并同类项后：', False, GRAY, 14),
    ('y = w\'₁x₁ + w\'₂x₂ + … + b\'  ← 依然是线性！', False, RED, 17),
])

# Matrix proof
card(s, Inches(7.2), Inches(1.9), Inches(5.0), Inches(2.5),
     '矩阵形式更简洁', [
         '',
         'y = W₂(W₁x + b₁) + b₂',
         '  = (W₂W₁)x + (W₂b₁ + b₂)',
         '  = W\'x + b\'',
         '',
         '两个矩阵相乘 → 还是一个矩阵',
         '无论叠多少层 → 等效单层线性',
     ], title_color=DARK)

# Key takeaway
add_rect(s, Inches(1.2), Inches(5.3), Inches(10.9), Inches(1.0), RGBColor(0xFD, 0xED, 0xEC), RED)
multi(s, Inches(1.6), Inches(5.35), Inches(10), Inches(0.9),
      [('堆叠解决不了问题。线性 + 线性 = 线性。', True, RED, 22),
       ('我们需要的是 —— 非线性。', True, RED, 18)])

# ═══════════════════════════════════════════════
# SLIDE 5: ACTIVATION FUNCTIONS
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 5)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '2.  激活函数：打破线性魔咒', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# ReLU card
card(s, Inches(1.2), Inches(1.9), Inches(3.5), Inches(4.5),
     'ReLU — 当今标配', [
         '',
         'ReLU(z) = max(0, z)',
         '',
         'z > 0 → 原样通过（导数=1）',
         'z ≤ 0 → 一刀截断（导数=0）',
         '',
         '✅ 正区间导数恒为1，永不衰减',
         '✅ 计算极其廉价（一次比较）',
         '⚠️ 死亡神经元风险',
     ], title_color=GREEN)

# Sigmoid/Tanh card
card(s, Inches(5.0), Inches(1.9), Inches(3.5), Inches(4.5),
     'Sigmoid / Tanh — 曾经的王者', [
         '',
         'σ(z) = 1 / (1 + e⁻ᶻ)',
         'tanh(z) = (eᶻ − e⁻ᶻ)/(eᶻ + e⁻ᶻ)',
         '',
         '输出平滑、有界、连续',
         '',
         '❌ 饱和区导数≈0 → 梯度消失',
         '❌ 深度网络中浅层无法训练',
     ], title_color=RED)

# Why ReLU wins
card(s, Inches(8.8), Inches(1.9), Inches(3.5), Inches(4.5),
     '为什么 ReLU 胜出？', [
         '',
         'Sigmoid 导数最大值：0.25',
         '50层：0.25⁵⁰ ≈ 10⁻³¹ ≈ 0',
         '',
         'ReLU 导数（正区间）：恒为 1',
         '50层：依然为 1！',
         '',
         '→ 梯度直达，深层也能训练',
         '',
         '简单 打败了 优雅。',
     ], title_color=BLUE)

# ═══════════════════════════════════════════════
# SLIDE 6: UNIVERSAL APPROXIMATION
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 6)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '万能逼近定理：用"小山丘"拼出任意函数', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

tb(s, Inches(1.2), Inches(1.8), Inches(10), Inches(0.5),
    '直觉：两个 ReLU → 一个三角山丘 → 足够多的山丘 → 逼近任意连续曲线', size=16, color=GRAY)

# Hill formula
card(s, Inches(1.2), Inches(2.5), Inches(6.5), Inches(2.0),
     '山丘的构造（三个 ReLU 配合）', [
         'f(x) = ReLU(x+1) + ReLU(x-1) − 2·ReLU(x)',
         'x < −1 → 0    |   −1 ≤ x < 0 → 上升    |   0 ≤ x < 1 → 下降    |   x ≥ 1 → 0',
         '调整 ReLU 的权重和拐点 → 控制山丘的位置、宽度、高度、形状',
     ], title_color=DARK, body_size=16)

# Theorem box
card(s, Inches(1.2), Inches(4.9), Inches(6.5), Inches(1.6),
     '📐  万能逼近定理（Cybenko, 1989）', [
         '一个隐藏层，神经元足够多 → 以任意精度逼近紧致集上的任意连续函数。',
         '定理保证"存在"这样的网络，但没说"怎么找到"——梯度下降解决后者。',
         '深度带来效率（而非表达能力）：浅层已经万能，但深度让表达变得经济。',
     ], title_color=BLUE, body_size=15)

# Fourier analogy
card(s, Inches(8.2), Inches(2.5), Inches(4.0), Inches(2.0),
     '类比：傅里叶级数', [
         '傅里叶：不同频率的正弦波拼出周期函数',
         '神经网络：不同位置的 ReLU 山丘拼出任意函数',
         '',
         '正弦波是全局的 → ReLU 山丘是局部的',
         '→ 对局部特征更灵活！',
     ], title_color=DARK, body_size=15)

# ═══════════════════════════════════════════════
# SLIDE 7: FULLY CONNECTED LAYER
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 7)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '3.  全连接层：从神经元到网络', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

tb(s, Inches(1.2), Inches(1.8), Inches(10), Inches(0.5),
    '规则：前一层的每一个神经元 → 连接 → 后一层的每一个神经元，每条连接有一个可学习权重。', size=16, color=GRAY)

# Key formula
tb(s, Inches(1.2), Inches(2.6), Inches(10), Inches(0.8),
    'a⁽ˡ⁺¹⁾  =  ReLU( W⁽ˡ⁾ a⁽ˡ⁾  +  b⁽ˡ⁾ )', size=36, color=DARK, bold=True)

# Three operations table
add_rect(s, Inches(1.2), Inches(3.6), Inches(10.9), Inches(1.8), LIGHT_BG, BORDER)
headers = ['矩阵乘法  W·a', '加偏置  +b', '激活函数  ReLU(·)']
descs = ['信息的混合与重组\n每个后层神经元从前层所有信号中\n提取自己关心的那部分', '阈值的平移\n即使前层输出全为零\n后层神经元仍有基线激活水平', '引入转折\n打破线性，让多层叠加有意义\n（第2节的核心结论）']
for i, (h, d) in enumerate(zip(headers, descs)):
    x = Inches(1.5 + i * 3.6)
    tb(s, x, Inches(3.8), Inches(3.2), Inches(0.4), h, size=18, color=BLUE, bold=True)
    tb(s, x, Inches(4.3), Inches(3.2), Inches(1.0), d, size=14, color=GRAY)

# Data flow
tb(s, Inches(1.2), Inches(5.8), Inches(10.9), Inches(0.5),
    '数据流：输入(300万像素) → 隐藏层1(边缘/纹理) → 隐藏层2(轮廓) → 隐藏层3(部件) → 输出(猫的概率)',
    size=15, color=GRAY)

# ═══════════════════════════════════════════════
# SLIDE 8: LOSS + GRADIENT DESCENT
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 8)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '4.  损失函数 × 梯度下降', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# 3 cards
card(s, Inches(1.2), Inches(1.9), Inches(3.4), Inches(2.5),
     '回归 → MSE', [
         'L = (1/m) Σ (ŷᵢ − yᵢ)²',
         '',
         '衡量预测值与真实值的欧几里得距离',
         '高斯噪声假设下的最大似然自然产物',
     ], title_color=DARK, body_size=15)

card(s, Inches(5.0), Inches(1.9), Inches(3.4), Inches(2.5),
     '分类 → 交叉熵', [
         'L = −[y·log(ŷ) + (1−y)·log(1−ŷ)]',
         '',
         'y=1时 L=−log(ŷ)：预测越错惩罚越大',
         '确信错误 → 指数级惩罚',
     ], title_color=DARK, body_size=15)

card(s, Inches(8.8), Inches(1.9), Inches(3.4), Inches(2.5),
     'Sigmoid + CE = 绝配', [
         '∂L/∂z = ŷ − y',
         '',
         '干净利落！没有饱和因子。',
         'ŷ=0.99 但 y=0 → 梯度=0.99 信号极强！',
         'MSE+Sigmoid 则 → 梯度消失 ❌',
     ], title_color=GREEN, body_size=15)

# Gradient descent
card(s, Inches(1.2), Inches(4.8), Inches(10.9), Inches(1.6),
     '梯度下降   w ← w − η·∇L     |    学习率η：太小→收敛慢，太大→震荡发散', [
         '随机梯度下降(SGD)：每次一个样本，噪声帮助跳出局部陷阱',
         'Mini-batch SGD：小批量求平均 → 标准的训练方式',
         'Momentum：累积速度惯性 → 加速通过平坦区，抑制震荡',
         'Adam：动量 + 自适应学习率 → 目前最广泛使用的优化器',
     ], title_color=BLUE, body_size=15)

# ═══════════════════════════════════════════════
# SLIDE 9: BACKPROPAGATION
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 9)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '5.  反向传播：链式法则的一次系统性传递', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

tb(s, Inches(1.2), Inches(1.8), Inches(10), Inches(0.5),
    '问题：百万个参数，逐一算偏导数需要百万次前向传播 → 计算爆炸。', size=16, color=GRAY)

# Chain rule
tb(s, Inches(1.2), Inches(2.6), Inches(10), Inches(0.6),
    '∂L/∂w  =  ∂L/∂ŷ   ·   ∂ŷ/∂z   ·   ∂z/∂w', size=36, color=DARK, bold=True)
multi(s, Inches(1.2), Inches(3.3), Inches(10.9), Inches(1.0), [
    ('       损失对输出     ×   激活函数导数   ×   这一层的输入', False, GRAY, 15),
    ('       "错得多离谱"       "局部敏感度"       "这个权重被用了多少"', False, GRAY, 14),
])

# Three key facts
for i, (title, desc, clr) in enumerate([
    ('O(n) 而非 O(n²)', '一次前向缓存中间值 + 一次反向传播误差信号 → 所有参数梯度一次性算出', BLUE),
    ('优美的镜像对称', '前向时数据流经 W，反向时误差流经 Wᵀ —— 每一步都是前向的"镜像"', BLUE),
    ('动态规划思想', '中间梯度 ∂L/∂z 只算一次，被后续所有参数梯度计算复用', BLUE),
]):
    card(s, Inches(1.2 + i * 3.8), Inches(4.5), Inches(3.4), Inches(2.0), title, [desc], title_color=clr, body_size=14)

# ═══════════════════════════════════════════════
# SLIDE 10: VANISHING GRADIENT
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 10)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '6.  梯度消失：为什么深度曾是奢侈品', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# Problem
add_rect(s, Inches(1.2), Inches(1.9), Inches(5.5), Inches(4.0), RGBColor(0xFD, 0xED, 0xEC), RED)
tb(s, Inches(1.6), Inches(2.1), Inches(4.8), Inches(0.4), 'Sigmoid 的致命缺陷', size=20, color=RED, bold=True)
multi(s, Inches(1.6), Inches(2.7), Inches(4.8), Inches(2.8), [
    ('Sigmoid导数：σ\'(z) = σ(z)(1−σ(z))', False, DARK, 17),
    ('最大值仅 0.25（当 σ(z)=0.5 时）', False, RED, 16),
    ('', False, DARK, 8),
    ('50层网络 × 每层 ≤0.25：', False, DARK, 15),
    ('梯度衰减为  0.25⁵⁰ ≈ 7.9×10⁻³¹', False, RED, 28),
    ('', False, DARK, 8),
    ('→ 浅层权重几乎不更新 → 深度白费', False, RED, 16),
])

# Solution
add_rect(s, Inches(7.2), Inches(1.9), Inches(5.0), Inches(4.0), RGBColor(0xE8, 0xF5, 0xE9), GREEN)
tb(s, Inches(7.6), Inches(2.1), Inches(4.4), Inches(0.4), 'ReLU 如何改变局面', size=20, color=GREEN, bold=True)
multi(s, Inches(7.6), Inches(2.7), Inches(4.4), Inches(2.8), [
    ('ReLU\'(z) = 1 (z>0) 或 0 (z≤0)', False, DARK, 17),
    ('正区间导数恒为 1，不衰减！', False, GREEN, 16),
    ('', False, DARK, 8),
    ('50层 → 只要神经元激活 → 梯度直达', False, DARK, 15),
    ('', False, DARK, 8),
    ('⚠️ 代价：死亡神经元', False, ORANGE, 14),
    ('（z始终≤0 → 梯度=0 → 永不更新）', False, GRAY, 13),
    ('→ Leaky ReLU/ELU/GELU 缓解', False, DARK, 14),
])

# ═══════════════════════════════════════════════
# SLIDE 11: OVERFITTING
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 11)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '7.  过拟合与泛化：学习的目标不是记住，是理解', size=28, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

# Three states
for i, (label, desc, clr, bg_clr) in enumerate([
    ('欠拟合', '模型太简单\n连训练数据中的\n模式都学不到', BLUE, RGBColor(0xE8, 0xF0, 0xFE)),
    ('适度拟合', '找到数据中的\n真实规律\n泛化到新数据', GREEN, RGBColor(0xE8, 0xF5, 0xE9)),
    ('过拟合', '网络太强\n背下所有细节\n包括噪音', RED, RGBColor(0xFD, 0xED, 0xEC)),
]):
    x = Inches(1.2 + i * 3.8)
    add_rect(s, x, Inches(1.9), Inches(3.4), Inches(1.8), bg_clr, clr)
    tb(s, x + Inches(0.3), Inches(2.1), Inches(2.8), Inches(0.4), label, size=22, color=clr, bold=True)
    tb(s, x + Inches(0.3), Inches(2.6), Inches(2.8), Inches(0.9), desc, size=14, color=DARK)

# Solutions
tb(s, Inches(1.2), Inches(4.2), Inches(10), Inches(0.5), '对抗过拟合的四件套', size=18, color=DARK, bold=True)
solns = [
    ('🛑  早停', '验证集损失不再下降\n→ 立刻停止训练', BLUE),
    ('🏋️  L2 正则化', '损失函数加 λ·Σw²\n惩罚过大的权重', ORANGE),
    ('🎲  Dropout', '每批随机关掉50%神经元\n强迫独立学习', GREEN),
    ('🔄  数据增强', '随机旋转/裁剪/翻转\n人为扩充数据多样性', RED),
]
for i, (title, desc, clr) in enumerate(solns):
    x = Inches(1.2 + i * 2.85)
    card(s, x, Inches(4.8), Inches(2.55), Inches(1.5), title, [desc], title_color=clr, body_size=13)

# ═══════════════════════════════════════════════
# SLIDE 12: CAUSAL CHAIN OVERVIEW
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s); page_number(s, 12)
tb(s, Inches(1.2), Inches(0.6), Inches(10), Inches(0.7), '全景回顾：8步因果链', size=30, color=DARK, bold=True)
divider(s, Inches(1.2), Inches(1.3), Inches(2))

chain = [
    ('①', '规则写不出来', '找函数映射器：300万像素 → 猫的概率'),
    ('②', '单层线性一刀切', '堆叠多层。但线性+线性=线性，堆叠无效'),
    ('③', '线性堆叠失败', '插入 ReLU：导数恒为1，打破梯度消失'),
    ('④', '定理保证能逼近任意函数', '全连接层 + 矩阵乘法系统化组织'),
    ('⑤', '随机参数毫无用处', '交叉熵损失 + 梯度下降 + Adam 优化'),
    ('⑥', '百万参数逐个算梯度不可能', '反向传播：链式法则一次算完 O(n)'),
    ('⑦', '深层网络梯度消失', 'ReLU 替代 Sigmoid：导数恒为1让50层训练成为可能'),
    ('⑧', '训练集全对、测试集全错', '早停 + L2 + Dropout + 数据增强 → 对抗过拟合'),
]

for i, (num, problem, solution) in enumerate(chain):
    y = Inches(2.1 + i * 0.6)
    # Number
    add_rect(s, Inches(1.2), y, Inches(0.45), Inches(0.45), BLUE)
    tb(s, Inches(1.25), y + Inches(0.02), Inches(0.4), Inches(0.4), num, size=14, color=BG, bold=True, align=PP_ALIGN.CENTER)
    # Arrow
    tb(s, Inches(1.8), y + Inches(0.02), Inches(0.2), Inches(0.4), '→', size=14, color=GRAY)
    # Problem
    tb(s, Inches(2.1), y + Inches(0.02), Inches(4.5), Inches(0.4), problem, size=15, color=DARK, bold=False)
    # Arrow
    tb(s, Inches(6.5), y + Inches(0.02), Inches(0.2), Inches(0.4), '→', size=14, color=BLUE)
    # Solution
    tb(s, Inches(6.8), y + Inches(0.02), Inches(5.5), Inches(0.4), solution, size=15, color=BLUE, bold=False)

# Bottom
add_rect(s, Inches(1.2), Inches(7.0), Inches(10.9), Inches(0.3), BLUE)

# ═══════════════════════════════════════════════
# SLIDE 13: CLOSING
# ═══════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_rect(s, Inches(0), Inches(0), prs.slide_width, Pt(4), BLUE)

tb(s, Inches(1.5), Inches(2.0), Inches(10), Inches(1.2), '它不是魔法', size=64, color=DARK, bold=True)
tb(s, Inches(1.5), Inches(3.2), Inches(10), Inches(0.7),
    '是数学、算法和工程在每一个瓶颈面前的精密协作。', size=24, color=GRAY)
divider(s, Inches(1.5), Inches(4.2), Inches(3))
multi(s, Inches(1.5), Inches(5.0), Inches(10), Inches(1.5), [
    ('从 y=wx+b 到能识别猫的深度网络——', False, DARK, 18),
    ('不是被编程的程序，而是从数据中自动生长出来的复合函数。', False, DARK, 18),
    ('最终得到的不是一个规则系统，而是一个学会了"理解"的数学结构。', False, GRAY, 16),
])

add_rect(s, Inches(0), Inches(7.2), prs.slide_width, Inches(0.3), BLUE)

# === SAVE ===
out = 'C:/笔记/biji/模型应用/assets/第一章_从函数到神经网络.pptx'
prs.save(out)
print(f'Saved: {out}')
print(f'Slides: {len(prs.slides)}')
