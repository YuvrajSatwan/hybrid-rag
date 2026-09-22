import { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import CitationCard from './CitationCard'
import { parseMarkdown, parseInline } from '../lib/markdown'
import styles from './AnswerPanel.module.css'

// ─── Inline renderer ──────────────────────────────────────────────────────────
function InlineContent({ text, onJumpToSource }) {
  const segments = parseInline(text)
  return segments.map((seg, i) => {
    if (seg.type === 'bold') return <strong key={i}>{seg.value}</strong>
    if (seg.type === 'italic') return <em key={i}>{seg.value}</em>
    if (seg.type === 'code') return <code key={i} className={styles.inlineCode}>{seg.value}</code>
    if (seg.type === 'cite') {
      return (
        <button
          key={i}
          type="button"
          className={styles.citePill}
          onClick={() => onJumpToSource(seg.n)}
          title={`Jump to source [${seg.n}]`}
          aria-label={`Source citation ${seg.n}`}
        >
          {seg.n}
        </button>
      )
    }
    return <span key={i}>{seg.value}</span>
  })
}

// ─── Code Block Component with Copy ───────────────────────────────────────────
function CodeBlock({ lang, code }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Fallback
      setCopied(false)
    }
  }

  return (
    <div className={styles.codeBlockWrapper}>
      <div className={styles.codeHeader}>
        <span className={styles.codeLang}>{lang || 'text'}</span>
        <button
          type="button"
          className={styles.copyBtn}
          onClick={handleCopy}
          aria-label="Copy code to clipboard"
          title="Copy code"
        >
          {copied ? (
            <>
              <CheckIcon />
              <span>Copied</span>
            </>
          ) : (
            <>
              <CopyIcon />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className={styles.pre}>
        <code>{code}</code>
      </pre>
    </div>
  )
}

// ─── Block renderer ───────────────────────────────────────────────────────────
function Blocks({ blocks, onJumpToSource }) {
  return blocks.map((block, i) => {
    if (block.type === 'code_block') {
      return <CodeBlock key={i} lang={block.lang} code={block.code} />
    }
    if (block.type === 'heading') {
      const Tag = block.level <= 2 ? 'h3' : 'h4'
      return (
        <Tag key={i} className={styles[`heading${block.level}`] || styles.heading3}>
          <InlineContent text={block.text} onJumpToSource={onJumpToSource} />
        </Tag>
      )
    }
    if (block.type === 'blockquote') {
      return (
        <blockquote key={i} className={styles.blockquote}>
          <InlineContent text={block.content} onJumpToSource={onJumpToSource} />
        </blockquote>
      )
    }
    if (block.type === 'hr') {
      return <hr key={i} className={styles.dividerLine} />
    }
    if (block.type === 'ul') {
      return (
        <ul key={i} className={styles.list}>
          {block.items.map((item, j) => (
            <li key={j}><InlineContent text={item} onJumpToSource={onJumpToSource} /></li>
          ))}
        </ul>
      )
    }
    if (block.type === 'ol') {
      return (
        <ol key={i} className={styles.listOrdered}>
          {block.items.map((item, j) => (
            <li key={j}><InlineContent text={item} onJumpToSource={onJumpToSource} /></li>
          ))}
        </ol>
      )
    }
    // paragraph
    return (
      <p key={i} className={styles.para}>
        <InlineContent text={block.content} onJumpToSource={onJumpToSource} />
      </p>
    )
  })
}

// ─── Main component ───────────────────────────────────────────────────────────
const panelVariants = {
  hidden: { opacity: 0, y: 12 },
  show:   { opacity: 1, y: 0, transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] } },
}

export default function AnswerPanel({ _query, result }) {
  const { answer, citations } = result
  const { blocks } = parseMarkdown(answer)
  const sourcesLabel = citations.length === 1 ? '1 Source' : `${citations.length} Sources`

  const [highlightedSource, setHighlightedSource] = useState(null)

  const handleJumpToSource = useCallback((sourceIndex) => {
    const details = document.getElementById('citations-details')
    if (details) {
      details.open = true
    }
    const el = document.getElementById(`source-card-${sourceIndex}`)
    if (el) {
      setTimeout(() => {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        setHighlightedSource(sourceIndex)
        setTimeout(() => setHighlightedSource(null), 2200)
      }, 100)
    }
  }, [])

  return (
    <motion.div
      className={styles.root}
      variants={panelVariants}
      initial="hidden"
      animate="show"
    >
      <section className={styles.answerSection}>
        <div className={styles.answerBody}>
          <Blocks blocks={blocks} onJumpToSource={handleJumpToSource} />
        </div>
      </section>

      {/* Citations Dropdown */}
      {citations.length > 0 && (
        <details id="citations-details" className={styles.citationsDetails}>
          <summary className={styles.citationsSummary}>
            <ChevronRightIcon className={styles.summaryIcon} />
            <span>{sourcesLabel}</span>
          </summary>
          <div className={styles.citationsList}>
            {citations.map((c, i) => (
              <CitationCard
                key={c.chunk_id || i}
                citation={c}
                index={i}
                isHighlighted={highlightedSource === i + 1}
              />
            ))}
          </div>
        </details>
      )}
    </motion.div>
  )
}

function ChevronRightIcon({ className }) {
  return (
    <svg className={className} width="12" height="12" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 18 15 12 9 6"/>
    </svg>
  )
}

function CopyIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  )
}

function CheckIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
      stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  )
}

