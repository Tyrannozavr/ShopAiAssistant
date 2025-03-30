const BOT_NAME = "dmivbot"
Object.assign(render, {
  inviteRender: function render(data, type, full) {
    const inviteLink = `https://t.me/${BOT_NAME}?start=manager_${full.identifier}`;
    return `
      <div>
        <button 
          style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;"
          onclick="copyToClipboard(this, '${inviteLink}')"
        >
          Invite
        </button>
      </div>
    `;
  },
  cityInviteRender: function render(data, type, full) {
    const cityInviteLink = `https://t.me/${BOT_NAME}?start=utm_${full.name}`;
    return `
      <div>
        <button 
          style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;"
          onclick="copyToClipboard(this, '${cityInviteLink}')"
        >
          Invite
        </button>
      </div>
    `;
  },
});

// Добавьте этот скрипт в ваш HTML (лучше в head или перед закрывающим тегом body)
function copyToClipboard(button, text) {
  // Сохраняем оригинальный текст и цвет
  const originalText = button.innerText;
  const originalColor = button.style.backgroundColor;

  // Меняем вид кнопки
  button.style.backgroundColor = '#388E3C';
  button.innerText = 'Copied';

  // Пробуем разные методы копирования
  try {
    // Метод 1: Modern Clipboard API (работает только на HTTPS/localhost)
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).catch(() => {
        fallbackCopy(text);
      });
    }
    // Метод 2: Старый метод document.execCommand
    else {
      fallbackCopy(text);
    }
  } catch (e) {
    console.error('Copy failed:', e);
    // Метод 3: Показываем текст для ручного копирования
    prompt('Copy this link:', text);
  }

  // Возвращаем оригинальный вид через 1 секунду
  setTimeout(() => {
    button.style.backgroundColor = originalColor;
    button.innerText = originalText;
  }, 1000);
}

// Старый метод копирования
function fallbackCopy(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';  // Prevent scrolling to bottom
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand('copy');
  } catch (err) {
    console.error('Fallback copy failed:', err);
    // В крайнем случае показываем prompt
    prompt('Copy this link:', text);
  }

  document.body.removeChild(textarea);
}
