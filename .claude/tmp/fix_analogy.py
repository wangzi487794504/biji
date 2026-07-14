with open('C:/笔记/biji/模型应用/2.优化与激活.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 64 (0-indexed) = "cosθ..." - keep it
# Line 65-66 (0-indexed 64-65) = broken analogy lines - replace entirely
# Line 67 (0-indexed 66) = blank line - keep
# Line 68 (0-indexed 67) = blank line - keep

# The correct analogy paragraph as a single line
analogy = '* 一个直观的类比：想象一根木棍，一头钉在你脚下，另一头指向空中某个方向。这根木棍就是梯度 $\\nabla L$——它指向最陡的上坡方向，长度等于那个方向的坡度。现在你想知道：如果朝另一个方向走（比如偏左 30°），坡度是多少？答案很简单——把木棍投影到你想走的那条线上。投影的长度，就是那个方向的坡度。如果你选的线和木棍完全重合，投影就是木棍本身的长度——坡度最大；如果你选的线和木棍垂直，投影长度为 0——那是平路，高度不变（等高线方向）；如果你背向木棍走（夹角 180°），投影是负的最大——最陡的下坡方向。所以，梯度自动成为最陡方向，不是巧合：任何其他方向都是它的"打折投影"，折扣由夹角的余弦决定。余弦最大是 1，此时夹角为 0——完全同向，投影不打折，当然最陡。\n'

# Replace lines 64-65 (indices) with just the analogy, keep blank lines
new_lines = lines[:64] + [analogy] + ['\n', '\n'] + lines[68:]

with open('C:/笔记/biji/模型应用/2.优化与激活.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed')
