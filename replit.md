# Overview

A modern Flask web application featuring a poster gallery (Filmytea) with optimized image loading, responsive design, clean architecture, and Replit deployment optimization. The application showcases movie and entertainment posters with fast image loading and e-commerce functionality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templating with template inheritance via `base.html`
- **CSS Framework**: Bootstrap 5 with dark theme support via Replit CDN
- **Icons**: Feather Icons for consistent visual elements
- **JavaScript**: Vanilla JavaScript for interactivity (navigation, form validation, animations)
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

## Backend Architecture
- **Web Framework**: Flask with secure routing structure and ProxyFix middleware
- **Data Storage**: In-memory data structures (ALL_POSTERS list) for poster catalog
- **Database**: PostgreSQL with SQLAlchemy ORM and connection pooling
- **Session Management**: Flask sessions with environment-based secret key
- **Error Handling**: HTTP error codes with proper abort handling
- **Logging**: Python logging module configured for debugging

## Application Structure
- **Route Organization**: Clean routing with dedicated endpoints for home, poster gallery, and poster details
- **Static Assets**: Optimized CSS with image loading animations and responsive design
- **Template Hierarchy**: Individual templates with image optimization and progressive loading
- **Image Optimization**: Cloudinary CDN integration with automatic resizing, format conversion, and quality optimization

## Deployment Architecture
- **Keep-Alive Service**: Dedicated Flask server on port 8000 to prevent Replit hibernation
- **Environment Configuration**: Environment-based configuration for secrets and URLs
- **Threading**: Multi-threaded architecture separating main app from keep-alive service
- **Health Monitoring**: Automated ping system to maintain application availability

## Design Patterns
- **Template Inheritance**: Consistent layout and navigation across all pages
- **Configuration Management**: Environment variable-based configuration
- **Separation of Concerns**: Static assets, templates, and application logic properly separated
- **Service Architecture**: Keep-alive functionality isolated as separate service

# External Dependencies

## Frontend Dependencies
- **Bootstrap 5**: UI framework via Replit CDN for themed dark mode
- **Feather Icons**: Icon library via unpkg CDN
- **Google Fonts**: Modern font stack with system font fallbacks

## Backend Dependencies
- **Flask**: Core web framework
- **Threading**: Built-in Python module for concurrent keep-alive service
- **Requests**: HTTP client for keep-alive pings
- **OS**: Environment variable access

## Development Tools
- **Python Logging**: Built-in debugging and monitoring
- **Flask Development Server**: Local development environment

## Hosting Platform
- **Replit**: Primary hosting platform with specialized keep-alive optimization
- **Environment Variables**: REPL_URL and SESSION_SECRET configuration