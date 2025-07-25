#!/usr/bin/env python
import os
import sys
import subprocess
import importlib.util

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'databseschema')
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backenddjango')

def check_django_extensions():
    """Check if django-extensions is installed."""
    try:
        importlib.util.find_spec('django_extensions')
        return True
    except ImportError:
        return False

def install_django_extensions():
    """Install django-extensions package."""
    print("Installing django-extensions...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django-extensions", "pygraphviz"])
    print("django-extensions installed successfully.")

def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")
    else:
        print(f"Output directory already exists: {OUTPUT_DIR}")

def generate_schema():
    """Generate database schema visualization."""
    # Change to the Django project directory
    os.chdir(BACKEND_DIR)
    
    # Add django-extensions to INSTALLED_APPS temporarily
    settings_path = os.path.join(BACKEND_DIR, 'crm_backend', 'settings.py')
    with open(settings_path, 'r') as f:
        settings_content = f.read()
    
    if "'django_extensions'," not in settings_content:
        # Find the INSTALLED_APPS section and add django_extensions
        apps_start = settings_content.find('INSTALLED_APPS = [')
        if apps_start != -1:
            apps_end = settings_content.find(']', apps_start)
            if apps_end != -1:
                modified_settings = (
                    settings_content[:apps_end] + 
                    "    'django_extensions',\n" + 
                    settings_content[apps_end:]
                )
                
                with open(settings_path, 'w') as f:
                    f.write(modified_settings)
                print("Added django_extensions to INSTALLED_APPS")
    
    # Generate the visualization
    dot_file = os.path.join(OUTPUT_DIR, 'db_schema.dot')
    png_file = os.path.join(OUTPUT_DIR, 'db_schema.png')
    
    # Define the apps to include in the visualization
    apps = [
        'applications',
        'borrowers',
        'brokers',
        'documents',
        'products',
        'users'
    ]
    
    # First generate DOT file
    dot_cmd = [
        sys.executable, 'manage.py', 'graph_models',
        '-a',  # Include all applications
        '--dot',  # Output in DOT format
        '-o', dot_file
    ]
    
    # Execute the command to generate DOT file
    try:
        print("Generating DOT file...")
        subprocess.check_call(dot_cmd)
        print(f"DOT file generated successfully at: {dot_file}")
        
        # Then convert DOT to PNG using graphviz dot command
        print("Converting DOT to PNG...")
        subprocess.check_call(['dot', '-Tpng', dot_file, '-o', png_file])
        print(f"PNG file generated successfully at: {png_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating schema: {e}")
        # Try with specific apps if -a fails
        try:
            app_dot_cmd = [
                sys.executable, 'manage.py', 'graph_models',
                *apps,  # Include specific apps
                '--dot',
                '-o', dot_file
            ]
            subprocess.check_call(app_dot_cmd)
            print(f"DOT file generated successfully with specific apps at: {dot_file}")
            
            # Convert DOT to PNG
            subprocess.check_call(['dot', '-Tpng', dot_file, '-o', png_file])
            print(f"PNG file generated successfully at: {png_file}")
            
        except subprocess.CalledProcessError as e2:
            print(f"Error generating schema with specific apps: {e2}")
    
    # Restore settings.py if modified
    if "'django_extensions'," not in settings_content:
        with open(settings_path, 'w') as f:
            f.write(settings_content)
        print("Restored original settings.py")

def main():
    """Main function to orchestrate the schema generation process."""
    print("Starting database schema visualization generation...")
    
    # Check and install django-extensions if needed
    if not check_django_extensions():
        install_django_extensions()
    else:
        print("django-extensions is already installed.")
    
    # Ensure output directory exists
    ensure_output_directory()
    
    # Generate the schema
    generate_schema()
    
    print("Process completed.")

if __name__ == "__main__":
    main()
