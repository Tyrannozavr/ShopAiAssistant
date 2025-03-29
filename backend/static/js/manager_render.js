const BOT_NAME = "dmivbot"
Object.assign(render, {
  inviteRender: function render(data, type, full, meta, fieldOptions) {
    const inviteLink = `https://t.me/${BOT_NAME}?start=manager_${full.identifier}`;
    return `
      <div>
        <button 
          style="
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
          "
          onclick="
            const button = this;
            button.style.backgroundColor='#388E3C';
            button.innerText='Copied';
            navigator.clipboard.writeText('${inviteLink}');
            setTimeout(() => {
              button.style.backgroundColor='#4CAF50';
              button.innerText='Invite';
            }, 1000);
          "
        >
          Invite
        </button>
      </div>
    `;
  },
  cityInviteRender: function render(data, type, full, meta, fieldOptions) {
    const cityInviteLink = `https://t.me/${BOT_NAME}?start=utm_${full.name}`;
    return `
      <div>
        <button 
          style="
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
          "
          onclick="
            const button = this;
            button.style.backgroundColor='#388E3C';
            button.innerText='Copied';
            navigator.clipboard.writeText('${cityInviteLink}');
            setTimeout(() => {
              button.style.backgroundColor='#4CAF50';
              button.innerText='Invite';
            }, 1000);
          "
        >
          Invite
        </button>
      </div>
    `;
  },
});
