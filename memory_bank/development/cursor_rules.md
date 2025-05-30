# Cursor Development Rules

## Overview
This document outlines the rules and guidelines for using Cursor in our Knowledge Retrieval System development. These rules ensure consistent and efficient development practices across the team.

## Version Information
- Version: 1.0.0
- Last Updated: 2024-04-23
- Status: Active

## General Rules

### 1. Code Generation
- Always review generated code before committing
- Ensure generated code follows project style guidelines
- Document any significant AI-generated code sections
- Verify generated code against existing patterns

### 2. Documentation
- Use Cursor for initial documentation drafts
- Review and refine AI-generated documentation
- Ensure documentation matches actual implementation
- Update documentation when code changes

### 3. Testing
- Generate test stubs using Cursor
- Review and complete test implementations
- Ensure test coverage requirements are met
- Verify test quality and completeness

## Specific Guidelines

### 1. Code Generation Rules
```markdown
1. **Prompt Guidelines**
   - Be specific and clear in prompts
   - Include context and requirements
   - Specify expected output format
   - Mention any constraints or limitations

2. **Review Process**
   - Review generated code line by line
   - Check for security vulnerabilities
   - Verify performance implications
   - Ensure compliance with standards

3. **Integration Rules**
   - Follow existing patterns
   - Maintain consistent style
   - Document integration points
   - Verify dependencies
```

### 2. Documentation Rules
```markdown
1. **Documentation Structure**
   - Follow project templates
   - Include version information
   - Maintain consistent formatting
   - Use clear language

2. **Content Guidelines**
   - Be specific and accurate
   - Include examples where needed
   - Document edge cases
   - Keep documentation up-to-date

3. **Review Process**
   - Technical review required
   - Verify accuracy
   - Check completeness
   - Ensure clarity
```

### 3. Testing Rules
```markdown
1. **Test Generation**
   - Generate test stubs
   - Include test cases
   - Specify test data
   - Document test scenarios

2. **Test Implementation**
   - Complete test logic
   - Add assertions
   - Handle edge cases
   - Include cleanup

3. **Test Quality**
   - Meet coverage requirements
   - Ensure reliability
   - Verify performance
   - Check maintainability
```

## Best Practices

### 1. Code Generation
```python
# Example of good prompt structure
"""
Generate a function that:
1. Takes input parameters: param1, param2
2. Returns: processed_result
3. Handles errors: specific_error_types
4. Follows pattern: existing_pattern_name
5. Includes: documentation, type hints
"""

# Example of code review checklist
"""
1. Security review
2. Performance check
3. Style compliance
4. Documentation
5. Test coverage
"""
```

### 2. Documentation
```markdown
# Example documentation structure
"""
## Component Name
### Purpose
### Usage
### Examples
### Edge Cases
### References
"""
```

### 3. Testing
```python
# Example test structure
"""
def test_component_functionality():
    # Setup
    # Execution
    # Verification
    # Cleanup
"""
```

## Quality Assurance

### 1. Code Quality
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Maintain consistent style

### 2. Documentation Quality
- Clear and concise
- Technically accurate
- Well-structured
- Up-to-date

### 3. Test Quality
- Comprehensive coverage
- Reliable execution
- Clear purpose
- Maintainable

## Security Considerations

### 1. Code Security
- Review for vulnerabilities
- Check input validation
- Verify authentication
- Ensure authorization

### 2. Data Security
- Protect sensitive data
- Follow encryption standards
- Secure storage
- Safe transmission

## Performance Guidelines

### 1. Code Performance
- Optimize algorithms
- Minimize resource usage
- Handle large datasets
- Manage memory efficiently

### 2. Documentation Performance
- Easy to navigate
- Quick to find information
- Clear structure
- Efficient updates

## Maintenance Rules

### 1. Code Maintenance
- Regular reviews
- Update dependencies
- Refactor when needed
- Document changes

### 2. Documentation Maintenance
- Regular updates
- Version control
- Change tracking
- Review process

## References
- [Cursor Documentation](https://cursor.sh/docs)
- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Project Documentation Standards](../development/documentation_standards.md)
- [Testing Guidelines](../development/testing_guidelines.md) 