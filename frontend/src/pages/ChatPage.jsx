import { useEffect, useMemo, useState } from 'react';
import AnalyticsPanel from '../components/AnalyticsPanel';
import ChatWindow from '../components/ChatWindow';
import SearchBar from '../components/SearchBar';
import Sidebar from '../components/Sidebar';
import UploadPanel from '../components/UploadPanel';
import {
  exportJson,
  fetchAnalytics,
  fetchMessages,
  fetchSentiment,
  fetchSummary,
  fetchUsers,
} from '../services/api';

const PAGE_SIZE = 5000;

function inferMyUserId(users, messages) {
  const explicitYou = users.find((u) => u.name?.trim().toLowerCase() === 'you');
  if (explicitYou) {
    return explicitYou.id;
  }

  const counts = new Map();
  messages.forEach((m) => {
    if (m.sender_id == null) return;
    counts.set(m.sender_id, (counts.get(m.sender_id) || 0) + 1);
  });

  if (counts.size > 0) {
    let maxId = null;
    let maxCount = -1;
    counts.forEach((count, senderId) => {
      if (count > maxCount) {
        maxCount = count;
        maxId = senderId;
      }
    });
    return maxId;
  }

  return users.length ? users[0].id : null;
}

function ChatPage() {
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [search, setSearch] = useState('');
  const [myUserId, setMyUserId] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [summary, setSummary] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [backendError, setBackendError] = useState('');
  const [loading, setLoading] = useState(false);
  const [totalMessages, setTotalMessages] = useState(0);

  const fetchAllMessages = async (searchTerm = '') => {
    let offset = 0;
    let total = 0;
    const allRows = [];

    do {
      const page = await fetchMessages(searchTerm, PAGE_SIZE, offset);
      const chunk = page.messages || [];
      total = page.total || 0;
      allRows.push(...chunk);
      offset += chunk.length;

      if (chunk.length === 0) {
        break;
      }
    } while (offset < total);

    return { messages: allRows, total };
  };

  const loadAll = async () => {
    setLoading(true);
    try {
      const [u, a, s, t, all] = await Promise.all([
        fetchUsers(),
        fetchAnalytics(),
        fetchSummary(),
        fetchSentiment(),
        fetchAllMessages(''),
      ]);

      setUsers(u);
      setMessages(all.messages || []);
      setTotalMessages(all.total || 0);
      setAnalytics(a);
      setSummary(s.summary);
      setSentiment(t);
      setMyUserId((prev) => {
        if (prev && u.some((item) => item.id === prev)) {
          return prev;
        }
        return inferMyUserId(u, all.messages || []);
      });
      setBackendError('');
    } catch (error) {
      setBackendError('Backend is unreachable. Start Flask on port 5000 and check database configuration.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const selectedName = useMemo(() => 'WhatsApp Conversation', []);

  const showMySelector = users.length > 1;

  const handleExport = async () => {
    try {
      const data = await exportJson();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'parsed-chat.json';
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      setBackendError('Export failed. Make sure backend is running.');
    }
  };

  return (
    <main className="app-shell">
      <div className="top-glow" />

      <section className="left-column">
        <UploadPanel onUploaded={loadAll} />
        <Sidebar users={users} messages={messages} myUserId={myUserId} onSetMyUserId={setMyUserId} />
      </section>

      <section className="center-column">
        <header className="conversation-title">
          <span>{selectedName}</span>
          {showMySelector && (
            <label className="identity-picker">
              You:
              <select
                value={myUserId || ''}
                onChange={(e) => setMyUserId(Number(e.target.value))}
              >
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.name}
                  </option>
                ))}
              </select>
            </label>
          )}
        </header>
        {backendError && <div className="error-banner">{backendError}</div>}
        <SearchBar value={search} onChange={setSearch} />
        <ChatWindow
          messages={messages}
          search={search}
          myUserId={myUserId}
          loading={loading}
        />
        <div className="pagination-info">Loaded {messages.length} messages of {totalMessages}</div>
      </section>

      <section className="right-column">
        <AnalyticsPanel
          analytics={analytics}
          summary={summary}
          sentiment={sentiment}
          onExport={handleExport}
        />
      </section>
    </main>
  );
}

export default ChatPage;
