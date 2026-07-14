export const meta = {
  name: 'book-writer',
  description: 'Multi-agent book writing system: execution → scoring + supervision + guardian → revise → finalize',
  phases: [
    { title: '分析', detail: '读取现有内容和章节规划' },
    { title: '执行', detail: '执行Agent撰写新内容' },
    { title: '评审', detail: '打分Agent + 监督Agent + 守护Agent 并行评审' },
    { title: '修订', detail: '根据评审意见修订内容' },
    { title: '终审', detail: '最终质量检查' },
  ],
}

// ============================================================
// 常量定义
// ============================================================

const QUALITY_THRESHOLD = 7.5  // 综合评分低于此阈值则需要修订
const MAX_REVISIONS = 2         // 最多修订次数

const BOOK_DIR = 'C:/笔记/biji/模型应用'
const OUTLINE_PATH = 'C:/笔记/biji/.claude/book-outline.md'

// ============================================================
// 评分维度
// ============================================================
const SCORING_SCHEMA = {
  type: 'object',
  properties: {
    technicalAccuracy: {
      type: 'number',
      description: '技术准确性 (0-10)：数学公式、算法描述、技术细节是否正确',
    },
    completeness: {
      type: 'number',
      description: '完整性 (0-10)：是否覆盖了该章节大纲要求的所有知识点',
    },
    readability: {
      type: 'number',
      description: '可读性 (0-10)：语言是否流畅，从问题出发的叙事是否自然，是否避免过于学术化',
    },
    educationalValue: {
      type: 'number',
      description: '教育价值 (0-10)：是否回答了"为什么"，是否建立了直觉，例子是否有启发性',
    },
    consistency: {
      type: 'number',
      description: '一致性 (0-10)：与前后章节的风格、术语、深度是否一致，是否与初稿风格吻合',
    },
    overallScore: {
      type: 'number',
      description: '综合评分 (0-10)：加权综合评分',
    },
    strengths: {
      type: 'array',
      items: { type: 'string' },
      description: '本段内容的亮点（2-4条）',
    },
    weaknesses: {
      type: 'array',
      items: { type: 'string' },
      description: '本段内容的不足（2-5条），每条需要具体的改进方向',
    },
    improvementSuggestions: {
      type: 'array',
      items: { type: 'string' },
      description: '具体的修改建议（3-6条），每一条都要是可操作的',
    },
  },
  required: ['overallScore', 'strengths', 'weaknesses', 'improvementSuggestions'],
}

const SUPERVISION_SCHEMA = {
  type: 'object',
  properties: {
    structureQuality: {
      type: 'number',
      description: '结构质量 (0-10)：章节内的小节划分是否合理，是否有清晰的层次',
    },
    logicalFlow: {
      type: 'number',
      description: '逻辑流畅度 (0-10)：从一个概念到下一个概念的过渡是否自然',
    },
    gapAnalysis: {
      type: 'array',
      items: { type: 'string' },
      description: '缺失内容分析：大纲要求但本章节遗漏的知识点',
    },
    transitionQuality: {
      type: 'number',
      description: '衔接质量 (0-10)：与前后章节的衔接暗示/过渡是否到位',
    },
    suggestions: {
      type: 'array',
      items: { type: 'string' },
      description: '结构层面的改进建议（2-4条）',
    },
  },
  required: ['gapAnalysis', 'suggestions'],
}

const GUARDIAN_SCHEMA = {
  type: 'object',
  properties: {
    mathematicalCorrectness: {
      type: 'number',
      description: '数学正确性 (0-10)：所有公式、推导、数学断言是否正确',
    },
    terminologyConsistency: {
      type: 'number',
      description: '术语一致性 (0-10)：关键术语的使用是否前后一致',
    },
    potentialMisunderstandings: {
      type: 'array',
      items: { type: 'string' },
      description: '可能导致读者误解的表述',
    },
    corrections: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          location: { type: 'string', description: '需要修正的位置描述' },
          issue: { type: 'string', description: '具体问题' },
          fix: { type: 'string', description: '修正建议' },
        },
      },
      description: '需要修正的技术错误列表',
    },
    isCorrect: {
      type: 'boolean',
      description: '整体技术内容是否基本正确（没有重大错误）',
    },
  },
  required: ['mathematicalCorrectness', 'corrections', 'isCorrect'],
}

// ============================================================
// Agent 提示词模板
// ============================================================

