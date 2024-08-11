import os
import shutil

import json
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

'''
find_files_and_render_templates iterates over all items in the current directory, looking for subdirectoies.
For each subdirectory, it loads the Jinja2 template and renders it with the data from any JSON or YAML files in the subdirectory.
The rendered content is saved to a new file in the output directory.
'''
def find_files_and_render_templates(inputs_dir_name, outputs_dir_name):
    current_dir = Path(os.getcwd())
    inputs_dir = current_dir/inputs_dir_name
    outputs_dir = current_dir/outputs_dir_name
    outputs_dir.mkdir(parents=True, exist_ok=True)
    print(f'Inputs dir: {inputs_dir.absolute()}')
    print(f'Outputs dir: {outputs_dir.absolute()}')

    # Iterate over all items in the current directory
    for item in inputs_dir.iterdir():
        cur_template_dir = inputs_dir / item

        # Check if the item is a directory
        if cur_template_dir.is_dir():
            output_item = outputs_dir / item.name
            output_item.mkdir(parents=True, exist_ok=True)
            print(f'Processing template directory: {cur_template_dir.absolute()}')

            # Load the Jinja2 template
            env = Environment(loader=FileSystemLoader(cur_template_dir.absolute()))
            template = env.get_template('template.alloy.j2')
            
            for datafile in cur_template_dir.iterdir():
                # Skip Jinja2 templates
                if datafile.suffix == '.j2':
                    continue
                print(f'Processing file: {datafile.absolute()}')

                cur_file_contents = load_file(datafile)

                rendered_content = template.render(data=cur_file_contents.get('data', {}))
                # Save the rendered content to a new file
                output_file_path = outputs_dir / item.name / f'{datafile.name.split(".")[0]}.alloy'
                with output_file_path.open(mode='w') as output_file:
                    output_file.write(rendered_content)
            print(f'Done processing directory: {cur_template_dir.absolute()}')
    
    print('Cleaning up outputs directory', end=' ')

    # Remove directories from outputs_dir that don't exist in inputs_dir
    for output_item in outputs_dir.iterdir():
        if output_item.is_dir():
            corresponding_input_dir = inputs_dir / output_item.name
            if not corresponding_input_dir.exists():
                print(f'Removing directory as it is not in the inputs directory: {output_item.absolute()}')
                shutil.rmtree(output_item)
    print('<OK>')

def load_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.suffix == '.json':
            return json.load(file)
        elif file_path.suffix in ['.yaml', '.yml']:
            return yaml.load(file, Loader=yaml.FullLoader)
        else:
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")

if __name__ == '__main__':
    inputs_dir_name = os.environ.get('INPUT_INPUTS_DIR_NAME', 'templates')
    outputs_dir_name = os.environ.get('INPUT_OUTPUTS_DIR_NAME', 'pipelines')
    matching_files = find_files_and_render_templates(inputs_dir_name, outputs_dir_name)
