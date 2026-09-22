import { motion } from 'framer-motion'
import styles from './ErrorState.module.css'

export default function ErrorState({ message, onRetry }) {
  return (
    <motion.div
      className={styles.root}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      role="alert"
    >
      <div className={styles.iconBox} aria-hidden="true">
        <AlertIcon />
      </div>
      <div className={styles.body}>
        <p className={styles.message}>
          {message || 'Something went wrong while processing your question.'}
        </p>
        {onRetry && (
          <button type="button" className={styles.retryBtn} onClick={onRetry}>
            Try again
          </button>
        )}
      </div>
    </motion.div>
  )
}

function AlertIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}
