import { useRef, useEffect, useCallback } from 'react'
import styles from './QuestionComposer.module.css'

export default function QuestionComposer({
  value,
  onChange,
  onSubmit,
  isLoading = false,
  autoFocus = true,
  placeholder = 'Ask anything about your documents…',
}) {
  const textareaRef = useRef(null)

  // Auto-resize textarea height
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    const newHeight = Math.min(Math.max(el.scrollHeight, 44), 180)
    el.style.height = `${newHeight}px`
  }, [value])

  // Auto-focus on mount
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

  return (
    <div className={styles.composerContainer}>
      <div className={`${styles.box} ${isLoading ? styles.boxLoading : ''}`}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          rows={1}
          disabled={isLoading}
          aria-label="Ask a question about your documents"
          spellCheck={true}
        />

        <div className={styles.controls}>
          <button
            type="button"
            className={`${styles.sendBtn} ${canSubmit ? styles.sendBtnActive : ''}`}
            onClick={() => {
              if (canSubmit) onSubmit()
            }}
            disabled={!canSubmit}
            aria-label={isLoading ? 'Retrieving answer' : 'Send message'}
            title={canSubmit ? 'Send message (Enter)' : 'Enter a question to send'}
          >
            {isLoading ? <Spinner /> : <ArrowUpIcon />}
          </button>
        </div>
      </div>

      <div className={styles.hintWrap}>
        <span className={styles.hintText}>
          Enter to send · Shift+Enter for newline
        </span>
      </div>
    </div>
  )
}

function ArrowUpIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="19" x2="12" y2="5" />
      <polyline points="5 12 12 5 19 12" />
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
