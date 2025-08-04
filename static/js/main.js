// Initialize tooltips and global event listeners
document.addEventListener('DOMContentLoaded', () => {
  console.log('AllToolsHub initialized');
  
  // Copy buttons functionality
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', () => {
      const text = button.getAttribute('data-copy');
      navigator.clipboard.writeText(text);
      button.textContent = 'Copied!';
      setTimeout(() => button.textContent = 'Copy', 2000);
    });
  });
});
