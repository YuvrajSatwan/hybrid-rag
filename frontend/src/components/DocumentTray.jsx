import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import styles from './DocumentTray.module.css'

const ALLOWED_EXTS = ['.pdf', '.md', '.txt', '.html']
const MAX_FILE_SIZE = 20 * 1024 * 1024 // 20 MB

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

export default function DocumentTray({
  documents = [],
  onDeleteDocument,
  onUploadFiles,
  onRetryDocument,
  _isUploading = false,
}) {
  const [showAddDrop, setShowAddDrop] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const [rejections, setRejections] = useState([])
  const [confirmDeleteDoc, setConfirmDeleteDoc] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const fileInputRef = useRef(null)
  const cancelBtnRef = useRef(null)

  // Listen for Escape key to close confirmation modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && confirmDeleteDoc) {
        setConfirmDeleteDoc(null)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [confirmDeleteDoc])

  // Focus cancel button when modal opens for safety
  useEffect(() => {
    if (confirmDeleteDoc && cancelBtnRef.current) {
      cancelBtnRef.current.focus()
    }
  }, [confirmDeleteDoc])

  const handleFiles = async (filesList) => {
    const incoming = Array.from(filesList)
    if (!incoming.length) return

    const newlyValid = []
    const newlyRejected = []

    for (const f of incoming) {
      const ext = '.' + f.name.split('.').pop().toLowerCase()
      if (!ALLOWED_EXTS.includes(ext)) {
        newlyRejected.push({
          name: f.name,
          reason: `Unsupported format (${ext || 'unknown'}). Supported: PDF, Markdown (.md), TXT, HTML.`,
        })
        continue
      }
      if (f.size === 0) {
        newlyRejected.push({
          name: f.name,
          reason: 'File is empty (0 bytes).',
        })
        continue
      }
      if (f.size > MAX_FILE_SIZE) {
        newlyRejected.push({
          name: f.name,
          reason: 'Files must be smaller than 20 MB.',
        })
        continue
      }
      newlyValid.push(f)
    }

    if (newlyRejected.length > 0) {
      setRejections(newlyRejected)
    } else {
      setRejections([])
    }

    if (newlyValid.length > 0) {
      try {
        await onUploadFiles(newlyValid)
        setShowAddDrop(false)
      } catch (err) {
        setRejections([
          {
            name: 'Upload error',
            reason: err.message || 'Failed to upload documents.',
          },
        ])
      }
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files)
    }
  }

  const handleConfirmDelete = async () => {
    if (!confirmDeleteDoc || isDeleting) return
    setIsDeleting(true)
    try {
      await onDeleteDocument(confirmDeleteDoc.document_id)
      setConfirmDeleteDoc(null)
    } finally {
      setIsDeleting(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.titleGroup}>
          <span className={styles.label}>Documents</span>
          <span className={styles.countBadge}>{documents.length}</span>
        </div>
        <button
          type="button"
          className={styles.addBtn}
          onClick={() => {
            setShowAddDrop((prev) => !prev)
            if (fileInputRef.current) fileInputRef.current.click()
          }}
          title="Upload more documents"
        >
          <PlusIcon />
          <span>Add documents</span>
        </button>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.md,.txt,.html"
        style={{ display: 'none' }}
        onChange={(e) => {
          if (e.target.files?.length) {
            handleFiles(e.target.files)
            e.target.value = ''
          }
        }}
      />

      {/* Validation / Rejection Banners */}
      <AnimatePresence>
        {rejections.length > 0 && (
          <motion.div
            className={styles.rejectionsWrapper}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            {rejections.map((rej, i) => (
              <div key={i} className={styles.rejectionItem}>
                <AlertIcon />
                <div className={styles.rejectionText}>
                  <strong>{rej.name}:</strong> {rej.reason}
                </div>
                <button
                  type="button"
                  className={styles.closeRejBtn}
                  onClick={() => setRejections((prev) => prev.filter((_, idx) => idx !== i))}
                  aria-label="Dismiss error"
                >
                  ×
                </button>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Inline Dropzone Accordion */}
      <AnimatePresence>
        {showAddDrop && (
          <motion.div
            className={`${styles.inlineDrop} ${dragOver ? styles.dropActive : ''}`}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            onDragOver={(e) => {
              e.preventDefault()
              setDragOver(true)
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            aria-label="Drop additional files here or press Enter to browse"
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                fileInputRef.current?.click()
              }
            }}
          >
            <UploadIcon />
            <span>
              {dragOver ? (
                <strong>Drop to upload</strong>
              ) : (
                'Drop additional files here or click to browse'
              )}
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Document List Rows */}
      <div className={styles.cardList} role="list">
        {documents.map((doc) => {
          const status = (doc.status || 'Ready').toUpperCase()
          const isReady = status === 'READY'
          const isIndexing = status === 'INDEXING' || status === 'PROCESSING' || status === 'UPLOADING'
          const isFailed = status === 'FAILED'
          const ext = getFileExt(doc.filename)

          return (
            <div key={doc.document_id} className={styles.docCard} role="listitem">
              <div className={styles.docLeft}>
                <span className={`${styles.extBadge} ${styles[ext] || ''}`}>
                  {ext.toUpperCase()}
                </span>
                <span className={styles.docName} title={doc.filename}>
                  {doc.filename}
                </span>
                {doc.file_size > 0 && (
                  <span className={styles.docSize}>{formatBytes(doc.file_size)}</span>
                )}
                {isReady && doc.chunk_count > 0 && (
                  <span className={styles.chunkMeta}>
                    {doc.chunk_count} {doc.chunk_count === 1 ? 'chunk' : 'chunks'}
                  </span>
                )}
              </div>

              <div className={styles.docRight}>
                <span
                  className={`${styles.badge} ${
                    isReady ? styles.ready : isIndexing ? styles.indexing : isFailed ? styles.failed : ''
                  }`}
                  title={doc.error || (doc.chunk_count ? `${doc.chunk_count} chunks indexed` : undefined)}
                >
                  {isIndexing && <span className={styles.pulseDot} />}
                  {status}
                </span>

                {isFailed && onRetryDocument && (
                  <button
                    type="button"
                    className={styles.retryBtn}
                    onClick={() => onRetryDocument(doc)}
                    title="Retry processing this document"
                  >
                    Retry
                  </button>
                )}

                <button
                  type="button"
                  className={styles.deleteBtn}
                  onClick={() => setConfirmDeleteDoc(doc)}
                  title={`Delete ${doc.filename}`}
                  aria-label={`Delete ${doc.filename}`}
                >
                  <TrashIcon />
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Delete Confirmation Modal */}
      <AnimatePresence>
        {confirmDeleteDoc && (
          <div
            className={styles.modalBackdrop}
            onClick={() => setConfirmDeleteDoc(null)}
            role="presentation"
          >
            <motion.div
              className={styles.modalDialog}
              role="dialog"
              aria-modal="true"
              aria-labelledby="confirm-delete-title"
              onClick={(e) => e.stopPropagation()}
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{ duration: 0.15 }}
            >
              <div className={styles.modalHeader}>
                <h3 id="confirm-delete-title" className={styles.modalTitle}>
                  Delete {confirmDeleteDoc.filename}?
                </h3>
              </div>
              <p className={styles.modalDescription}>
                This document will no longer be used for answers.
              </p>
              <div className={styles.modalActions}>
                <button
                  ref={cancelBtnRef}
                  type="button"
                  className={styles.modalCancelBtn}
                  onClick={() => setConfirmDeleteDoc(null)}
                  disabled={isDeleting}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className={styles.modalConfirmBtn}
                  onClick={handleConfirmDelete}
                  disabled={isDeleting}
                >
                  {isDeleting ? 'Deleting…' : 'Delete document'}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}

function PlusIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  )
}

function UploadIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
  )
}

function TrashIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    </svg>
  )
}

function AlertIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}
