import { useState } from 'react'
import styles from './CitationItem.module.css'

const SNIPPET_CHAR_LIMIT = 220

export default function CitationItem({
  citation,
  index,
  isHighlighted = false,
}) {
  const { title, source_url, snippet = '', page, filename, section } = citation
  const [expanded, setExpanded] = useState(false)

  const displayName = filename || title || 'Document'
  const parts = []
  if (page) parts.push(`Page ${page}`)
  if (section && section !== displayName) parts.push(section)
  const metaText = parts.join(' · ')

  const cleanSnippet = snippet.trim()
  const isLong = cleanSnippet.length > SNIPPET_CHAR_LIMIT
  const displaySnippet = !isLong || expanded
    ? cleanSnippet
    : cleanSnippet.slice(0, SNIPPET_CHAR_LIMIT) + '…'

  const hasLink = Boolean(source_url)

  return (
    <div
      id={`source-item-${index + 1}`}
      className={`${styles.item} ${isHighlighted ? styles.highlighted : ''}`}
    >
      <div className={styles.topRow}>
        <div className={styles.badgeGroup}>
          <span className={styles.indexCircle}>{index + 1}</span>
          <span className={styles.title} title={displayName}>
            {displayName}
          </span>
          {metaText && <span className={styles.metaText}>{metaText}</span>}
        </div>

        {hasLink && (
          <a
            href={source_url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.linkBtn}
            title="Open source"
          >
            <ExternalLinkIcon />
          </a>
        )}
      </div>

      {cleanSnippet && (
        <div className={styles.excerptWrap}>
          <p className={styles.excerpt}>
            &ldquo;{displaySnippet}&rdquo;
          </p>
          {isLong && (
            <button
              type="button"
              className={styles.expandBtn}
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? 'Show less' : 'Show full excerpt'}
            </button>
          )}
        </div>
      )}
    </div>
  )
}

function ExternalLinkIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
      <polyline points="15 3 21 3 21 9" />
      <line x1="10" y1="14" x2="21" y2="3" />
    </svg>
  )
}
