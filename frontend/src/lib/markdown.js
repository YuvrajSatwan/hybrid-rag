/**
 * Safe, minimal markdown renderer for LLM-generated answer text.
 *
 * SECURITY: This renderer does NOT accept raw HTML and never uses innerHTML
 * with untrusted content. All output is constructed from trusted React nodes
 * built via this parser — retrieved document content cannot inject HTML.
 *
 * Supported constructs:
 *   - Fenced code blocks with language: ```lang\ncode\n```
 *   - Headings (#, ##, ###, ####)
 *   - Blockquotes (> text)
 *   - Bullet lists (- or *)
 *   - Numbered lists (1. 2. etc.)
 *   - Horizontal rules (---)
 *   - Paragraphs (blank-line separated)
 *   - Inline: **bold**, *italic*, `code`, [N] citations
 */

/**
 * Parse a flat string into a list of block descriptors.
 */
function parseBlocks(text) {
  const rawLines = text.replace(/\r\n/g, '\n').split('\n')
  const blocks = []
  let buffer = []
  let inCodeBlock = false
  let codeBlockLang = ''
  let codeBlockLines = []

  const flushParagraph = () => {
    const joined = buffer.join('\n').trim()
    if (joined) blocks.push({ type: 'paragraph', content: joined })
    buffer = []
  }

  for (let i = 0; i < rawLines.length; i++) {
    const line = rawLines[i]

    // Code block toggle
    if (line.trim().startsWith('```')) {
      if (!inCodeBlock) {
        flushParagraph()
        inCodeBlock = true
        codeBlockLang = line.trim().slice(3).trim()
        codeBlockLines = []
      } else {
        inCodeBlock = false
        blocks.push({
          type: 'code_block',
          lang: codeBlockLang || 'text',
          code: codeBlockLines.join('\n'),
        })
        codeBlockLang = ''
        codeBlockLines = []
      }
      continue
    }

    if (inCodeBlock) {
      codeBlockLines.push(line)
      continue
    }

    // Headings
    const headingMatch = line.match(/^(#{1,4})\s+(.+)$/)
    if (headingMatch) {
      flushParagraph()
      blocks.push({
        type: 'heading',
        level: headingMatch[1].length,
        text: headingMatch[2].trim(),
      })
      continue
    }

    // Blockquotes
    if (line.startsWith('>')) {
      flushParagraph()
      const quoteText = line.replace(/^>\s?/, '')
      if (blocks.length && blocks[blocks.length - 1].type === 'blockquote') {
        blocks[blocks.length - 1].content += '\n' + quoteText
      } else {
        blocks.push({ type: 'blockquote', content: quoteText })
      }
      continue
    }

    // Horizontal rules
    if (/^(\*\*\*|---|___)$/.test(line.trim())) {
      flushParagraph()
      blocks.push({ type: 'hr' })
      continue
    }

    // Lists
    const isBullet  = /^[-*]\s+/.test(line)
    const isOrdered = /^\d+\.\s+/.test(line)
    const isBlank   = line.trim() === ''

    if (isBullet || isOrdered) {
      flushParagraph()
      const listType = isBullet ? 'ul' : 'ol'
      const itemText = line.replace(/^[-*]\s+/, '').replace(/^\d+\.\s+/, '')
      // Merge consecutive list items of same type
      if (blocks.length && blocks[blocks.length - 1].type === listType) {
        blocks[blocks.length - 1].items.push(itemText)
      } else {
        blocks.push({ type: listType, items: [itemText] })
      }
    } else if (isBlank) {
      flushParagraph()
    } else {
      buffer.push(line)
    }
  }

  flushParagraph()

  // Handle unclosed code block gracefully
  if (inCodeBlock && codeBlockLines.length > 0) {
    blocks.push({
      type: 'code_block',
      lang: codeBlockLang || 'text',
      code: codeBlockLines.join('\n'),
    })
  }

  return blocks
}

/**
 * Parse inline markdown within a single line of text.
 * Returns an array of React-renderable segments.
 * Each segment: { type: 'text'|'bold'|'italic'|'code'|'cite', value: string, n?: number }
 */
export function parseInline(text) {
  // Pattern captures: **bold**, *italic*, `code`, [N] citations
  const pattern = /\*\*(.+?)\*\*|(\*|_)(.+?)\2|`([^`]+)`|\[(\d+)\]/g
  const segments = []
  let last = 0
  let match

  while ((match = pattern.exec(text)) !== null) {
    if (match.index > last) {
      segments.push({ type: 'text', value: text.slice(last, match.index) })
    }

    if (match[1] !== undefined) {
      segments.push({ type: 'bold', value: match[1] })
    } else if (match[3] !== undefined) {
      segments.push({ type: 'italic', value: match[3] })
    } else if (match[4] !== undefined) {
      segments.push({ type: 'code', value: match[4] })
    } else if (match[5] !== undefined) {
      segments.push({ type: 'cite', value: match[0], n: parseInt(match[5], 10) })
    }

    last = match.index + match[0].length
  }

  if (last < text.length) {
    segments.push({ type: 'text', value: text.slice(last) })
  }

  return segments
}

/**
 * Parse markdown text into structured block objects for rendering.
 */
export function parseMarkdown(text) {
  if (!text) return { blocks: [] }
  return { blocks: parseBlocks(text) }
}

