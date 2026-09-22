import { useRef, useEffect } from 'react'
import MessageItem from './MessageItem'
import QuestionComposer from './QuestionComposer'
import styles from './ConversationArea.module.css'

const EXAMPLE_PROMPTS = [
  'Summarize this document',
  'What are the key technologies and takeaways?',
  'What are the main conclusions?',
  'Extract all action items and timelines',
]

export default function ConversationArea({
  messages = [],
  query,
  onQueryChange,
  onSubmitQuery,
  isLoading = false,
  onRetryMessage,
  onNewConversation,
}) {
  const scrollBottomRef = useRef(null)
  const isThreadEmpty = messages.length === 0

  // Scroll to bottom when new messages arrive or loading state changes
  useEffect(() => {
    scrollBottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSelectExample = (promptText) => {
    onQueryChange(promptText)
    onSubmitQuery(promptText)
  }

  return (
    <section className={styles.container}>
      {/* Thread Header Toolbar when conversation is active */}
      {!isThreadEmpty && onNewConversation && (
        <div className={styles.topBar}>
          <span className={styles.threadMeta}>
            {messages.filter((m) => m.role === 'user').length} questions in this session
          </span>
          <button
            type="button"
            className={styles.newChatBtn}
            onClick={onNewConversation}
            title="Start a new conversation thread"
          >
            <NewChatIcon />
            <span>New conversation</span>
          </button>
        </div>
      )}

      {/* Scrollable conversation messages stream */}
      <div className={styles.scrollArea}>
        <div className={styles.feedWrapper}>
          {isThreadEmpty ? (
            /* Tasteful empty conversation state */
            <div className={styles.emptyConversation}>
              <div className={styles.emptyContent}>
                <h2 className={styles.emptyTitle}>Ask your documents</h2>
                <p className={styles.emptySubtitle}>
                  Get answers grounded in the documents you&apos;ve uploaded.
                </p>

                <div className={styles.suggestionsGrid}>
                  {EXAMPLE_PROMPTS.map((prompt, i) => (
                    <button
                      key={i}
                      type="button"
                      className={styles.suggestionBtn}
                      onClick={() => handleSelectExample(prompt)}
                    >
                      <span className={styles.suggestionText}>{prompt}</span>
                      <ArrowRightIcon />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            /* Message Thread */
            <div className={styles.messageList} role="log" aria-live="polite">
              {messages.map((msg) => (
                <MessageItem
                  key={msg.id}
                  message={msg}
                  onRetry={onRetryMessage}
                />
              ))}

              {/* Understated loading state */}
              {isLoading && (
                <div className={styles.loadingRow}>
                  <div className={styles.loadingCard}>
                    <span className={styles.loadingPulse} />
                    <span className={styles.loadingText}>
                      Searching documents and synthesizing answer…
                    </span>
                  </div>
                </div>
              )}

              <div ref={scrollBottomRef} className={styles.anchor} />
            </div>
          )}
        </div>
      </div>

      {/* Anchored ChatGPT-Style Question Composer */}
      <div className={styles.composerWrapper}>
        <QuestionComposer
          value={query}
          onChange={onQueryChange}
          onSubmit={onSubmitQuery}
          isLoading={isLoading}
          autoFocus={true}
        />
      </div>
    </section>
  )
}

function ArrowRightIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  )
}

function NewChatIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
    </svg>
  )
}
