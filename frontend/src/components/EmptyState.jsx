import { useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import styles from './EmptyState.module.css'

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

export default function EmptyState({
  onUploadFiles,
  isUploading = false,
  uploadProgress = {},
}) {
  const [dragOver, setDragOver] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState([])
  const [rejectedFiles, setRejectedFiles] = useState([])
  const fileInputRef = useRef(null)

  // Validate files individually: accept valid, explain rejected
  const handleFilesAdded = (filesList) => {
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
      setRejectedFiles((prev) => [...prev, ...newlyRejected])
    }

    if (newlyValid.length > 0) {
      setSelectedFiles((prev) => {
        const existingNames = new Set(prev.map((p) => p.name))
        const merged = [...prev]
        for (const vf of newlyValid) {
          if (!existingNames.has(vf.name)) {
            merged.push(vf)
          }
        }
        return merged
      })
    }
  }

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFilesAdded(e.dataTransfer.files)
    }
  }, [])

  const handleBrowseClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFilesAdded(e.target.files)
      e.target.value = ''
    }
  }

  const handleRemoveSelected = (name) => {
    setSelectedFiles((prev) => prev.filter((f) => f.name !== name))
  }

  const handleDismissRejected = (index) => {
    setRejectedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleStartUpload = async () => {
    if (!selectedFiles.length || isUploading) return
    try {
      await onUploadFiles(selectedFiles)
      setSelectedFiles([])
      setRejectedFiles([])
    } catch (err) {
      setRejectedFiles([
        {
          name: 'Upload error',
          reason: err.message || 'Failed to upload documents. Please try again.',
        },
      ])
    }
  }

  return (
    <div className={styles.root}>
      <motion.div
        className={styles.hero}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
      >
        <h1 className={styles.heading}>No documents</h1>
        <p className={styles.sub}>
          Upload a document to start asking questions.
        </p>

        {/* Hidden File Picker */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.md,.txt,.html"
          style={{ display: 'none' }}
          onChange={handleInputChange}
          aria-label="Upload documents file input"
        />

        {/* Dropzone with Drag, Drop, Browse and Keyboard support */}
        <div
          className={`${styles.dropzone} ${dragOver ? styles.dropzoneActive : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
          role="button"
          tabIndex={0}
          aria-label="File upload dropzone. Press Enter to browse files."
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              handleBrowseClick()
            }
          }}
        >
          <div className={styles.dropContent}>

            {dragOver ? (
              <div className={styles.dropTextGroup}>
                <p className={styles.dropMainTextHighlight}>Drop to upload</p>
                <p className={styles.dropSubText}>Release files to add them to your workspace</p>
              </div>
            ) : (
              <div className={styles.dropTextGroup}>
                <p className={styles.dropMainText}>
                  Drag &amp; drop files here
                </p>
                <p className={styles.dropSubText}>or use the file browser</p>
              </div>
            )}

            <button
              type="button"
              className={styles.browseBtn}
              onClick={(e) => {
                e.stopPropagation()
                handleBrowseClick()
              }}
              tabIndex={-1}
            >
              Browse files
            </button>

            <div className={styles.formatBadges}>
              <span className={styles.formatBadge}>PDF</span>
              <span className={styles.formatBadge}>Markdown</span>
              <span className={styles.formatBadge}>TXT</span>
              <span className={styles.formatBadge}>HTML</span>
              <span className={styles.formatSizeBadge}>Max 20 MB</span>
            </div>
          </div>
        </div>

        {/* Rejected Files UX */}
        <AnimatePresence>
          {rejectedFiles.length > 0 && (
            <motion.div
              className={styles.rejectionsWrapper}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              {rejectedFiles.map((rej, idx) => (
                <div key={idx} className={styles.rejectionItem}>
                  <div className={styles.rejectionIcon}>
                    <AlertIcon />
                  </div>
                  <div className={styles.rejectionBody}>
                    <span className={styles.rejectionFilename}>{rej.name}:</span>
                    <span className={styles.rejectionReason}>{rej.reason}</span>
                  </div>
                  <button
                    type="button"
                    className={styles.dismissRejectionBtn}
                    onClick={() => handleDismissRejected(idx)}
                    aria-label="Dismiss error"
                    title="Dismiss"
                  >
                    ×
                  </button>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Selected Files Queue */}
        <AnimatePresence>
          {selectedFiles.length > 0 && (
            <motion.div
              className={styles.fileList}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className={styles.queueHeader}>
                <span className={styles.queueTitle}>Ready for indexing</span>
                <span className={styles.queueCount}>
                  {selectedFiles.length} {selectedFiles.length === 1 ? 'file' : 'files'}
                </span>
              </div>

              {selectedFiles.map((file) => {
                const status = uploadProgress[file.name] || (isUploading ? 'Uploading' : 'Ready')
                const ext = getFileExt(file.name)

                return (
                  <div key={file.name} className={styles.fileItem}>
                    <div className={styles.fileItemLeft}>
                      <span className={`${styles.extBadge} ${styles[ext] || ''}`}>
                        {ext.toUpperCase()}
                      </span>
                      <span className={styles.fileName} title={file.name}>
                        {file.name}
                      </span>
                      <span className={styles.fileSize}>{formatBytes(file.size)}</span>
                    </div>

                    <div className={styles.fileItemRight}>
                      <span className={`${styles.statusBadge} ${styles[status.toLowerCase()] || ''}`}>
                        {status}
                      </span>
                      {!isUploading && (
                        <button
                          type="button"
                          className={styles.removeBtn}
                          onClick={(e) => {
                            e.stopPropagation()
                            handleRemoveSelected(file.name)
                          }}
                          title={`Remove ${file.name}`}
                          aria-label={`Remove ${file.name}`}
                        >
                          ×
                        </button>
                      )}
                    </div>
                  </div>
                )
              })}

              <div className={styles.uploadActionRow}>
                <button
                  type="button"
                  className={styles.uploadActionBtn}
                  disabled={isUploading}
                  onClick={handleStartUpload}
                >
                  {isUploading ? (
                    <>
                      <Spinner />
                      <span>Indexing documents…</span>
                    </>
                  ) : (
                    <span>Upload {selectedFiles.length} {selectedFiles.length === 1 ? 'file' : 'files'}</span>
                  )}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </motion.div>
    </div>
  )
}


function AlertIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}

function Spinner() {
  return (
    <svg className={styles.spinner} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
      <circle cx="12" cy="12" r="10" strokeOpacity="0.25" />
      <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round" />
    </svg>
  )
}
