document.querySelector('.animated-button').addEventListener('mouseenter', function() {
    this.classList.add('hovered');
  });
  
  document.querySelector('.animated-button').addEventListener('mouseleave', function() {
    this.classList.remove('hovered');
  });
  