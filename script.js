// Navigation Toggle with Enhanced Animation
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('nav ul');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            
            // Animate hamburger menu
            const spans = navToggle.querySelectorAll('span');
            if (navToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translateY(10px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translateY(-10px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when a link is clicked
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }

    // Set active link based on current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
});

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc2626';
            isValid = false;
        } else {
            input.style.borderColor = '#ddd';
        }
    });

    return isValid;
}

// Form Submission Handler
function handleFormSubmit(event, formId) {
    event.preventDefault();
    
    if (validateForm(formId)) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        
        // Collect form data
        const data = Object.fromEntries(formData);
        console.log('Form submitted:', data);
        
        // Show success message
        alert('Thank you for your submission! We will contact you soon.');
        form.reset();
    } else {
        alert('Please fill in all required fields.');
    }
}

// Smooth Scroll for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Animate Elements on Scroll
function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    const elements = document.querySelectorAll('.card-3d, .featured-card, .showcase-card, .selection-item, .stat-card');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(element);
    });
}

window.addEventListener('load', observeElements);

// Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.floor(target) + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Initialize Counters
function initCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const text = entry.target.textContent;
                const target = parseInt(text.replace(/[^0-9]/g, ''));
                if (!isNaN(target)) {
                    animateCounter(entry.target, target);
                }
                observer.unobserve(entry.target);
            }
        });
    });
    statNumbers.forEach(stat => observer.observe(stat));
}

window.addEventListener('load', initCounters);

// Parallax Effect for Hero Section
document.addEventListener('mousemove', function(e) {
    const cards = document.querySelectorAll('.image-card');
    if (cards.length === 0) return;
    
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    cards.forEach(card => {
        const offset = 30;
        const x = (mouseX - 0.5) * offset;
        const y = (mouseY - 0.5) * offset;
        
        card.style.transform = `perspective(1000px) rotateY(${x}deg) rotateX(${-y}deg) translateZ(50px)`;
    });
});

// Create floating stars/particles effect
function createStars() {
    const starsContainer = document.querySelector('.stars');
    if (!starsContainer) return;
    
    for (let i = 0; i < 50; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.position = 'absolute';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.background = 'rgba(255, 255, 255, ' + (Math.random() * 0.5 + 0.3) + ')';
        star.style.borderRadius = '50%';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animation = `float ${Math.random() * 3 + 3}s infinite`;
        starsContainer.appendChild(star);
    }
}

window.addEventListener('load', createStars);

// Scroll Velocity Effect on Navigation
let lastScrollY = 0;
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (!header) return;
    
    const currentScrollY = window.scrollY;
    
    if (currentScrollY > 100) {
        header.style.boxShadow = '0 15px 50px rgba(230, 57, 70, 0.2)';
    } else {
        header.style.boxShadow = '0 10px 40px rgba(230, 57, 70, 0.15)';
    }
    
    lastScrollY = currentScrollY;
});
