import { useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import styles from './DeleteConfirmModal.module.css'

export default function DeleteConfirmModal({
  isOpen,
  doc,
  onConfirm,
  onCancel,
  isDeleting = false,
}) {
  const cancelBtnRef = useRef(null)

  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && !isDeleting) {
        onCancel()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onCancel, isDeleting])

  useEffect(() => {
    if (isOpen && cancelBtnRef.current) {
      cancelBtnRef.current.focus()
    }
  }, [isOpen])

  if (!isOpen || !doc) return null

  return (
    <AnimatePresence>
      <div
        className={styles.backdrop}
        onClick={() => !isDeleting && onCancel()}
        role="presentation"
      >
        <motion.div
          className={styles.dialog}
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-dialog-title"
          onClick={(e) => e.stopPropagation()}
          initial={{ opacity: 0, scale: 0.96, y: 8 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.96, y: 8 }}
          transition={{ duration: 0.16, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className={styles.header}>
            <h3 id="delete-dialog-title" className={styles.title}>
              Delete document?
            </h3>
          </div>

          <p className={styles.description}>
            Are you sure you want to delete <strong className={styles.docName}>{doc.filename}</strong>? Its indexed chunks and embeddings will be permanently removed from this workspace.
          </p>

          <div className={styles.actions}>
            <button
              ref={cancelBtnRef}
              type="button"
              className={styles.cancelBtn}
              onClick={onCancel}
              disabled={isDeleting}
            >
              Cancel
            </button>
            <button
              type="button"
              className={styles.confirmBtn}
              onClick={onConfirm}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deleting…' : 'Delete'}
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}