function executionPrompt(chapter, section, outline, existingContent) {
  return `你是一位深度学习教程的作者，正在撰写《从函数到大模型》一书。

## 你的写作任务

章节：${chapter}
小节：${section}

## 全书大纲参考
${outline}

## 本章现有内容
${existingContent || '（本章还没有内容，你将撰写第一版）'}

## 写作要求

1. **风格**：中文叙述，面向有编程基础但非ML专业的读者。从具体问题出发，逐步引入抽象概念。每个概念都回答"为什么需要它"。

2. **结构**：
   - 从一个具体的困惑或问题开始
   - 逐步展开概念，数学公式 + 直觉解释
   - 用类比和可视化思维帮助理解
   - 结尾处自然过渡到下一节

3. **深度**：不要在任何一个概念上蜻蜓点水。对关键概念，要追问到底。

4. **公式**：使用简单明了的 LaTeX 风格数学公式，用 $...$ 或 $$...$$ 包裹。

5. **长度**：这个小节的内容应该足够充实，通常在 500-2000 字之间，取决于主题复杂度。

6. **衔接**：开头与上一节自然衔接，结尾为下一节做铺垫。

请直接输出你撰写的教程内容，不要输出其他元信息。`
}

function scoringPrompt(content, chapter, section, outline) {
  return `你是一位严格的教学内容评审专家。请对以下教程内容进行多维度评分。

## 评审对象
章节：${chapter} / ${section}

## 大纲要求
${outline}

## 待评审内容
${content}

请从以下维度进行评分（0-10分），并给出具体、可操作的改进建议。
注意：你的评分要严格、公正。如果内容好就说好，如果不好就明确指出。`
}

function supervisionPrompt(content, chapter, section, outline, fullOutline) {
  return `你是一位书籍结构编辑，负责把控整本书的宏观结构和逻辑流。

## 当前评审
章节：${chapter} / ${section}

## 本章在大纲中的位置和要求
${outline}

## 全书结构概览
${fullOutline}

## 待评审内容
${content}

请从结构层面进行分析：小节划分是否合理？逻辑流是否顺畅？有没有遗漏大纲要求的知识点？与前后章节的衔接是否自然？`
}

function guardianPrompt(content, chapter, section) {
  return `你是一位深度学习技术专家，负责确保教程中所有技术内容的正确性。

## 当前评审
章节：${chapter} / ${section}

## 待评审内容
${content}

请仔细检查：
1. 所有数学公式和推导是否正确
2. 技术概念描述是否准确
3. 术语使用是否一致
4. 是否有可能导致读者误解的表述
5. 代码/伪代码（如果有）是否有错误

对每一个发现的问题，请给出具体的修正建议。
如果你的检查结果是没有重大错误，请把 isCorrect 设为 true。`
}

function revisionPrompt(originalContent, scoringResult, supervisionResult, guardianResult, chapter, section) {
  const s = scoringResult || {}
  const sup = supervisionResult || {}
  const g = guardianResult || {}
  return `你是一位深度学习教程的作者。你的初稿收到了以下评审意见，请根据意见修订你的内容。

## 原稿
${originalContent}

## 评分Agent的意见
综合评分：${s.overallScore ?? 'N/A'}/10
亮点：${(s.strengths || []).join('；')}
不足：${(s.weaknesses || []).join('；')}
改进建议：${(s.improvementSuggestions || []).join('；')}

## 监督Agent的意见
结构质量：${sup.structureQuality ?? 'N/A'}/10
缺失内容：${(sup.gapAnalysis || []).join('；')}
改进建议：${(sup.suggestions || []).join('；')}

## 守护Agent的意见
数学正确性：${g.mathematicalCorrectness ?? 'N/A'}/10
需要修正的问题：${(g.corrections || []).map(c => `${c.location}: ${c.issue} → ${c.fix}`).join('；')}
可能导致误解：${(g.potentialMisunderstandings || []).join('；')}

## 修订要求
1. 逐一处理所有评审意见
2. 守护Agent指出的技术错误必须修正
3. 监督Agent指出的结构问题需要调整
4. 评分Agent的建议要尽量采纳
5. 保持原有的叙事风格和流畅性
6. 直接输出修订后的完整内容，不需要标注修改位置`
}

// ============================================================
// 主流程
// ============================================================

// 解析用户输入
const userInput = args || {}
const chapter = userInput.chapter || '第二章'
const section = userInput.section || ''
const targetFile = userInput.file || `${BOOK_DIR}/神经网络.md`

// Phase 1: 分析现有内容
phase('分析')

log(`📖 正在准备：${chapter} ${section ? '→ ' + section : ''}`)

// 读取大纲
const outlineContent = await agent(
  `读取文件 ${OUTLINE_PATH}，返回该文件的完整内容。只返回文件内容，不要添加任何说明。`,
  { label: '读取大纲' }
)

// 读取现有内容
const existingContent = await agent(
  `读取文件 ${targetFile}，返回该文件的完整内容。只返回文件内容，不要添加任何说明。`,
  { label: '读取现有内容' }
)

// 解析对应章节的大纲要求
const chapterOutline = await agent(
  `从以下全书大纲中，提取出"${chapter}"（包括${section ? '其中的"' + section + '"小节' : '所有小节'}）的完整大纲内容。只返回相关的大纲条目，不要添加额外说明。

${outlineContent}`,
  { label: '提取章节大纲' }
)

