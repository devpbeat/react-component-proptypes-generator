import argparse
import os

# Template with and without default props
TEMPLATE_WITH_DEFAULTS = """import PropTypes from 'prop-types';

const propTypes = {{
{prop_definitions}
}};
const defaultProps = {{
{default_props}
}};

const {component_name} = {{
  propTypes,
  defaultProps,
}};

export default {component_name};
"""

TEMPLATE_NO_DEFAULTS = """import PropTypes from 'prop-types';

const propTypes = {{
{prop_definitions}
}};

const {component_name} = {{
  propTypes,
}};

export default {component_name};
"""

def generate_jsx(component_name, props, defaults):
    """
    Generates the JSX content for a component file with prop types and optional default props.
    """
    prop_definitions = "\n".join(
        [generate_prop_definition(name, ptype, required) for name, ptype, required in props]
    )

    # Format the default props, handling 'null_func' and other special cases
    default_props = "\n".join([
        f"  {name}: {format_default_value(value)}," for name, value in defaults.items()
    ])

    template = TEMPLATE_WITH_DEFAULTS if default_props else TEMPLATE_NO_DEFAULTS
    return template.format(
        component_name=component_name,
        prop_definitions=prop_definitions,
        default_props=default_props
    )

def generate_prop_definition(name, ptype, required):
    """
    Generate a single PropType definition, with an eslint-disable comment if needed.
    """
    if ptype == "objectOfany":
        return f"  // eslint-disable-next-line react/forbid-prop-types\n  {name}: PropTypes.objectOf(PropTypes.any){'.isRequired' if required else ''},"
    else:
        return f"  {name}: PropTypes.{ptype}{'.isRequired' if required else ''},"

def format_default_value(value):
    """
    Formats default values for JSX. Handles `null_func`, boolean, integer, and string cases.
    """
    if value == "null_func":
        return "() => null"
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (int, float)):
        return value
    return f'"{value}"'

def parse_props(props_list):
    """
    Parses and validates the props list from the command line argument.
    """
    props = []
    for prop in props_list or []:
        try:
            name, ptype, required = prop.split(":")
            required = required.lower() == "true"
            props.append((name, ptype, required))
        except ValueError:
            raise ValueError(f"Invalid prop format '{prop}'. Use name:type:required (e.g., myProp:string:true).")
    return props

def parse_defaults(defaults_list):
    """
    Parses and formats default values from the command line argument.
    """
    defaults = {}
    for default in defaults_list or []:
        try:
            name, value = default.split(":", 1)
            if value == "null_func":
                defaults[name] = "null_func"
            elif value.isdigit():
                defaults[name] = int(value)
            elif value.replace('.', '', 1).isdigit():
                defaults[name] = float(value)
            elif value.lower() in ["false", "true"]:
                defaults[name] = value.lower() == "true"
            else:
                defaults[name] = value
        except ValueError:
            raise ValueError(f"Invalid default format '{default}'. Use name:value (e.g., myProp:defaultValue).")
    return defaults

def main():
    parser = argparse.ArgumentParser(description="Generate a JSX component with PropTypes and defaultProps.")
    parser.add_argument("component_name", help="Name of the component to create.")
    parser.add_argument("--props", nargs="+", help="List of props in the format name:type:required (e.g., myProp:string:true).")
    parser.add_argument("--defaults", nargs="+", help="List of default props in the format name:value (e.g., myProp:defaultValue).")
    args = parser.parse_args()

    try:
        props = parse_props(args.props)
        defaults = parse_defaults(args.defaults)
    except ValueError as e:
        print(f"Error: {e}")
        return

    jsx_content = generate_jsx(args.component_name, props, defaults)
    filename = os.path.join(os.getcwd(), f"{args.component_name}.jsx")

    try:
        with open(filename, "w") as f:
            f.write(jsx_content)
        print(f"Created {filename} with the specified structure.")
    except IOError as e:
        print(f"Error: Could not write to file '{filename}': {e}")

if __name__ == "__main__":
    main()
