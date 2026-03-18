import { memo } from 'react';

function highlightText(text, query) {
  const safeText = String(text ?? '');
  if (!query) return safeText;

  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'ig');
  const parts = safeText.split(regex);

  return parts.map((part, idx) => {
    if (part.toLowerCase() === query.toLowerCase()) {
      return <mark key={idx}>{part}</mark>;
    }
    return <span key={idx}>{part}</span>;
  });
}

function MessageBubble({ msg, isMine, search, showSenderName = true }) {
  const isSystem = msg.type === 'system';
  const cls = `bubble ${isSystem ? 'system' : isMine ? 'mine' : 'theirs'} ${msg.type}`;
  const rowClass = isSystem ? 'center' : isMine ? 'right' : 'left';
  const timeText = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`bubble-row ${rowClass}`}>
      <div className={cls}>
        {showSenderName && msg.sender_name && !isSystem && <div className="sender-name">{msg.sender_name}</div>}
        <div className="message-text">{highlightText(msg.message, search)}</div>
        <div className="meta-row">
          <span>{timeText}</span>
          {msg.type !== 'text' && <span className="type-tag">{msg.type}</span>}
        </div>
      </div>
    </div>
  );
}

export default memo(MessageBubble);
