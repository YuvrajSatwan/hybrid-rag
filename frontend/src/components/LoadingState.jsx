import { motion } from 'framer-motion'
import styles from './LoadingState.module.css'

export default function LoadingState() {
  return (
    <motion.div
      className={styles.root}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      role="status"
      aria-live="polite"
    >
      <div className={styles.label}>
        <span className={styles.pulseDot} aria-hidden="true" />
        <span className={styles.stageText}>Searching your documents…</span>
      </div>
      <div className={styles.bar} aria-hidden="true">
        <div className={styles.barFill} />
      </div>
    </motion.div>
  )
}
