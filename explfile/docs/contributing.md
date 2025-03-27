# Contributing to VoxStitch

## Getting Started

### 1. Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/your-username/voxstitch.git
cd voxstitch
```

2. **Install Dependencies**
```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. **Environment Setup**
```bash
# Frontend
cp frontend/.env.example frontend/.env

# Backend
cp backend/.env.example backend/.env
```

### 2. Development Workflow

1. **Create Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes**
- Follow coding standards
- Add tests
- Update documentation

3. **Commit Changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

4. **Push Changes**
```bash
git push origin feature/your-feature-name
```

5. **Create Pull Request**
- Use PR template
- Add description
- Link related issues

## Code Standards

### 1. TypeScript/React Guidelines

```typescript
// Use functional components
const Component: React.FC<Props> = ({ prop1, prop2 }) => {
  // Use hooks at the top
  const [state, setState] = useState<string>('');
  
  // Define handlers
  const handleClick = useCallback(() => {
    setState('new value');
  }, []);
  
  // Return JSX
  return (
    <div>
      <h1>{prop1}</h1>
      <button onClick={handleClick}>{prop2}</button>
    </div>
  );
};

// Use proper typing
interface Props {
  prop1: string;
  prop2: string;
}

// Export at the bottom
export default Component;
```

### 2. Python Guidelines

```python
# Use type hints
from typing import Dict, List, Optional

class ChatProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def process_chat(
        self,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process chat messages with given options.
        
        Args:
            messages: List of chat messages
            options: Optional processing options
            
        Returns:
            Processed chat data
        """
        # Implementation
        pass
```

### 3. Documentation Guidelines

```markdown
# Component/Module Name

## Purpose
Brief description of what this component/module does.

## Usage
```typescript
import { Component } from './Component';

<Component prop1="value" prop2="value" />
```

## Props/Parameters
| Name  | Type   | Required | Description |
|-------|--------|----------|-------------|
| prop1 | string | Yes      | Purpose     |
| prop2 | string | No       | Purpose     |

## Examples
Show common use cases.
```

## Testing Requirements

### 1. Frontend Tests

```typescript
describe('Component', () => {
  // Setup
  beforeEach(() => {
    // Setup code
  });
  
  // Test cases
  it('should render correctly', () => {
    render(<Component prop1="test" />);
    expect(screen.getByText('test')).toBeInTheDocument();
  });
  
  it('should handle interactions', async () => {
    render(<Component prop1="test" />);
    await userEvent.click(screen.getByRole('button'));
    expect(mockHandler).toHaveBeenCalled();
  });
});
```

### 2. Backend Tests

```python
def test_chat_processing():
    processor = ChatProcessor(config)
    
    # Test basic functionality
    result = await processor.process_chat(test_messages)
    assert result['status'] == 'success'
    
    # Test edge cases
    result = await processor.process_chat([])
    assert result['status'] == 'error'
```

## Pull Request Process

### 1. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots
If applicable, add screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No new warnings
```

### 2. Review Process

1. **Code Review**
   - Style compliance
   - Test coverage
   - Performance impact
   - Security considerations

2. **Documentation Review**
   - API documentation
   - Usage examples
   - Architecture updates

3. **Testing Review**
   - Test coverage
   - Edge cases
   - Performance tests

## Development Tools

### 1. Recommended VSCode Extensions

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "ms-python.vscode-pylance"
  ]
}
```

### 2. Git Hooks

```bash
#!/bin/sh
# pre-commit

# Run linters
npm run lint
flake8 backend/

# Run tests
npm test
pytest backend/tests/

# Check types
tsc --noEmit
mypy backend/
```

## Release Process

### 1. Version Control

```bash
# Update version
npm version patch # or minor/major
git tag v1.0.1
git push origin v1.0.1
```

### 2. Changelog

```markdown
# Changelog

## [1.0.1] - 2025-03-27
### Added
- New feature X
- New component Y

### Fixed
- Bug in component Z
- Performance issue in API

### Changed
- Updated dependency A
- Improved documentation
```

## Community Guidelines

### 1. Communication

- Use inclusive language
- Be respectful
- Stay on topic
- Help others learn

### 2. Issue Reporting

```markdown
## Issue Template

### Description
Clear description of the issue

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- OS:
- Browser:
- Version:
```

### 3. Feature Requests

```markdown
## Feature Request Template

### Problem
What problem does this solve?

### Proposed Solution
How should it work?

### Alternatives Considered
What other approaches exist?

### Additional Context
Any other relevant information
```

## Resources

### 1. Documentation
- Architecture Guide
- API Reference
- Testing Guide
- Style Guide

### 2. Tools
- ESLint configuration
- Prettier configuration
- PyTest configuration
- CI/CD pipelines

### 3. Templates
- Component templates
- Test templates
- Documentation templates
- PR templates
