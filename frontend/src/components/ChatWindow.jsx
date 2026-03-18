import { useMemo } from 'react';
import { Virtuoso } from 'react-virtuoso';
import MessageBubble from './MessageBubble';

function dayLabel(timestamp) {
  const dt = new Date(timestamp);
  return dt.toLocaleDateString([], { day: '2-digit', month: 'short', year: 'numeric' });
}

function ChatWindow({ messages, search, myUserId, loading, loadingMore }) {
  const normalizedSearch = search.trim().toLowerCase();

  const filtered = useMemo(() => {
    if (!normalizedSearch) {
      return messages;
    }

    return messages.filter((m) => {
      const text = (m.message || '').toLowerCase();
      const sender = (m.sender_name || '').toLowerCase();
      return text.includes(normalizedSearch) || sender.includes(normalizedSearch);
    });
  }, [messages, normalizedSearch]);

  return (
    <section className="chat-window">
      <div className="chat-header">
        {loading ? 'Conversation (loading...)' : `Conversation (${filtered.length} messages)`}
      </div>
      <div className="chat-performance-hint">
        {loading
          ? 'Preparing first messages...'
          : `Showing ${filtered.length} messages${loadingMore ? ' (loading more...)' : ''}.`}
      </div>
      <div className="chat-messages">
        {loading ? (
          <div className="empty-state">Loading messages...</div>
        ) : filtered.length === 0 ? (
          <div className="empty-state">No messages to display</div>
        ) : (
          <Virtuoso
            className="chat-virtuoso"
            data={filtered}
            followOutput={false}
            increaseViewportBy={{ top: 300, bottom: 500 }}
            itemContent={(index, item) => {
              const previous = index > 0 ? filtered[index - 1] : null;
              const currentDay = dayLabel(item.timestamp);
              const previousDay = previous ? dayLabel(previous.timestamp) : null;
              const needsDayDivider = index === 0 || currentDay !== previousDay;

              return (
              <div>
                {needsDayDivider && <div className="date-divider">{currentDay}</div>}
                <MessageBubble
                  msg={item}
                  search={search}
                  isMine={item.sender_id != null && myUserId != null && item.sender_id === myUserId}
                  showSenderName
                />
              </div>
            );
            }}
          />
        )}
      </div>
    </section>
  );
}

export default ChatWindow;
