# Component Generator CLI

A command-line tool for generating React component files with `PropTypes` and optional default properties in JavaScript (JSX). This tool helps developers quickly scaffold components by defining props, types, and default values from the command line.

---

## Features

- Generates a `.jsx` file with `PropTypes` definitions based on provided arguments
- Supports default prop values for common data types (strings, numbers, booleans, and functions)
- Adds ESLint comments for certain complex prop types (e.g., `objectOfany`)

---

## Installation

To use this tool, clone the repository and ensure you have Python 3.x installed.

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Make the script executable (optional)**:
    ```bash
    chmod +x generate_component.py
    ```
3. **Run the script**:
    ```bash
    python generate_component.py --help
    ```

---

## Usage

The CLI accepts three primary arguments:

- `component_name` (**required**): The name of the component to create.
- `--props` (**optional**): List of props in the format `name:type:required` (e.g., `myProp:string:true`).
- `--defaults` (**optional**): List of default prop values in the format `name:value` (e.g., `myProp:defaultValue`).

### Basic Command Format

```bash
python generate_component.py <component_name> [--props <name:type:required> ...] [--defaults <name:value> ...]
```

### Examples

#### Example 1: Generate a Component with Props and Default Values

The following command creates a component named `MyComponent.jsx` with specific prop types and default values:

```bash
python generate_component.py MyComponent --props title:string:true count:number:false --defaults title:"Hello" count:10
```

**Props:**
- `title`: a required string
- `count`: an optional number

**Defaults:**
- `title`: defaults to "Hello"
- `count`: defaults to 10

#### Example 2: Generate a Component with a Function Default

The following command creates a component with a function default for `onClick`:

```bash
python generate_component.py ButtonComponent --props onClick:function:false --defaults onClick:null_func
```

**Props:**
- `onClick`: an optional function

**Defaults:**
- `onClick`: defaults to a `null_func` (() => null)

### Argument Details

#### Component Name (Positional Argument)

The name of the component to create. This is a required argument and will name the `.jsx` file generated.

```bash
python generate_component.py MyComponent
```

#### --props

Defines the props for the component. Accepts multiple `name:type:required` entries. For instance:

```bash
--props title:string:true description:string:false
```

**Supported types:**

- `string`, `number`, `bool`, `func`, `array`, `object`, `objectOfany` (adds ESLint exception for `PropTypes.objectOf(PropTypes.any)`)
- `required` must be either `true` or `false`, indicating if the prop is mandatory.

#### --defaults

Defines the default values for the props, using the format `name:value`. This flag accepts common data types:

- **String**: Wrap in quotes (e.g., `title:"Hello"`)
- **Number**: Provide as-is (e.g., `count:10`)
- **Boolean**: Use `true` or `false`
- **Null function**: Use `null_func` to generate `() => null` (e.g., `onClick:null_func`)

### Output

The generated file, `<component_name>.jsx`, will be created in the current directory, containing the specified props and default values.

#### Example Output

Given the command:

```bash
python generate_component.py ExampleComponent --props name:string:true age:number:false --defaults name:"John Doe" age:30
```

The generated `ExampleComponent.jsx` file will look like:

```javascript
import PropTypes from 'prop-types';

const propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number,
};

const defaultProps = {
  name: "John Doe",
  age: 30,
};

const ExampleComponent = {
  propTypes,
  defaultProps,
};

export default ExampleComponent;
```

### Error Handling

- **Invalid Prop Format**: If a prop is not in the format `name:type:required`, an error will be displayed.
- **Invalid Default Format**: If a default value is incorrectly formatted, an error will be shown.

### Notes

- The tool uses `PropTypes.objectOf(PropTypes.any)` for `objectOfany` with an added ESLint exception.
- Use `null_func` for function props that default to an empty function (`() => null`).