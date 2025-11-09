# GitHub Copilot Context

This is the default Copilot prompt for this project.

## Tooling

- uv for package management using dependency groups
- pytest and pytest-cov for test automation and test coverage generation
- Git for sorce code versioning

## Project structure

- Source files in the src directory, packaging ready
- The package name and properties in the pyproject.toml file
- Ready for packaging
- Test files in the tests directory

### Features

- fixed title text
- scrolling caption from a text file
- timed captions from a csv file where timestamps and captions are stored
- reverse geolocation using an external Nominatim server
- TrueType font usage for text rendering
- Windows executable creation by Github Actions

## Guidelines

### Software design principles

As a professional software developer who is also experienced in test automation you should follow
these rules:
- Use software design patterns
- Apply SOLID desing principles as:
  -  Single Responsibility Principle: A class should have only one reason to change, meaning it should have only one job.
  -  Open/Closed Principle: Software entities should be open for extension but closed for modification.
  -  Liskov Substitution Principle: Subtypes must be substitutable for their base types without altering the correctness of the program.
  -  Interface Segregation Principle: Clients should not be forced to depend on interfaces they do not use.
  -  Dependency Inversion Principle: High-level modules should not depend on low-level modules; both should depend on abstractions.
- Apply DRY principle
- Apply KISS principle
- Keep the method and function cognitive complexity below 15
- Keep method and function length below 30 lines
- Use slotted dataclasses or Pydanticv2 data models when applicable
- Use generators and iterators when applicable
- Use effective Python data structures and algorithms