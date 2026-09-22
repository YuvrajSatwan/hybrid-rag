import { useRef, useEffect, useCallback } from 'react'
import styles from './QueryInput.module.css'

export default function QueryInput({
  value,
  onChange,
  onSubmit,
  isLoading = false,
  autoFocus = false,
}) {
  const textareaRef = useRef(null)

  // Auto-resize textarea according to scrollHeight
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 260) + 'px'
  }, [value])

  // Focus on mount when requested
  useEffect(() => {
    if (autoFocus && textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [autoFocus])

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        if (!isLoading && value.trim().length > 0) {
          onSubmit()
        }
      }
    },
    [isLoading, value, onSubmit]
  )

  const canSubmit = !isLoading && value.trim().length > 0
  const placeholder = 'Message Hybrid-RAG...'

  return (
    <div className={`${styles.wrapper} ${isLoading ? styles.wrapperLoading : ''}`}>
      <textarea
        ref={textareaRef}
        className={styles.textarea}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        rows={1}
        disabled={isLoading}
        aria-label="Ask question about documents"
        spellCheck={true}
      />

      <div className={styles.footer}>
        <div className={styles.hintWrap}>
          <span className={styles.hint}>
            {isLoading ? 'Processing…' : 'Enter to send · Shift+Enter for newline'}
          </span>
        </div>

        <button
          type="button"
          className={styles.sendBtn}
          onClick={() => {
            if (canSubmit) onSubmit()
          }}
          disabled={!canSubmit}
          aria-label={isLoading ? 'Searching documents' : 'Submit question'}
        >
          {isLoading ? (
            <Spinner />
          ) : (
            <SendUpIcon />
          )}
        </button>
      </div>
    </div>
  )
}

function SendUpIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="19" x2="12" y2="5" />
      <polyline points="5 12 12 5 19 12" />
    </svg>
  )
}

function Spinner() {
  return (
    <svg className={styles.spinner} width="14" height="14" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.5">
      <circle cx="12" cy="12" r="10" strokeOpacity="0.25" />
      <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round" />
    </svg>
  )
}
