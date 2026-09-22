import { useState, useCallback, useEffect, useMemo, useRef } from 'react'
import Header from './components/Header'
import DocumentSidebar from './components/DocumentSidebar'
import ConversationArea from './components/ConversationArea'
import EmptyWorkspace from './components/EmptyWorkspace'
import DeleteConfirmModal from './components/DeleteConfirmModal'
import {
  submitQuery,
  fetchWorkspace,
  createWorkspace,
  deleteWorkspace,
  uploadDocuments,
  deleteDocument,
  fetchConversation,
} from './lib/api'

import styles from './App.module.css'

const STORAGE_WS_KEY = 'sr_session_workspace_id'
const STORAGE_CONV_KEY = 'sr_session_conversation_id'

function getInitialTheme() {
  try {
    const saved = localStorage.getItem('sr-theme')
    if (saved) return saved
  } catch {}
  return 'light'
}

export default function App() {
  // ─── Theme ──────────────────────────────────────────────────────────────────
  const [theme, setTheme] = useState(getInitialTheme)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    try {
      localStorage.setItem('sr-theme', theme)
    } catch {}
  }, [theme])

  const toggleTheme = () =>
    setTheme((t) => (t === 'dark' ? 'light' : 'dark'))

  // ─── Ephemeral Session & Workspace State ────────────────────────────────────
  const [workspaceId, setWorkspaceId] = useState(() => {
    try {
      return sessionStorage.getItem(STORAGE_WS_KEY) || null
    } catch {
      return null
    }
  })
  const [workspace, setWorkspace] = useState({ workspace_id: '', documents: [] })
  const [optimisticDocs, setOptimisticDocs] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [selectedDocId, setSelectedDocId] = useState(null)
  const [docToDelete, setDocToDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const headerFileInputRef = useRef(null)

  // ─── Conversation Area & Messages State ─────────────────────────────────────
  const [conversationId, setConversationId] = useState(() => {
    try {
      return sessionStorage.getItem(STORAGE_CONV_KEY) || null
    } catch {
      return null
    }
  })
  const [messages, setMessages] = useState([])
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Initialize or re-attach to session workspace
  const initWorkspace = useCallback(async (preferredId = null) => {
    let wsId = preferredId
    if (!wsId) {
      try {
        wsId = sessionStorage.getItem(STORAGE_WS_KEY)
      } catch {}
    }

    if (wsId) {
      try {
        const data = await fetchWorkspace(wsId)
        setWorkspaceId(wsId)
        setWorkspace(data)
        return wsId
      } catch (err) {
        console.warn('Workspace expired or not found, starting fresh session:', err)
        try {
          sessionStorage.removeItem(STORAGE_WS_KEY)
          sessionStorage.removeItem(STORAGE_CONV_KEY)
        } catch {}
      }
    }

    // Create a new temporary workspace
    try {
      const newWs = await createWorkspace('Session Workspace')
      setWorkspaceId(newWs.workspace_id)
      setWorkspace(newWs)
      setConversationId(null)
      setMessages([])
      try {
        sessionStorage.setItem(STORAGE_WS_KEY, newWs.workspace_id)
        sessionStorage.removeItem(STORAGE_CONV_KEY)
      } catch {}
      return newWs.workspace_id
    } catch (err) {
      console.error('Failed to create session workspace:', err)
      return null
    }
  }, [])

  // Mount effect: initialize workspace
  useEffect(() => {
    initWorkspace()
  }, [initWorkspace])

  const refreshWorkspace = useCallback(async () => {
    if (!workspaceId) return
    try {
      const data = await fetchWorkspace(workspaceId)
      setWorkspace(data)
      // Clear optimistic docs that are now indexed or in real list
      setOptimisticDocs((prev) => {
        const normalize = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '')
        const serverDocIds = new Set((data.documents || []).map((d) => d.document_id))
        const serverDocNames = new Set((data.documents || []).map((d) => normalize(d.filename)))
        return prev.filter((od) => {
          if (serverDocIds.has(od.document_id)) return false
          if (serverDocNames.has(normalize(od.filename))) return false
          return true
        })
      })
    } catch (err) {
      if (err.status === 404) {
        console.warn('Workspace expired during refresh, reinitializing…')
        await initWorkspace()
      } else {
        console.error('Failed to reload workspace:', err)
      }
    }
  }, [workspaceId, initWorkspace])

  // Merge server documents with any active optimistic uploads
  const allDocuments = useMemo(() => {
    const serverDocs = workspace?.documents || []
    return [...optimisticDocs, ...serverDocs]
  }, [optimisticDocs, workspace?.documents])

  // Poll workspace while any document is indexing or uploading
  useEffect(() => {
    const isAnyIndexing = allDocuments.some((d) => {
      const s = (d.status || '').toLowerCase()
      return s === 'indexing' || s === 'processing' || s === 'uploading'
    })
    if (!isAnyIndexing) return

    const timer = setInterval(() => {
      refreshWorkspace()
    }, 1500)

    return () => clearInterval(timer)
  }, [allDocuments, refreshWorkspace])

  // Load existing conversation on mount if available
  useEffect(() => {
    if (!workspaceId || !conversationId) return
    let ignore = false
    fetchConversation(workspaceId, conversationId)
      .then((data) => {
        if (!ignore && data?.messages?.length) {
          setMessages(data.messages)
        }
      })
      .catch((err) => console.debug('No prior conversation found:', err))
    return () => {
      ignore = true
    }
  }, [workspaceId, conversationId])

  // Explicit New Session Action: deletes temporary workspace on server and starts fresh
  const handleNewSession = useCallback(async () => {
    const currentWsId = workspaceId
    // 1. Tell backend to wipe all temporary files for this workspace
    if (currentWsId) {
      try {
        await deleteWorkspace(currentWsId)
      } catch (err) {
        console.warn('Failed to delete workspace on server:', err)
      }
    }

    // 2. Clear session storage
    try {
      sessionStorage.removeItem(STORAGE_WS_KEY)
      sessionStorage.removeItem(STORAGE_CONV_KEY)
    } catch {}

    // 3. Clear UI state
    setMessages([])
    setConversationId(null)
    setOptimisticDocs([])
    setSelectedDocId(null)
    setDocToDelete(null)

    // 4. Create fresh session workspace
    try {
      const newWs = await createWorkspace('Session Workspace')
      setWorkspaceId(newWs.workspace_id)
      setWorkspace(newWs)
      try {
        sessionStorage.setItem(STORAGE_WS_KEY, newWs.workspace_id)
      } catch {}
    } catch (err) {
      console.error('Failed to create fresh workspace:', err)
    }
  }, [workspaceId])

  // Upload handler with immediate presence
  const handleUploadFiles = async (filesList) => {
    const files = Array.from(filesList)
    if (!files.length) return

    let activeId = workspaceId
    if (!activeId) {
      activeId = await initWorkspace()
      if (!activeId) return
    }

    // Immediately show files in document list
    const tempDocs = files.map((f) => ({
      document_id: `temp-${Date.now()}-${f.name}`,
      filename: f.name,
      file_size: f.size,
      status: 'Uploading',
      progress: 50,
      file_ref: f,
    }))

    setOptimisticDocs((prev) => [...tempDocs, ...prev])
    setIsUploading(true)

    try {
      setTimeout(() => {
        setOptimisticDocs((prev) =>
          prev.map((od) =>
            tempDocs.some((td) => td.document_id === od.document_id)
              ? { ...od, status: 'Indexing', progress: 100 }
              : od
          )
        )
      }, 400)

      await uploadDocuments(activeId, files)
      setOptimisticDocs((prev) =>
        prev.filter((od) => !tempDocs.some((td) => td.document_id === od.document_id))
      )
      await refreshWorkspace()
    } catch (err) {
      if (err.status === 404) {
        console.warn('Workspace expired during upload, reinitializing…')
        await handleNewSession()
      } else {
        setOptimisticDocs((prev) =>
          prev.map((od) =>
            tempDocs.some((td) => td.document_id === od.document_id)
              ? { ...od, status: 'Failed', error: err.message }
              : od
          )
        )
      }
      throw err
    } finally {
      setIsUploading(false)
    }
  }

  // Retry document upload
  const handleRetryDocument = (doc) => {
    if (doc.file_ref) {
      handleUploadFiles([doc.file_ref])
    }
  }

  // Delete document
  const handleConfirmDelete = async () => {
    if (!docToDelete || isDeleting || !workspaceId) return
    setIsDeleting(true)
    try {
      if (docToDelete.document_id.startsWith('temp-')) {
        setOptimisticDocs((prev) =>
          prev.filter((d) => d.document_id !== docToDelete.document_id)
        )
      } else {
        await deleteDocument(workspaceId, docToDelete.document_id)
        await refreshWorkspace()
      }
      setDocToDelete(null)
    } catch (err) {
      console.error('Failed to delete document:', err)
    } finally {
      setIsDeleting(false)
    }
  }

  const handleNewConversation = useCallback(() => {
    setMessages([])
    setConversationId(null)
    try {
      sessionStorage.removeItem(STORAGE_CONV_KEY)
    } catch {}
  }, [])

  const handleSubmitQuery = useCallback(
    async (overrideQuery) => {
      const text = (overrideQuery ?? query).trim()
      if (!text || isLoading) return

      let activeWsId = workspaceId
      if (!activeWsId) {
        activeWsId = await initWorkspace()
        if (!activeWsId) return
      }

      const userMsgId = `user-${Date.now()}`
      const newMessages = [
        ...messages,
        {
          id: userMsgId,
          role: 'user',
          content: text,
        },
      ]

      setMessages(newMessages)
      setQuery('')
      setIsLoading(true)

      try {
        const res = await submitQuery(text, activeWsId, 10, conversationId)
        if (res.conversation_id && res.conversation_id !== conversationId) {
          setConversationId(res.conversation_id)
          try {
            sessionStorage.setItem(STORAGE_CONV_KEY, res.conversation_id)
          } catch {}
        }

        setMessages((prev) => [
          ...prev,
          {
            id: `assistant-${Date.now()}`,
            role: 'assistant',
            content: res.answer,
            citations: res.citations || [],
            latency_ms: res.latency_ms,
          },
        ])
      } catch (err) {
        if (err.status === 404) {
          setMessages((prev) => [
            ...prev,
            {
              id: `assistant-err-${Date.now()}`,
              role: 'assistant',
              content: 'Your temporary session has expired. A new session has been initialized. Please upload your documents again.',
              error: true,
              originalQuery: text,
            },
          ])
          await handleNewSession()
        } else {
          setMessages((prev) => [
            ...prev,
            {
              id: `assistant-err-${Date.now()}`,
              role: 'assistant',
              content: err.message || 'Something went wrong while processing your question.',
              error: true,
              originalQuery: text,
            },
          ])
        }
      } finally {
        setIsLoading(false)
      }
    },
    [query, isLoading, messages, workspaceId, conversationId, initWorkspace, handleNewSession]
  )

  const handleRetryMessage = useCallback(
    (msgId) => {
      const errIndex = messages.findIndex((m) => m.id === msgId)
      if (errIndex > 0) {
        const priorUserMsg = messages[errIndex - 1]
        if (priorUserMsg && priorUserMsg.role === 'user') {
          setMessages((prev) => prev.filter((m) => m.id !== msgId))
          handleSubmitQuery(priorUserMsg.content)
        }
      }
    },
    [messages, handleSubmitQuery]
  )

  const hasDocuments = allDocuments.length > 0

  return (
    <div className={styles.appShell}>
      {/* Top Application Chrome */}
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        documentCount={allDocuments.length}
        onUploadClick={hasDocuments ? () => headerFileInputRef.current?.click() : null}
        onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        isSidebarOpen={isSidebarOpen}
        onNewSession={handleNewSession}
      />

      {/* Hidden file input for Header upload button */}
      <input
        ref={headerFileInputRef}
        type="file"
        multiple
        accept=".pdf,.md,.txt,.html"
        style={{ display: 'none' }}
        onChange={(e) => {
          if (e.target.files?.length) {
            handleUploadFiles(e.target.files)
            e.target.value = ''
          }
        }}
        aria-label="Upload documents"
      />

      {/* Main Workspace Body */}
      <main className={styles.workspaceBody}>
        {!hasDocuments ? (
          /* Polished empty workspace when no documents exist yet */
          <EmptyWorkspace
            onUploadFiles={handleUploadFiles}
            isUploading={isUploading}
          />
        ) : (
          /* Two-region document workspace */
          <div className={styles.twoRegionLayout}>
            {/* Left: Document Context & File List */}
            <DocumentSidebar
              documents={allDocuments}
              selectedDocId={selectedDocId}
              onSelectDoc={setSelectedDocId}
              onDeleteDocument={(doc) => setDocToDelete(doc)}
              onRetryDocument={handleRetryDocument}
              onUploadFiles={handleUploadFiles}
              isOpen={isSidebarOpen}
              onClose={() => setIsSidebarOpen(false)}
            />

            {/* Right: Conversation & Question Interface */}
            <ConversationArea
              messages={messages}
              query={query}
              onQueryChange={setQuery}
              onSubmitQuery={handleSubmitQuery}
              isLoading={isLoading}
              onRetryMessage={handleRetryMessage}
              onNewConversation={handleNewConversation}
            />
          </div>
        )}
      </main>

      {/* Accessible Delete Confirmation Modal */}
      <DeleteConfirmModal
        isOpen={Boolean(docToDelete)}
        doc={docToDelete}
        onConfirm={handleConfirmDelete}
        onCancel={() => setDocToDelete(null)}
        isDeleting={isDeleting}
      />
    </div>
  )
}
