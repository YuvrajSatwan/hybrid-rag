import styles from './DocumentItem.module.css'

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function getFileExt(filename) {
  if (!filename || !filename.includes('.')) return 'doc'
  return filename.split('.').pop().toLowerCase()
}

export default function DocumentItem({
  doc,
  onDelete,
  onRetry,
  isSelected = false,
  onSelect,
}) {
  const { filename, file_size, status = 'Ready', chunk_count, progress } = doc
  const ext = getFileExt(filename)
  const normalizedStatus = status.toLowerCase()

  const isReady = normalizedStatus === 'ready'
  const isIndexing = normalizedStatus === 'indexing' || normalizedStatus === 'processing'
  const isUploading = normalizedStatus === 'uploading'
  const isFailed = normalizedStatus === 'failed'

  let statusLabel = 'Ready'
  if (isUploading) {
    statusLabel = progress != null ? `Uploading ${progress}%` : 'Uploading…'
  } else if (isIndexing) {
    statusLabel = 'Indexing…'
  } else if (isFailed) {
    statusLabel = 'Failed'
  }

  const metaText = [
    file_size > 0 ? formatBytes(file_size) : null,
    isReady && chunk_count > 0 ? `${chunk_count} ${chunk_count === 1 ? 'chunk' : 'chunks'}` : null,
  ].filter(Boolean).join(' · ')

  return (
    <div
      className={`${styles.item} ${isSelected ? styles.itemSelected : ''}`}
      onClick={onSelect}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onSelect?.()
        }
      }}
    >
      {/* File type icon badge */}
      <span className={`${styles.extBadge} ${styles[ext] || ''}`}>
        {ext.toUpperCase()}
      </span>

      {/* Main info */}
      <div className={styles.info}>
        <span className={styles.filename} title={filename}>
          {filename}
        </span>
        <div className={styles.metaRow}>
          {metaText && <span className={styles.metaText}>{metaText}</span>}
          {metaText && <span className={styles.dotSeparator}>·</span>}
          <div className={styles.statusWrap}>
            <span
              className={`${styles.statusDot} ${
                isReady
                  ? styles.statusReady
                  : isIndexing || isUploading
                  ? styles.statusPulse
                  : isFailed
                  ? styles.statusFailed
                  : ''
              }`}
            />
            <span className={styles.statusText}>{statusLabel}</span>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className={styles.actions} onClick={(e) => e.stopPropagation()}>
        {isFailed && onRetry && (
          <button
            type="button"
            className={styles.retryBtn}
            onClick={() => onRetry(doc)}
            title="Retry uploading this file"
          >
            Retry
          </button>
        )}

        <button
          type="button"
          className={styles.deleteBtn}
          onClick={() => onDelete(doc)}
          title={`Delete ${filename}`}
          aria-label={`Delete ${filename}`}
        >
          <TrashIcon />
        </button>
      </div>
    </div>
  )
}

function TrashIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    </svg>
  )
}