// 如果指定了小节，提取该小节的上下文
let sectionContext = ''
if (section) {
  sectionContext = await agent(
    `在以下内容中，找到"${chapter}"的"${section}"小节前后的内容（前后各200字左右），帮助了解上下文。如果该小节还不存在，就返回"该小节尚未撰写"。

${existingContent}`,
    { label: '提取上下文' }
  )
}

log(`📝 开始撰写：${chapter} ${section}`)

// Phase 2: 执行Agent撰写
phase('执行')

let currentContent = await agent(
  executionPrompt(chapter, section, chapterOutline, sectionContext),
  { label: `撰写:${section || chapter}`, phase: '执行' }
)

log(`✅ 初稿完成，共约 ${currentContent.length} 字`)

// Phase 3: 并行评审
phase('评审')

log('🔍 三个Agent并行评审中...')

const [scoringResult, supervisionResult, guardianResult] = await parallel([
  () => agent(scoringPrompt(currentContent, chapter, section, chapterOutline), {
    label: '打分Agent',
    phase: '评审',
    schema: SCORING_SCHEMA,
  }),
  () => agent(supervisionPrompt(currentContent, chapter, section, chapterOutline, outlineContent), {
    label: '监督Agent',
    phase: '评审',
    schema: SUPERVISION_SCHEMA,
  }),
  () => agent(guardianPrompt(currentContent, chapter, section), {
    label: '守护Agent',
    phase: '评审',
    schema: GUARDIAN_SCHEMA,
  }),
])

// 汇总评审结果
const reviewSummary = {
  score: scoringResult?.overallScore || 0,
  isCorrect: guardianResult?.isCorrect || false,
  gaps: supervisionResult?.gapAnalysis || [],
  corrections: guardianResult?.corrections || [],
}

log(`📊 评审结果：
  - 综合评分：${reviewSummary.score}/10 ${reviewSummary.score >= QUALITY_THRESHOLD ? '✅' : '⚠️ 需要修订'}
  - 技术正确性：${reviewSummary.isCorrect ? '✅ 基本正确' : '❌ 存在错误'}
  - 缺失内容：${reviewSummary.gaps.length} 项
  - 技术修正：${reviewSummary.corrections.length} 处`)

// Phase 4: 修订循环
phase('修订')

let revisionCount = 0
let finalContent = currentContent

while (
  (reviewSummary.score < QUALITY_THRESHOLD || !reviewSummary.isCorrect || reviewSummary.gaps.length > 0) &&
  revisionCount < MAX_REVISIONS
) {
  revisionCount++
  log(`🔄 第 ${revisionCount} 次修订...`)

  finalContent = await agent(
    revisionPrompt(finalContent, scoringResult, supervisionResult, guardianResult, chapter, section),
    { label: `修订第${revisionCount}轮`, phase: '修订' }
  )

  // 并行重新打分和守护检查
  const [reScore, reGuardian] = await parallel([
    () => agent(
      scoringPrompt(finalContent, chapter, section, chapterOutline),
      { label: `重新打分第${revisionCount}轮`, phase: '修订', schema: SCORING_SCHEMA }
    ),
    () => agent(
      guardianPrompt(finalContent, chapter, section),
      { label: `重新守护第${revisionCount}轮`, phase: '修订', schema: GUARDIAN_SCHEMA }
    ),
  ])

  reviewSummary.score = reScore?.overallScore || 0
  reviewSummary.isCorrect = reGuardian?.isCorrect || false

  log(`📊 第 ${revisionCount} 次修订后：评分 ${reviewSummary.score}/10，${reviewSummary.isCorrect ? '✅ 技术正确' : '⚠️ 仍有问题'}`)
}

if (revisionCount >= MAX_REVISIONS && reviewSummary.score < QUALITY_THRESHOLD) {
  log(`⚠️ 已达最大修订次数 (${MAX_REVISIONS})，当前评分 ${reviewSummary.score}/10。建议人工审核。`)
}

// Phase 5: 终审
phase('终审')

log('🏁 终审中...')

const finalCheck = await agent(
  `请对以下最终版内容做一次快速终审，确认内容已经可以发布。

章节：${chapter} / ${section}

## 最终内容
${finalContent}

## 评审历史
- 综合评分：${reviewSummary.score}/10
- 技术正确：${reviewSummary.isCorrect ? '是' : '否'}
- 修订次数：${revisionCount}

请给出你的终审意见（一段话），包括：
1. 内容是否可以发布
2. 如果还有小问题，指出具体位置和修正建议
3. 与初稿风格的一致性评价`,
  { label: '终审', phase: '终审' }
)

log(`📋 终审意见：${finalCheck}`)

// 返回结果
return {
  chapter,
  section,
  content: finalContent,
  finalScore: reviewSummary.score,
  isCorrect: reviewSummary.isCorrect,
  revisions: revisionCount,
  finalCheck,
  reviewDetails: {
    scoring: scoringResult,
    supervision: supervisionResult,
    guardian: guardianResult,
  },
}
