# ExpenseIQ Core Coding Rules

## Universal Principles

WE'RE FOLLOWING THE CODE-FIRST APPROACH.

### Architecture & Design

- Always follow MVC architecture
    - Models: Data structures and business logic
    - Views: User interface and presentation
    - Controllers: Request handling and orchestration

- Maintain clear separation of concerns
    - Each module should have a single responsibility
    - Avoid tight coupling between components

- Keep code readable, modular, and testable
    - Use meaningful variable and function names
    - Write functions that do one thing well
    - Ensure code is easily unit testable

### Code Quality

- Code must compile/run without errors or warnings
    - Fix all linting issues before committing
    - Run tests before submission

- Do not declare unused variables, imports, or functions
    - Remove dead code regularly
    - Clean up imports before finalizing

### Error Handling

- Add proper exception handling
    - Catch specific exceptions, not generic ones

- Handle failures gracefully and return meaningful errors
    - Return structured error responses
    - Include error codes and descriptions

- Do not expose internal stack traces or sensitive details
    - Log errors internally
    - Return user-friendly error messages

### Logging & Debugging

- Log only essential error information or flow-critical events
    - Log at appropriate levels (ERROR, INFO, WARNING)

- Avoid debug, verbose, or development-only logs
    - Remove test logs before production deployment

## Python-Specific Guidelines (Backend)

### Language & Standards

- Follow PEP 8 style guide
- Use type hints where applicable

### Error Handling

- Use try-except blocks appropriately
    - Catch specific exceptions, not generic ones

### Logging & Debugging

- Use logging framework instead of print()
    - Do not add unnecessary console prints

## React-Specific Guidelines (Frontend)

### Language & Standards

- Follow React and JSX best practices
- Use TypeScript where applicable

### Architecture

- Use functional components only
- Follow MVC mapping in React
    - Models: Data models / interfaces
    - Views: JSX components (UI only)
    - Controllers: Hooks or controller modules handling logic

- Keep business logic out of JSX

### React Hooks

- Use React Hooks correctly (`useState`, `useEffect`, etc.)
    - Clean up side effects properly
    - Avoid unnecessary re-renders

### Error Handling

- Use try/catch for async operations
- Handle API and async errors gracefully
    - Provide fallback UI where required

### Logging & Debugging

- Avoid excessive console.log usage
    - Do not add unnecessary console prints or logs

### Code Cleanup

- Remove unused props, state variables, and imports
