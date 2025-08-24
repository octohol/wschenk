# Tailspin Toys Crowd Funding Development Guidelines

This is a crowdfunding platform for games with a developer theme. The application uses a Flask backend API with SQLAlchemy ORM for database interactions, and an Astro/Svelte frontend with Tailwind CSS for styling. Please follow these guidelines when contributing:

## Code standards

### Required Before Each Commit

- Run Python tests to ensure backend functionality
- Format Python code with `black` and sort imports with `isort` 
- Ensure all new Python functions and classes have proper docstrings following Google style
- For frontend changes, run builds in the client directory to verify build success and the end-to-end tests, to ensure everything works correctly
- When making API changes, update and run the corresponding tests to ensure everything works correctly
- When updating models, ensure database migrations are included if needed
- When adding new functionality, make sure you update the README
- Make sure all guidance in the Copilot Instructions file is updated with any relevant changes, including to project structure and scripts, and programming guidance

### Global language guidance

- Use type hints for function parameters and return values for all languages which support them

### Python and Flask Patterns

- Use SQLAlchemy models for database interactions
- Use Flask blueprints for organizing routes
- Follow RESTful API design principles

### Python Formatting Standards

- Use [black](https://black.readthedocs.io/) for code formatting with default settings
- Use [isort](https://pycqa.github.io/isort/) for import sorting with profile "black" for compatibility
- Line length should be 88 characters (black default)
- Use double quotes for strings unless single quotes avoid escaping

### Python Documentation Standards

- All modules must have a module-level docstring describing their purpose
- All public functions and methods must have docstrings following Google style format
- All classes must have docstrings describing their purpose and key attributes
- Docstrings should include:
  - Brief description of the function/class purpose
  - Args: description of each parameter with type information
  - Returns: description of return value and type (if applicable)
  - Raises: description of exceptions that may be raised (if applicable)
- Use triple double quotes (""") for all docstrings
- Example format:
  ```python
  def example_function(param1: str, param2: int) -> bool:
      """Brief description of function purpose.
      
      Longer description if needed to explain complex behavior.
      
      Args:
          param1: Description of the first parameter.
          param2: Description of the second parameter.
          
      Returns:
          Description of return value.
          
      Raises:
          ValueError: Description of when this exception is raised.
      """
  ```

### Svelte and Astro Patterns

- Use Svelte for interactive components
- Follow Svelte's reactive programming model
- Create reusable components when functionality is used in multiple places
- Use Astro for page routing and static content

### Styling

- Use Tailwind CSS classes for styling
- Maintain dark mode theme throughout the application
- Use rounded corners for UI elements
- Follow modern UI/UX principles with clean, accessible interfaces

### GitHub Actions workflows

- Follow good security practices
- Make sure to explicitly set the workflow permissions
- Add comments to document what tasks are being performed

## Scripts

- Several scripts exist in the `scripts` folder
- Use existing scripts to perform tasks rather than performing them manually
- Existing scripts:
    - `scripts/setup-env.sh`: Performs installation of all Python and Node dependencies
    - `scripts/run-server-tests.sh`: Calls setup-env, then runs all Python tests
    - `scripts/start-app.sh`: Calls setup-env, then starts both backend and frontend servers

## Repository Structure

- `server/`: Flask backend code
  - `models/`: SQLAlchemy ORM models
  - `routes/`: API endpoints organized by resource
  - `tests/`: Unit tests for the API
  - `utils/`: Utility functions and helpers
- `client/`: Astro/Svelte frontend code
  - `src/components/`: Reusable Svelte components
  - `src/layouts/`: Astro layout templates
  - `src/pages/`: Astro page routes
  - `src/styles/`: CSS and Tailwind configuration
- `scripts/`: Development and deployment scripts
- `data/`: Database files
- `docs/`: Project documentation
- `README.md`: Project documentation
