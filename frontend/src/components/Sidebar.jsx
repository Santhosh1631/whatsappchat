import { useMemo } from 'react';

function Sidebar({ users, messages, myUserId }) {
  const messageCountByUser = useMemo(() => {
    const counts = {};
    users.forEach((u) => {
      counts[u.id] = 0;
    });

    messages.forEach((m) => {
      if (m.sender_id != null && Object.prototype.hasOwnProperty.call(counts, m.sender_id)) {
        counts[m.sender_id] += 1;
      }
    });

    return counts;
  }, [users, messages]);

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Participants</h2>
      </div>
      <div className="search-box">
        <input type="text" placeholder="Single imported conversation" readOnly />
      </div>
      <div className="chat-list">
        <div className="chat-item active">
          <div className="chat-avatar all">💬</div>
          <div className="chat-info">
            <div className="chat-name">Imported Chat</div>
            <div className="chat-preview">{messages.length} total messages</div>
          </div>
        </div>
        {users.map((user) => (
          <div key={user.id} className="chat-item">
            <div className="chat-avatar">{user.name.charAt(0).toUpperCase()}</div>
            <div className="chat-info">
              <div className="chat-name">
                {user.name}
                {myUserId === user.id && <span className="you-tag">YOU</span>}
              </div>
              <div className="chat-preview">{messageCountByUser[user.id] || 0} messages</div>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;
