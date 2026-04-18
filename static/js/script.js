// ===================================
// Smooth Scrolling for Navigation Links
// ===================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===================================
// Mobile Menu Toggle
// ===================================
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// ===================================
// Navbar Scroll Effect
// ===================================
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
    }
    
    lastScroll = currentScroll;
});

// ===================================
// Form Submission Handler
// ===================================
// Form handling is done entirely in form-handler.js
// Do NOT add another submit listener here — it causes conflicts.

// ===================================
// Scroll Animation Observer
// ===================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
const animatedElements = document.querySelectorAll('.service-card, .benefit-card, .testimonial-card, .step-item, .team-feature');
animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ===================================
// CTA Button Scroll to Contact
// ===================================
// FIX: Exclude the form's submit button (.full-width) to avoid hijacking form submission.
// Only target CTA buttons that are NOT inside a <form>.
const ctaButtons = document.querySelectorAll('.btn-primary:not(.full-width), .cta-button');
ctaButtons.forEach(button => {
    if (button.textContent.includes('Request') || button.textContent.includes('Book') || button.textContent.includes('Start')) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const contactSection = document.getElementById('contact');
            if (contactSection) {
                const offsetTop = contactSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    }
});

// ===================================
// Learn More Button Scroll
// ===================================
const learnMoreButtons = document.querySelectorAll('.btn-secondary');
learnMoreButtons.forEach(button => {
    if (button.textContent.includes('Learn More')) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const howItWorks = document.getElementById('how-it-works');
            if (howItWorks) {
                const offsetTop = howItWorks.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    }
});

// ===================================
// Active Navigation Link
// ===================================
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === `#${current}`) {
            item.classList.add('active');
        }
    });
});

// ===================================
// Statistics Counter Animation
// ===================================
const stats = document.querySelectorAll('.stat-number');
let hasAnimated = false;

const animateStats = () => {
    if (hasAnimated) return;
    
    const heroSection = document.querySelector('.hero');
    const heroPosition = heroSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight;
    
    if (heroPosition < screenPosition) {
        stats.forEach(stat => {
            const target = stat.textContent;
            const isNumber = !isNaN(parseInt(target));
            
            if (isNumber) {
                const number = parseInt(target);
                const increment = number / 50;
                let current = 0;
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= number) {
                        stat.textContent = target;
                        clearInterval(timer);
                    } else {
                        stat.textContent = Math.floor(current) + (target.includes('+') ? '+' : '');
                    }
                }, 30);
            }
        });
        hasAnimated = true;
    }
};

window.addEventListener('scroll', animateStats);
window.addEventListener('load', animateStats);

// ===================================
// Lazy Loading Images
// ===================================
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}

console.log('Ayur Narayana website loaded successfully!');