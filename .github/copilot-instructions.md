# GitHub Copilot Context

This project is a testbed for different map solving techniques.

## Tooling

- uv for package management using dependency groups
- pytest and pytest-cov for test automation and test coverage generation
- Git for source code versioning
- SonarCloud for code quality analysis
- GitHub Actions for continuous integration and deployment

## Project structure

- Source files in the src directory, packaging ready
- The package name and properties in the pyproject.toml file
- Ready for packaging
- Test files in the tests directory

### Features

- Map generation
- Simple UI widgets
- Keyboard controlled behaviour
- Asset loading for widgets
- Minimap and normal map rendering
- Profiling and benchmarking

## Guidelines

### Software design principles

As a professional software developer also experienced in test automation, you should follow
these rules:

- Use software design patterns
- Apply SOLID desing principles as:
    - Single Responsibility Principle: A class should have only one reason to change, meaning it should have only one
      job.
    - Open/Closed Principle: Software entities should be open for extension but closed for modification.
    - Liskov Substitution Principle: Subtypes must be substitutable for their base types without altering the
      correctness of the program.
    - Interface Segregation Principle: Clients should not be forced to depend on interfaces they do not use.
    - Dependency Inversion Principle: High-level modules should not depend on low-level modules; both should depend on
      abstractions.
- Apply DRY principle
- Apply KISS principle
- Apply YAGNI principle
- Apply ISP principle

### Clean code

- Keep the code clean, apply comments only when really needed. We don't want to see comments in every line.
- Keep the method and function cognitive complexity below 15
- Keep method and function length below 30 lines excluding the comments.
- Keep the number of methods below 20 within a class.
- Keep the number of global variables below 3.
- Keep the number of exceptions ignored below 1.

### Pythonic code

- Use slotted dataclasses or Pydantic V2 data models when applicable
- Use generators and iterators when applicable
- Use effective Python data structures and algorithms
- Use type hints and data validation, prefer Pydantic V2 when applicable

### Testing

- GitHub Copilot should run tests to check the correctness of the proposed solution
- GitHub Copilot should ensure on a refactoring task the working solution should also be working after refactoring.

