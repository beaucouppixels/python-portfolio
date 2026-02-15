# Contributing to Python Portfolio

Thank you for your interest in contributing! While this is primarily a personal portfolio repository, I welcome feedback, suggestions, and contributions that improve the projects.

## How to Contribute

###  Reporting Bugs

If you find a bug, please create an issue with:
- Clear title describing the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Python version and OS
- Relevant code snippets or error messages

###  Suggesting Enhancements

For feature requests or improvements:
- Check existing issues first to avoid duplicates
- Clearly describe the enhancement and its benefits
- Include examples or use cases if applicable

### 🔧 Code Contributions

If you'd like to contribute code:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed
4. **Test your changes**
   ```bash
   python3 your_script.py
   ```
5. **Commit with a descriptive message**
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**
   - Describe what your PR does
   - Reference any related issues
   - Explain testing you've performed

## Code Style Guidelines

- **PEP 8:** Follow Python style guidelines
- **Documentation:** Add docstrings for functions and classes
- **Comments:** Explain "why", not "what"
- **Naming:** Use descriptive variable and function names

Example:
```python
def fetch_page(url, max_retries=3, delay=1):
    """
    Fetch page content with retry logic and better error handling
    
    Args:
        url (str): The URL to fetch
        max_retries (int): Maximum number of retry attempts
        delay (int): Initial delay between retries in seconds
        
    Returns:
        str: The HTML content of the page
        
    Raises:
        RequestException: If all retry attempts fail
    """
    # Implementation...
```

## Project Structure

```
python-portfolio/
├── webscraper/           # Web scraping project
│   ├── README.md        # Project documentation
│   └── webscrapper.py   # Main scraper script
├── future-project/       # Template for new projects
│   ├── README.md
│   └── src/
└── tests/               # Unit tests (future)
```

## Questions?

Feel free to:
- Open an issue for questions
- Reach out on LinkedIn
- Email me (see README for contact info)

## Code of Conduct

Be respectful and constructive. This is a learning and professional development space.

---

Thank you for helping improve this portfolio! 
