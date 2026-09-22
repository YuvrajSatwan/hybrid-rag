import styles from './Header.module.css'

export default function Header({
  theme,
  onToggleTheme,
  documentCount = 0,
  onUploadClick,
  onToggleSidebar,
  isSidebarOpen = false,
  onNewSession,
}) {
  return (
    <header className={styles.header}>
      {/* Brand area */}
      <div className={styles.brand}>
        {/* Mobile menu button */}
        {documentCount > 0 && (
          <button
            type="button"
            className={`${styles.mobileMenuBtn} ${isSidebarOpen ? styles.mobileMenuBtnActive : ''}`}
            onClick={onToggleSidebar}
            aria-label={isSidebarOpen ? 'Close document sidebar' : 'Open document sidebar'}
            title="Documents"
          >
            <SidebarToggleIcon />
          </button>
        )}

        <div className={styles.wordmarkGroup}>
          <span className={styles.title}>HYBRID-RAG</span>
          <span className={styles.divider}>/</span>
          <span className={styles.subtitle}>Document Assistant</span>
        </div>
      </div>

      {/* Right action area */}
      <div className={styles.actions}>
        {documentCount > 0 && (
          <button
            type="button"
            className={styles.docCountBadge}
            onClick={onToggleSidebar}
            title={`${documentCount} ${documentCount === 1 ? 'document' : 'documents'} in workspace`}
          >
            <DocumentIcon />
            <span className={styles.docCountText}>
              {documentCount} {documentCount === 1 ? 'document' : 'documents'}
            </span>
          </button>
        )}

        {onUploadClick && (
          <button
            type="button"
            className={styles.uploadBtn}
            onClick={onUploadClick}
            title="Upload new documents"
          >
            <PlusIcon />
            <span>Upload</span>
          </button>
        )}

        {onNewSession && (
          <button
            type="button"
            className={styles.newSessionBtn}
            onClick={onNewSession}
            title="Clear session documents and start fresh"
          >
            <RefreshIcon />
            <span>New Session</span>
          </button>
        )}

        <button
          type="button"
          className={styles.themeToggle}
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
        </button>
      </div>
    </header>
  )
}

function SidebarToggleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="9" y1="3" x2="9" y2="21" />
    </svg>
  )
}

function DocumentIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  )
}

function PlusIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  )
}

function SunIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  )
}

function MoonIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  )
}

function RefreshIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67" />
    </svg>
  )
}
