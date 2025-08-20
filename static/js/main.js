// Main JavaScript file for Flask Modern App
// Handles interactive features and UI enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeNavigation();
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();
    initializePortfolio();
    initializeScrollEffects();
    
    console.log('Flask Modern App initialized successfully!');
});

// Navigation functionality
function initializeNavigation() {
    // Highlight active navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Find first invalid field and focus it
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            } else {
                // Show loading state on submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i data-feather="loader" class="me-2"></i>Sending...';
                    submitBtn.disabled = true;
                    
                    // Re-initialize feather icons for the new loader icon
                    if (window.feather) {
                        feather.replace();
                    }
                    
                    // Reset button after 3 seconds if form is still visible
                    setTimeout(() => {
                        if (document.body.contains(submitBtn)) {
                            submitBtn.innerHTML = originalText;
                            submitBtn.disabled = false;
                            if (window.feather) {
                                feather.replace();
                            }
                        }
                    }, 3000);
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation feedback
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
}

// Animation and scroll effects
function initializeAnimations() {
    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll(
        '.feature-card, .project-card, .portfolio-item, .tool-category'
    );
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Initialize tooltips and popovers
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Portfolio functionality
function initializePortfolio() {
    // Portfolio filtering (if on portfolio page)
    const portfolioTabs = document.querySelectorAll('#portfolioTabs button');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    portfolioTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-bs-target');
            
            // Add smooth transition
            portfolioItems.forEach(item => {
                item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            });
        });
    });
}

// Scroll effects
function initializeScrollEffects() {
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove background to navbar on scroll
        if (scrollTop > 50) {
            navbar.classList.add('shadow-sm');
        } else {
            navbar.classList.remove('shadow-sm');
        }
        
        // Hide/show navbar on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Back to top button
    createBackToTopButton();
}

// Create back to top button
function createBackToTopButton() {
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i data-feather="arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle';
    backToTopButton.style.cssText = `
        width: 50px;
        height: 50px;
        z-index: 1000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    `;
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    document.body.appendChild(backToTopButton);
    
    // Replace feather icon
    if (window.feather) {
        feather.replace();
    }
    
    // Show/hide on scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.visibility = 'visible';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.visibility = 'hidden';
        }
    });
}

// Project details modal (for portfolio page)
function showProjectDetails(projectTitle) {
    const modal = document.getElementById('projectModal');
    const modalTitle = document.getElementById('projectModalLabel');
    const modalBody = document.getElementById('projectDetails');
    
    if (modal && modalTitle && modalBody) {
        modalTitle.textContent = projectTitle;
        
        // Sample project details (in a real app, this would come from an API)
        const projectDetails = {
            'E-Commerce Platform': {
                description: 'A comprehensive e-commerce solution built with Flask, featuring user authentication, product catalog, shopping cart, and payment integration.',
                features: ['User Authentication', 'Product Management', 'Shopping Cart', 'Payment Gateway', 'Order Tracking', 'Admin Dashboard'],
                technologies: ['Flask', 'SQLAlchemy', 'Bootstrap', 'JavaScript', 'Stripe API'],
                timeline: '6 weeks',
                status: 'Completed'
            },
            'Task Management App': {
                description: 'A collaborative task management application with real-time updates, team collaboration features, and progress tracking.',
                features: ['Real-time Updates', 'Team Collaboration', 'Progress Tracking', 'File Attachments', 'Notifications', 'Mobile Responsive'],
                technologies: ['Python', 'WebSockets', 'HTML5', 'CSS3', 'Socket.IO'],
                timeline: '4 weeks',
                status: 'In Progress'
            },
            'Data Analytics Dashboard': {
                description: 'Interactive dashboard for data visualization and analytics with customizable charts and reporting features.',
                features: ['Interactive Charts', 'Custom Reports', 'Data Export', 'User Permissions', 'Real-time Data', 'Mobile Support'],
                technologies: ['Flask', 'Chart.js', 'Pandas', 'Bootstrap', 'D3.js'],
                timeline: '8 weeks',
                status: 'Planning'
            }
        };
        
        const project = projectDetails[projectTitle];
        if (project) {
            modalBody.innerHTML = `
                <div class="row">
                    <div class="col-md-8">
                        <h6>Project Description</h6>
                        <p class="text-muted mb-4">${project.description}</p>
                        
                        <h6>Key Features</h6>
                        <ul class="list-unstyled">
                            ${project.features.map(feature => `
                                <li class="mb-1">
                                    <i data-feather="check" class="text-success me-2"></i>${feature}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="project-meta bg-light bg-opacity-10 p-3 rounded">
                            <h6>Project Details</h6>
                            <div class="mb-3">
                                <small class="text-muted">Status</small>
                                <div>
                                    <span class="badge ${project.status === 'Completed' ? 'bg-success' : project.status === 'In Progress' ? 'bg-primary' : 'bg-secondary'}">
                                        ${project.status}
                                    </span>
                                </div>
                            </div>
                            <div class="mb-3">
                                <small class="text-muted">Timeline</small>
                                <div>${project.timeline}</div>
                            </div>
                            <div class="mb-3">
                                <small class="text-muted">Technologies</small>
                                <div class="mt-1">
                                    ${project.technologies.map(tech => `
                                        <span class="badge bg-primary bg-opacity-10 text-primary me-1 mb-1">${tech}</span>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Re-initialize feather icons
            if (window.feather) {
                feather.replace();
            }
        }
        
        // Show modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    
    // You could send error reports to a logging service here
    // For now, we'll just log it to the console
});

// Service worker registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment below if you add a service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         console.log('SW registered: ', registration);
        //     })
        //     .catch(function(registrationError) {
        //         console.log('SW registration failed: ', registrationError);
        //     });
    });
}

// Export functions for use in other scripts
window.FlaskApp = {
    showProjectDetails,
    initializeFormValidation,
    debounce,
    throttle
};
