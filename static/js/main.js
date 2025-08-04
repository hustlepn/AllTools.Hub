// Runs when the page fully loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('AllToolsHub initialized'); 
  
  // Add site-wide JavaScript here
  // Example: Mobile menu toggle (if added later)
  document.querySelector('.mobile-menu-btn')?.addEventListener('click', () => {
    document.querySelector('nav').classList.toggle('open');
  });
});
