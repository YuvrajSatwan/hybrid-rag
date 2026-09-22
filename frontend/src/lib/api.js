/**
 * API client for HYBRID-RAG backend.
 *
 * Provides workspace document management, uploading, deleting, and grounded Q&A.
 */

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '')
const QUERY_TIMEOUT_MS = 60_000

/**
 * @typedef {Object} Citation
 * @property {string} chunk_id
 * @property {string} [title]
 * @property {string} [filename]
 * @property {number|null} [page]
 * @property {string|null} [section]
 * @property {string} snippet
 * @property {string} [source_url]
 */

/**
 * @typedef {Object} QueryResponse
 * @property {string} answer
 * @property {Citation[]} citations
 * @property {number} latency_ms
 * @property {string} [workspace_id]
 */

/**
 * Submit a query against the workspace documents.
 *
 * @param {string} query
 * @param {string} [workspaceId='default']
 * @param {number} [topK=10]
 * @param {string|null} [conversationId=null]
 * @param {AbortSignal} [signal]
 * @returns {Promise<QueryResponse>}
 */
export async function submitQuery(query, workspaceId = 'default', topK = 10, conversationId = null, signal = null) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), QUERY_TIMEOUT_MS)

  if (signal) {
    signal.addEventListener('abort', () => controller.abort())
  }

  let res
  try {
    res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        workspace_id: workspaceId,
        top_k: topK,
        conversation_id: conversationId,
      }),
      signal: controller.signal,
    })
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. The retrieval pipeline may be warming up — please try again.')
    }
    console.error('Query fetch failed:', err)
    throw new Error("Couldn't connect to HYBRID-RAG. Please ensure the server is running.")
  } finally {
    clearTimeout(timeoutId)
  }

  if (!res.ok) {
    let userMsg = 'Something went wrong while processing your question.'
    try {
      const body = await res.json()
      if (res.status === 404) {
        userMsg = body.detail || 'Workspace has expired or was not found.'
      } else if (res.status === 400 && body.detail) {
        userMsg = body.detail
      } else if (res.status >= 500) {
        console.error('Server error response:', body)
        userMsg = 'Something went wrong while processing your question.'
      } else if (body.detail) {
        userMsg = body.detail
      }
    } catch {
      // JSON parse error
    }
    const err = new Error(userMsg)
    err.status = res.status
    throw err
  }

  const data = await res.json()

  if (!data.answer && !data.citations?.length) {
    throw new Error('No answer could be generated from the selected documents.')
  }

  return data
}

/**
 * Initialize a new temporary workspace.
 *
 * @param {string} [name='My Documents']
 */
export async function createWorkspace(name = 'My Documents') {
  const res = await fetch(`${API_BASE}/api/workspaces`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  })
  if (!res.ok) throw new Error('Failed to initialize session workspace')
  return res.json()
}

/**
 * Fetch the active workspace with its document list.
 *
 * @param {string} [workspaceId='default']
 */
export async function fetchWorkspace(workspaceId = 'default') {
  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}`)
  if (!res.ok) {
    const err = new Error(res.status === 404 ? 'Workspace not found or expired' : 'Failed to fetch workspace')
    err.status = res.status
    throw err
  }
  return res.json()
}

/**
 * Delete a workspace and all its indexed session data.
 *
 * @param {string} workspaceId
 */
export async function deleteWorkspace(workspaceId) {
  if (!workspaceId) return null
  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}`, {
    method: 'DELETE',
  })
  if (!res.ok && res.status !== 404) {
    throw new Error('Failed to delete workspace')
  }
  return res.ok ? res.json() : null
}

/**
 * Upload one or more files to a workspace.
 * Supported: PDF, Markdown (.md), TXT, HTML.
 *
 * @param {string} [workspaceId='default']
 * @param {File[]} files
 */
export async function uploadDocuments(workspaceId = 'default', files) {
  const formData = new FormData()
  for (const f of files) {
    formData.append('files', f)
  }

  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/documents/upload`, {
    method: 'POST',
    body: formData,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const errorObj = new Error(err.detail || `Upload failed (HTTP ${res.status})`)
    errorObj.status = res.status
    throw errorObj
  }

  return res.json()
}

/**
 * Delete a document from a workspace.
 *
 * @param {string} [workspaceId='default']
 * @param {string} documentId
 */
export async function deleteDocument(workspaceId = 'default', documentId) {
  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/documents/${documentId}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete document')
  return res.json()
}

/**
 * Fetch messages for a conversation session.
 *
 * @param {string} [workspaceId='default']
 * @param {string} conversationId
 */
export async function fetchConversation(workspaceId = 'default', conversationId = 'default') {
  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/conversations/${conversationId}`)
  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error('Failed to load conversation')
  }
  return res.json()
}

/**
 * Delete a conversation session.
 *
 * @param {string} [workspaceId='default']
 * @param {string} conversationId
 */
export async function deleteConversation(workspaceId = 'default', conversationId = 'default') {
  const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/conversations/${conversationId}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete conversation')
  return res.json()
}

// Backward compatibility helpers
export const fetchCollections = () => fetch(`${API_BASE}/api/workspaces`).then(r => r.json())
export const fetchCollection = (id) => fetchWorkspace(id)


