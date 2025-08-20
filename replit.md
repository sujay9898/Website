# Overview

A modern Flask web application featuring a portfolio/personal website with responsive design, clean architecture, and Replit deployment optimization. The application showcases projects, provides contact functionality, and includes a keep-alive service for reliable hosting on Replit.

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
- **Web Framework**: Flask with simple routing structure
- **Data Storage**: In-memory data structures (PROJECTS list) for portfolio content
- **Session Management**: Flask sessions with configurable secret key
- **Error Handling**: Flash messaging system for user feedback
- **Logging**: Python logging module configured for debugging

## Application Structure
- **Route Organization**: Single-file routing with dedicated endpoints for home, about, portfolio, and contact
- **Static Assets**: Organized CSS and JavaScript files in dedicated static directories
- **Template Hierarchy**: Base template with page-specific extensions for consistent layout

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