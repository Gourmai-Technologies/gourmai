// Function to check if an element is in the viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;

    // Check if the bottom of the element is within the viewport or if the element's height equals the viewport height
    return (
        (rect.top >= 0 && rect.bottom <= windowHeight) ||
        (rect.top <= 0 && rect.bottom >= windowHeight)
    );
}


  
  // Function to handle the scroll event
  function handleScroll() {
    const boxes = document.querySelectorAll('.blur-box');
    
    boxes.forEach(box => {
      if (isInViewport(box)) {
        box.classList.remove('blur-feature-section-background');
        box.classList.add('no-blur-feature-section-background');
      } else {
        box.classList.add('blur-feature-section-background');
        box.classList.remove('no-blur-feature-section-background');
    }
    });
  }
  
  // Add scroll event listener
  window.addEventListener('scroll', handleScroll);
  
  // Initial check on page load
  handleScroll();








// Function to handle the intersection
function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target); // Stop observing once animation is triggered
        } else {
            entry.target.classList.remove('fade-in'); // Remove fade-in class when not intersecting
        }
    });
}

// Create a new intersection observer
const observer = new IntersectionObserver(handleIntersection, {
    root: null, // Use the viewport as the root
    threshold: 1 // Trigger when 50% of the element is in view
});

// Select the elements to animate
const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');

// Observe each element
elementsToAnimate.forEach(element => {
    observer.observe(element);
});
  