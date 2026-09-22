import { useState, useRef, useCallback } from 'react'
import styles from './EmptyWorkspace.module.css'

const ALLOWED_EXTS = ['.pdf', '.md', '.txt', '.html']
const MAX_FILE_SIZE = 20 * 1024 * 1024 // 20 MB

export default function EmptyWorkspace({
  onUploadFiles,
  isUploading = false,
}) {
  const [dragOver, setDragOver] = useState(false)
  const [rejections, setRejections] = useState([])
  const fileInputRef = useRef(null)

  const handleFilesAdded = useCallback((filesList) => {
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
          reason: 'File exceeds maximum size of 20 MB.',
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
      onUploadFiles(newlyValid).catch((err) => {
        setRejections([
          {
            name: 'Upload error',
            reason: err.message || 'Failed to upload documents.',
          },
        ])
      })
    }
  }, [onUploadFiles])

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
    if (e.dataTransfer?.files?.length) {
      handleFilesAdded(e.dataTransfer.files)
    }
  }, [handleFilesAdded])

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const handleInputChange = (e) => {
    if (e.target.files?.length) {
      handleFilesAdded(e.target.files)
      e.target.value = ''
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.workspaceCard}>
        {/* Workspace Title & Intro */}
        <div className={styles.header}>
          <h1 className={styles.title}>Your documents</h1>
          <p className={styles.subtitle}>
            Upload documents and ask questions about them.
          </p>
        </div>

        {/* Hidden file picker */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.md,.txt,.html"
          style={{ display: 'none' }}
          onChange={handleInputChange}
          aria-label="Upload documents"
        />

        {/* Polished Upload Box */}
        <div
          className={`${styles.dropzone} ${dragOver ? styles.dropzoneActive : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
          role="button"
          tabIndex={0}
          aria-label="Upload files dropzone. Press Enter to browse."
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              handleBrowseClick()
            }
          }}
        >
          <div className={styles.dropInner}>
            <div className={styles.uploadIconWrap}>
              <UploadDocumentIcon />
            </div>

            <div className={styles.textGroup}>
              <h2 className={styles.dropHeading}>
                {dragOver ? 'Drop files to upload' : 'Upload your documents'}
              </h2>
              <p className={styles.dropSub}>
                Drop files here or browse files
              </p>
            </div>

            <button
              type="button"
              className={styles.browseBtn}
              onClick={(e) => {
                e.stopPropagation()
                handleBrowseClick()
              }}
              disabled={isUploading}
            >
              <PlusIcon />
              <span>{isUploading ? 'Uploading…' : 'Add documents'}</span>
            </button>

            <div className={styles.formatMeta}>
              <span>PDF · Markdown · TXT · HTML</span>
              <span className={styles.metaDot}>·</span>
              <span>Max 20 MB</span>
            </div>
          </div>
        </div>

        {/* Rejection / Validation Banners */}
        {rejections.length > 0 && (
          <div className={styles.rejectionsList}>
            {rejections.map((rej, i) => (
              <div key={i} className={styles.rejectionItem}>
                <AlertIcon />
                <div className={styles.rejectionText}>
                  <strong>{rej.name}:</strong> {rej.reason}
                </div>
                <button
                  type="button"
                  className={styles.dismissBtn}
                  onClick={() => setRejections((prev) => prev.filter((_, idx) => idx !== i))}
                  aria-label="Dismiss error"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function UploadDocumentIcon() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="12" y1="18" x2="12" y2="12" />
      <polyline points="9 15 12 12 15 15" />
    </svg>
  )
}

function PlusIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
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
