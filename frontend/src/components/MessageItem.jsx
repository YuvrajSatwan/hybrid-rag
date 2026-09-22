import { useState, useCallback } from 'react'
import CitationItem from './CitationItem'
import { parseMarkdown, parseInline } from '../lib/markdown'
import styles from './MessageItem.module.css'

// ─── Inline Content ──────────────────────────────────────────────────────────
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
          className={styles.citeChip}
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

// ─── Code Block with Copy ────────────────────────────────────────────────────
function CodeBlock({ lang, code }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
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

// ─── Markdown Blocks Renderer ────────────────────────────────────────────────
function BlocksRenderer({ blocks, onJumpToSource }) {
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
    return (
      <p key={i} className={styles.para}>
        <InlineContent text={block.content} onJumpToSource={onJumpToSource} />
      </p>
    )
  })
}

// ─── Main Message Component ──────────────────────────────────────────────────
export default function MessageItem({
  message,
  onRetry,
}) {
  const { id, role, content, citations = [], latency_ms, error } = message
  const [sourcesOpen, setSourcesOpen] = useState(false)
  const [highlightedIndex, setHighlightedIndex] = useState(null)

  const handleJumpToSource = useCallback((sourceIndex) => {
    setSourcesOpen(true)
    setTimeout(() => {
      const el = document.getElementById(`source-item-${sourceIndex}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
        setHighlightedIndex(sourceIndex)
        setTimeout(() => setHighlightedIndex(null), 2000)
      }
    }, 50)
  }, [])

  if (role === 'user') {
    return (
      <div className={styles.userRow}>
        <div className={styles.userBubble}>
          <p className={styles.userText}>{content}</p>
        </div>
      </div>
    )
  }

  // Assistant message
  if (error) {
    return (
      <div className={styles.assistantRow}>
        <div className={styles.errorBox}>
          <div className={styles.errorHeader}>
            <AlertIcon />
            <span className={styles.errorTitle}>Error generating answer</span>
          </div>
          <p className={styles.errorMsg}>{content}</p>
          {onRetry && (
            <button
              type="button"
              className={styles.retryBtn}
              onClick={() => onRetry(id)}
            >
              Try again
            </button>
          )}
        </div>
      </div>
    )
  }

  const { blocks } = parseMarkdown(content || '')
  const hasCitations = citations && citations.length > 0
  const sourcesLabel = citations.length === 1 ? '1 Source' : `${citations.length} Sources`

  return (
    <div className={styles.assistantRow}>
      <div className={styles.assistantContent}>
        {/* Render documentation-grade markdown text */}
        <div className={styles.prose}>
          <BlocksRenderer blocks={blocks} onJumpToSource={handleJumpToSource} />
        </div>

        {/* Latency badge if available */}
        {latency_ms != null && (
          <div className={styles.metaFooter}>
            <span className={styles.latency}>
              Answered in {(latency_ms / 1000).toFixed(2)}s
            </span>
          </div>
        )}

        {/* Expandable Citations / Sources */}
        {hasCitations && (
          <div className={styles.sourcesWrapper}>
            <button
              type="button"
              className={styles.sourcesToggle}
              onClick={() => setSourcesOpen(!sourcesOpen)}
              aria-expanded={sourcesOpen}
            >
              <ChevronIcon className={`${styles.chevron} ${sourcesOpen ? styles.chevronOpen : ''}`} />
              <span className={styles.sourcesToggleLabel}>{sourcesLabel}</span>
            </button>

            {sourcesOpen && (
              <div className={styles.sourcesList}>
                {citations.map((c, i) => (
                  <CitationItem
                    key={c.chunk_id || i}
                    citation={c}
                    index={i}
                    isHighlighted={highlightedIndex === i + 1}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function ChevronIcon({ className }) {
  return (
    <svg className={className} width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 18 15 12 9 6" />
    </svg>
  )
}

function CopyIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  )
}

function CheckIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  )
}

function AlertIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}
