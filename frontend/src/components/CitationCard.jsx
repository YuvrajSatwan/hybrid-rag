import { useState } from 'react'
import { motion } from 'framer-motion'
import styles from './CitationCard.module.css'

const SNIPPET_CHAR_LIMIT = 180

export default function CitationCard({ citation, index, isHighlighted = false }) {
  const { title, source_url, snippet, page, filename, section } = citation
  const [expanded, setExpanded] = useState(false)
  const hasLink = Boolean(source_url)
  const Tag = hasLink ? 'a' : 'div'

  const linkProps = hasLink
    ? { href: source_url, target: '_blank', rel: 'noopener noreferrer' }
    : {}

  const displayName = filename || title || 'Document'
  const parts = []
  if (page) parts.push(`Page ${page}`)
  if (section && section !== displayName) parts.push(section)
  const metaText = parts.join(' · ')

  const cleanSnippet = snippet?.trim() || ''
  const isLong = cleanSnippet.length > SNIPPET_CHAR_LIMIT
  const displaySnippet = !isLong || expanded
    ? cleanSnippet
    : cleanSnippet.slice(0, SNIPPET_CHAR_LIMIT) + '…'

  const ext = displayName.includes('.')
    ? displayName.split('.').pop().toLowerCase()
    : 'doc'

  return (
    <motion.div
      id={`source-card-${index + 1}`}
      className={`${styles.cardWrapper} ${isHighlighted ? styles.highlighted : ''}`}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1], delay: index * 0.04 }}
    >
      <Tag
        className={`${styles.card} ${hasLink ? styles.linked : ''}`}
        {...linkProps}
      >
        {/* Citation number & Type icon */}
        <div className={styles.leftCol}>
          <span className={styles.num}>{String(index + 1).padStart(2, '0')}</span>
          <span className={`${styles.typeBadge} ${styles[ext] || ''}`}>
            {ext.toUpperCase()}
          </span>
        </div>

        {/* Body */}
        <div className={styles.body}>
          <div className={styles.titleRow}>
            <p className={styles.title}>{displayName}</p>
            {hasLink && (
              <span className={styles.arrow} aria-hidden="true">
                <ArrowIcon />
              </span>
            )}
          </div>

          {metaText && <p className={styles.meta}>{metaText}</p>}

          {cleanSnippet && (
            <div className={styles.snippetContainer}>
              <p className={styles.snippet}>&ldquo;{displaySnippet}&rdquo;</p>
              {isLong && (
                <button
                  type="button"
                  className={styles.expandBtn}
                  onClick={(e) => {
                    e.preventDefault()
                    e.stopPropagation()
                    setExpanded(!expanded)
                  }}
                  aria-expanded={expanded}
                >
                  {expanded ? 'View less' : 'View more'}
                </button>
              )}
            </div>
          )}
        </div>
      </Tag>
    </motion.div>
  )
}

function ArrowIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="7" y1="17" x2="17" y2="7"/>
      <polyline points="7 7 17 7 17 17"/>
    </svg>
  )
}

