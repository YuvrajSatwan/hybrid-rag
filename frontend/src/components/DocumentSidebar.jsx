import { useState, useRef } from 'react'
import DocumentItem from './DocumentItem'
import styles from './DocumentSidebar.module.css'

export default function DocumentSidebar({
  documents = [],
  onDeleteDocument,
  onUploadFiles,
  onRetryDocument,
  isOpen = false,
  onClose,
  selectedDocId,
  onSelectDoc,
}) {
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
    if (e.dataTransfer?.files?.length) {
      onUploadFiles(e.dataTransfer.files)
    }
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const handleInputChange = (e) => {
    if (e.target.files?.length) {
      onUploadFiles(e.target.files)
      e.target.value = ''
    }
  }

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className={styles.mobileBackdrop}
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`${styles.sidebar} ${isOpen ? styles.sidebarOpen : ''} ${
          dragOver ? styles.sidebarDragOver : ''
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.md,.txt,.html"
          style={{ display: 'none' }}
          onChange={handleInputChange}
          aria-label="Upload documents"
        />

        {/* Sidebar Header */}
        <div className={styles.header}>
          <div className={styles.headerLeft}>
            <span className={styles.title}>DOCUMENTS</span>
            <span className={styles.countBadge}>{documents.length}</span>
          </div>

          <button
            type="button"
            className={styles.addBtn}
            onClick={handleBrowseClick}
            title="Add documents"
          >
            <PlusIcon />
            <span>Add</span>
          </button>
        </div>

        {/* Drag drop hint banner when drag over */}
        {dragOver && (
          <div className={styles.dropOverlay}>
            <UploadIcon />
            <span>Drop files to add</span>
          </div>
        )}

        {/* Document List */}
        <div className={styles.docList} role="list">
          {documents.map((doc) => (
            <DocumentItem
              key={doc.document_id || doc.filename}
              doc={doc}
              isSelected={selectedDocId === doc.document_id}
              onSelect={() => onSelectDoc?.(doc.document_id)}
              onDelete={() => onDeleteDocument(doc)}
              onRetry={onRetryDocument}
            />
          ))}
        </div>

        {/* Quick add prompt at sidebar bottom */}
        <div className={styles.footer}>
          <button
            type="button"
            className={styles.footerAddBtn}
            onClick={handleBrowseClick}
          >
            <PlusIcon />
            <span>Add documents</span>
          </button>
          <span className={styles.formatHint}>PDF · Markdown · TXT · HTML</span>
        </div>
      </aside>
    </>
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

function UploadIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
  )
}
