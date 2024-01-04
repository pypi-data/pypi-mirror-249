import os
from pathlib import Path
from threading import Lock

import yaml

from .EmbeddingYAML import EmbeddingYAML
from .utils import manage_code_length, remove_empty_lines

# from .config import PROJECT_ROOT


REQUIRED_ENTITY_FIELDS = ["name", "description", "functional_category", "dependencies", "nested"]
REQUIRED_FILE_FIELDS = ["name", "description", "entities"]

class SummaryYAML:
    def __init__(self, root_directory, embedding_mode=False, yaml_dict=None, files_content=None):
        self.root_directory = Path(root_directory)
        self.current_directory = self.root_directory
        self.current_file = None
        self.current_entity = None
        self.current_entity_ancestry = []
        self.yaml_dict = yaml_dict
        self.files_content = files_content
        self.summary_data = self.load_yaml_recursive(self.root_directory)
        self.current_directory_summary = self.summary_data
        self.yaml_lock = Lock()

        if embedding_mode:
            embedding_file = os.path.join(self.root_directory, '.embeddings.yaml')
            self.embedding_yaml = EmbeddingYAML(embedding_file)
        else:
            self.embedding_yaml = None

    def load_yaml_recursive(self, directory):
        data = None
        if self.yaml_dict:
            data = self.yaml_dict.get(str(directory))
        # else:
        #     yaml_path = os.path.join(directory, '.summary.yaml')
        #     if not os.path.exists(yaml_path):
        #         return {}
        #     with open(yaml_path, 'r') as f:
        #         data = yaml.safe_load(f)


            subdirectories = data.get('subdirectories', [])
            data['subdirectories'] = {}
            for subdirectory in subdirectories:
                subdirectory_path = os.path.join(directory, subdirectory)
                data['subdirectories'][subdirectory] = self.load_yaml_recursive(subdirectory_path)

        return data

    def set_current_directory(self, new_directory):
        # Check if the new_directory is a direct subdirectory of the current_directory
        potential_new_directory = self.current_directory / new_directory

        if potential_new_directory.exists() and potential_new_directory.is_dir():
            self.current_directory = Path(potential_new_directory)
            return

        # Check if new_directory is a subdirectory of root_directory
        new_directory_path = Path(new_directory)

        try:
            new_directory_path.relative_to(self.root_directory)
        except ValueError:
            print("The new directory must be a subdirectory of the root directory or a direct subdirectory of the current directory.")
            print(f"This is the directory we tried to enter: {new_directory}")
            return

        self.current_directory = new_directory_path

    def set_current_file(self, file_name, directory=None, need_file_summary=True):
        if need_file_summary:
            if directory:
                self.set_current_directory(directory)
            data = self._navigate_to_current_directory()
            potential_files = [f for f in data.get('files', []) if f['name'] == file_name]
            if len(potential_files) == 0:
                self.current_file = None
            else:
                self.current_file = potential_files[0]
        else:
            self.current_file = directory / file_name

    def set_bookmark(self, bookmark, reset=False, need_file_summary=True):
        if reset:
            self.reset_bookmark()
        if bookmark[0].get('directory'):
            self.set_current_directory(bookmark[0].get('directory'))
            self.set_current_file(bookmark[0].get('file'), bookmark[0].get('directory'), need_file_summary)
            if len(bookmark) > 1:
                bookmark = bookmark[1:]
                self.set_current_entity(bookmark)
            else:
                self.current_entity = None
        else:
            self.set_current_entity(bookmark)

    def set_current_entity(self, entity_info, start_line=None, file_name=None, directory=None):
        if file_name:
            self.set_current_file(file_name, directory)
        if not self.current_file:
            raise ValueError("Current file is not set.")
        if isinstance(entity_info, str):
            # Handle non-nested entities
            self.current_entity = self.find_entity(self.current_file, entity_info, start_line)
            self.current_entity_ancestry = [self.current_entity]
        elif isinstance(entity_info, list):
            self.current_entity_ancestry = []
            # Handle nested entities
            parent = self.current_file
            for info in entity_info:
                entity = self.find_entity(parent, info['name'], info.get('start_line'))
                if entity is None:
                    raise ValueError(f"Entity {info['name']} not found.")
                self.current_entity_ancestry.append(entity)
                parent = entity
            self.current_entity = entity

        if self.current_entity is None:
            raise ValueError(f"Entity not found.")

    def reset_bookmark(self):
        self.current_directory = self.root_directory
        self.current_file = None
        self.current_entity = None
        self.current_entity_ancestry = []

    def get_current_bookmark(self):
        if not self.get_current_file(name_only=True):
            return [{'directory': self.get_current_directory(str_only=True)}]
        base_list = [{'directory': self.get_current_directory(str_only=True), 'file': self.get_current_file(name_only=True)}]
        base_list.extend([{'name': e['name'], 'start_line': e['start_line']} for e in self.current_entity_ancestry])
        return base_list

    def find_entity(self, parent, entity_name, start_line=None):
        if parent is self.current_file:
            candidates = [e for e in self.get_all_entities(parent.get('entities', [])) if e['name'] == entity_name]
        else:
            candidates = [e for e in self.get_all_entities(parent.get('nested', [])) if e['name'] == entity_name]

        if start_line:
            top_candidates = [e for e in candidates if e['start_line'] == start_line]
            if len(top_candidates) == 0:
                return None
            return top_candidates[0]
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            raise ValueError(f"Multiple entities with the name '{entity_name}' found. Please specify a start line.")
        return None

    def get_all_entities(self, entities):
        all_entities = []
        for entity in entities:
            all_entities.append(entity)
            if entity["nested"]:
                all_entities.extend(self.get_all_entities(entity["nested"]))
        return all_entities

    def get_files_in_current_directory(self):
        data = self._navigate_to_current_directory()
        return [f['name'] for f in data.get('files', [])]

    def get_subdirectories_in_current_directory(self):
        data = self._navigate_to_current_directory()
        return [d for d in data.get('subdirectories', [])]

    def get_entities_in_current_file(self):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        return [[{'name': e['name'], 'start_line': e['start_line']}] for e in self.current_file.get('entities', [])]

    def get_entities_hashes_in_current_file(self):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        hashes = self.get_entities_hashes(self.current_file.get('entities', []))
        return hashes

    def get_entities_hashes(self, entities):
        hashes = []
        for e in entities:
            hashes.append({'name': e['name'], 'entity_hash': e.get('entity_hash')})
            if e.get("nested"):
                hashes.extend(self.get_entities_hashes(e["nested"]))
        return hashes

    def get_current_file(self, name_only=False):
        if self.current_file:
            if name_only:
                return self.current_file['name']
            return os.path.join(self.current_directory, self.current_file['name'])
        return None

    def get_current_directory(self, str_only=False):
        if str_only:
            return str(self.current_directory)
        return self.current_directory

    def get_current_entity(self):
        return self.current_entity

    def get_nested_entities(self, include_start_line=False):
        if self.current_entity is None:
            return None

        nested_entities = self.current_entity.get('nested', [])

        if include_start_line:
            return [{'name': e['name'], 'start_line': e['start_line']} for e in nested_entities]
        else:
            return [e['name'] for e in nested_entities]

    def add_field(self, field_name, value):
        with self.yaml_lock:
            if not self.current_entity:
                raise ValueError("Current entity is not set.")
            self.current_entity[field_name] = value

    def add_field_to_current_file(self, field_name, value):
        with self.yaml_lock:
            if not self.current_file:
                raise ValueError("Current file is not set.")
            self.current_file[field_name] = value

    def add_field_to_current_directory(self, field_name, value):
        with self.yaml_lock:
            data = self._navigate_to_current_directory()
            data[field_name] = value

    def get_embedding_for_current_entity(self):
        if not self.embedding_yaml:
            raise ValueError("Embedding mode is off.")
        if not self.current_entity:
            raise ValueError("Current entity is not set.")
        return self.embedding_yaml.get_embedding_by_id(self.current_entity['entity_id'])

    def save(self):
        # Build the path to the correct .summary.yaml based on the current directory
        # save_path = os.path.join(self.current_directory, '.summary.yaml')

        # Navigate the summary_data dictionary to the data corresponding to the current directory
        data_to_save = self._navigate_to_current_directory().copy()
        self.current_directory_summary = data_to_save
        # data_to_save['subdirectories'] = [dir_name for dir_name in data_to_save.get('subdirectories',[])]
        #
        # if not self.yaml_dict:
        #     with open(save_path, 'w', encoding='utf-8') as f:
        #         yaml.dump(data_to_save, f)
        if self.current_directory == self.root_directory:
            self.yaml_dict[str(self.current_directory)] = data_to_save

    def get_current_file_type(self):
        if not self.current_file:
            raise ValueError("Current file is not set.")
        return self.current_file.get('file_type', None)

    def read_code_lines(self, start_line=None, end_line=None, file_path=None):
        if not file_path:
            if type(self.current_file) == dict:
                file_path = os.path.join(self.current_directory, self.current_file['name'])
            else:
                file_path = str(self.current_file)
        if start_line == None:
            start_line = 0
        if end_line != None:
            end_line += 1
        if not self.files_content or not self.files_content.get(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = self.files_content.get(file_path, "").split("\n")
        return ''.join(lines[start_line:end_line]).rstrip()  # Assuming 1-based line numbers in YAML

    def get_source_file_path(self):
        return os.path.join(self.current_directory, self.current_file['name'])

    def get_imports_in_current_file(self, up_to_line=None, file_path=None, imports=None):
        if not self.current_file:
            if file_path:
                self.current_file = file_path
            else:
                raise ValueError("Current file is not set.")
        if imports is None:
            imports = self.current_file.get('imports', [])
        if up_to_line:
            imports = [imp for imp in imports if imp['end_line'] <= up_to_line]
        code_imports = [{'info': imp, 'code': self.read_code_lines(imp['start_line'], imp['end_line'], file_path)} for imp in
                        imports]
        return code_imports

    def get_declarations_in_current_file(self, up_to_line=None, file_path=None, declarations=None):
        if not self.current_file:
            if file_path:
                self.current_file = file_path
            else:
                raise ValueError("Current file is not set.")
        if declarations is None:
            declarations = self.current_file.get('declarations', [])
        if up_to_line:
            declarations = [dec for dec in declarations if dec['end_line'] <= up_to_line]
        code_declarations = [{'info': dec, 'code': self.read_code_lines(dec['start_line'], dec['end_line'], file_path)} for dec in
                             declarations]
        return code_declarations

    def get_imports_and_declarations_in_current_file(self, up_to_line=True, include_line_number=False, file_path=None,
                                                     imports=None, declarations=None, file_end_line=None):
        # note that up_to_line should be language dependent, for Java it should likely be false
        if self.get_current_entity() and up_to_line:
            imports_and_declarations = self.get_declarations_in_current_file(up_to_line=self.get_current_entity()['start_line']) + self.get_imports_in_current_file(up_to_line=self.get_current_entity()['start_line'])
        else:
            imports_and_declarations = self.get_declarations_in_current_file(file_path=file_path, declarations=declarations) + self.get_imports_in_current_file(file_path=file_path, imports=imports)
        imports_and_declarations = sorted(imports_and_declarations, key=lambda x: x['info']['start_line'])
        if include_line_number:
            imports_and_declarations_code = "\n".join(
                [self.enumerate_code_lines(item['code'], item['info']['start_line'], file_end_line)
                 for item in imports_and_declarations])
        else:
            imports_and_declarations_code = '\n'.join(item['code'] for item in imports_and_declarations)

        return imports_and_declarations_code

    def enumerate_code_lines(self, code_lines, start_line, file_end_line=None):
        end_line = start_line + len(code_lines.split("\n"))

        if not file_end_line:
            file_end_line = max([a[0]['start_line'] for a in self.get_entities_in_current_file()])
        number_of_integers = len(str(file_end_line)) + 1

        enumerated_code = "\n".join([f"{str(line_number).zfill(number_of_integers)}: {code_line}"
                                     for line_number, code_line in zip(range(start_line, end_line + 1),
                                                                       code_lines.split("\n"))])
        return enumerated_code

    def get_entity_code(self, reduced=True, reduce_empty_lines=False, include_line_number=False,
                        file_path=None, file_type=None, file_end_line=None):
        if not self.current_file or not self.current_entity:
            raise ValueError("Either current file or entity is not set.")

        start_line = self.current_entity['start_line']
        end_line = self.current_entity['end_line']

        if not file_path:
            file_path = str(os.path.join(self.current_directory, self.current_file['name']))

        if not self.files_content or not self.files_content.get(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = [line + "\n" for line in self.files_content.get(file_path, "").splitlines()]

        nested_entities = self.current_entity.get('nested', [])
        nested_entities = sorted(nested_entities, key=lambda x: x['start_line'])
        entity_code = ''
        entity_code_for_prompt = ''
        last_line = start_line  # Initialize last_line to start_line

        if reduced:
            for nested_entity in nested_entities:
                nested_start = nested_entity['start_line']
                nested_end = nested_entity['end_line']
                nested_declaration_end = nested_entity.get('declaration_end_line', nested_start)
                description = nested_entity.get('description', '')

                # Get the indentation level from the nested entity's first line
                indentation = ''
                if nested_start < len(lines):
                    indentation = lines[nested_start][:len(lines[nested_start]) - len(lines[nested_start].lstrip())]

                # Add lines before the nested entity
                code_to_add = ''.join(lines[last_line:nested_start])
                entity_code += code_to_add
                if include_line_number:
                    entity_code_for_prompt += self.enumerate_code_lines(code_to_add, last_line, file_end_line)
                else:
                    entity_code_for_prompt += code_to_add
                # Add the nested entity's function definition line
                code_to_add = ''.join(lines[nested_start:nested_declaration_end + 1])
                entity_code += code_to_add
                if include_line_number:
                    entity_code_for_prompt += self.enumerate_code_lines(code_to_add, nested_start + 1,
                                                                        file_end_line)  # +1 here is not tested
                else:
                    entity_code_for_prompt += code_to_add
                # Add the description as a comment, replacing the function body
                entity_code_for_prompt += f"{indentation}    # {description}\n"

                last_line = nested_end + 1  # Update last_line to after the nested entity

        # Add remaining lines after the last nested entity
        if not file_type:
            file_type = self.get_current_file_type()
        actual_code = manage_code_length(''.join(lines[last_line:end_line + 1]).rstrip(), file_type)
        entity_code += actual_code
        if include_line_number:
            entity_code_for_prompt += self.enumerate_code_lines(actual_code, last_line, file_end_line)
        else:
            entity_code_for_prompt += actual_code

        if reduce_empty_lines and not include_line_number:
            entity_code = remove_empty_lines(entity_code)
            entity_code_for_prompt = remove_empty_lines(entity_code_for_prompt)
        return entity_code, entity_code_for_prompt

    def get_current_file_info(self):
        return self.current_directory, self.current_file['name'] if self.current_file else None

    def _get_entity_info(self, entity_info, level=0, prefix='  '):
        entity_info_str = ''

        # Set the current entity to this entity
        self.set_bookmark(entity_info)

        # Get its details
        entity = self.get_current_entity()

        # Create the string for this entity
        entity_info_str += f"{prefix * level}{entity['name']}: {entity.get('description', 'No description')}\n"

        # Check for nested entities within this entity
        nested_entities = self.get_nested_entities(include_start_line=True)

        # Recursively get info for each nested entity
        for nested_entity in nested_entities:
            self.set_bookmark(entity_info)
            current_entity_bookmark = self.get_current_bookmark()
            nested_entity_info = current_entity_bookmark + [nested_entity]
            entity_info_str += self._get_entity_info(nested_entity_info, level + 1)

        return entity_info_str

    def get_all_entities_info_in_current_file(self):
        all_entities_info = ""

        # First, get the list of top-level entities in the current file
        entities_in_file = self.get_entities_in_current_file()

        # Loop through each top-level entity to get its info and its nested entities info
        for entity_info in entities_in_file:
            all_entities_info += self._get_entity_info(entity_info)

        return all_entities_info

    def get_all_file_info_in_current_directory(self):
        files_info_str = ''
        files = self.get_files_in_current_directory()
        bookmark = self.get_current_bookmark()
        for file in files:
            self.set_current_file(file)
            files_info_str += f"{file}: {self.current_file.get('description', 'No description')}\n"
        self.set_bookmark(bookmark)
        return files_info_str

    def get_all_subdirectory_info_in_current_directory(self):
        subdirectory_info_str = ''
        subdirectories = self.get_subdirectories_in_current_directory()
        bookmark = self.get_current_bookmark()
        for subdirectory in subdirectories:
            self.set_current_directory(subdirectory)
            data = self._navigate_to_current_directory()
            subdirectory_info_str += f"{self.current_directory.name}: {data.get('directory_description', 'No description')}\n"
            self.set_bookmark(bookmark)
        return subdirectory_info_str

    def _navigate_to_current_directory(self):
        data = self.summary_data

        relative_path = self.current_directory.relative_to(self.root_directory)

        # Loop through each part of the relative path
        for parent in reversed(Path(relative_path).parents):
            sub_dir = parent.name
            if sub_dir:
                data = data['subdirectories'].get(sub_dir, {})

        # Finally, navigate to the base of the relative path (if it exists)
        base = Path(relative_path).name
        if base:
            data = data['subdirectories'].get(base, {})

        return data

    def get_directory_summary(self, summary_data=None):
        if not summary_data:
            summary_data = self.summary_data
        summary_data_new = {'directory_description': summary_data['directory_description'], "files": [], 'subdirectories': {}}
        for file in summary_data['files']:
            new_file = {}
            new_file['name'] = file["name"]
            all_entities = self.get_all_entities(file["entities"])
            new_file['entities'] = [{key: value for key, value in entity.items() if key in REQUIRED_ENTITY_FIELDS} for entity in all_entities]
            summary_data_new["files"].append(new_file)
        subdirectories_new = {subdir_name: self.get_directory_summary(subdir_data) for subdir_name, subdir_data
                              in summary_data['subdirectories'].items()}
        summary_data_new['subdirectories'] = subdirectories_new
        return summary_data_new

    def get_code_from_path(self, start_line=None, code_for_prompt=None, show_nested=True, include_line_number=False,
                           file_path=None, imports=None, declarations=None, entity=None, file_type=None,
                           file_end_line=None):
        code_for_hash = code_for_prompt
        if start_line:
            imports_and_declarations_code = self.get_imports_and_declarations_in_current_file(
                file_path=file_path, imports=imports, declarations=declarations,
                include_line_number=include_line_number, file_end_line=file_end_line)
            if not code_for_prompt:
                if entity:
                    self.current_entity = entity
                    entity_code, entity_code_for_prompt = self.get_entity_code(file_path=file_path, reduced=not show_nested,
                                                                               include_line_number=include_line_number, file_type=file_type,
                                                                               file_end_line=file_end_line)
                    code_for_prompt = entity_code_for_prompt
                    code_for_hash = entity_code
                else:
                    entity = self.get_entities_with_start_line(start_line, self.current_file["entities"])
                    entity_lines = [[{"name": entity["name"], "start_line": entity["start_line"]}]]
                    code_for_prompt, code_for_hash = "", ""
                    for entity_info in entity_lines:
                        self.set_bookmark(entity_info)
                        entity_code, entity_code_for_prompt = self.get_entity_code(reduced=not show_nested, include_line_number=include_line_number)
                        code_for_prompt += entity_code_for_prompt
                        code_for_hash += entity_code
            final_code = "# For context: Imports and declarations from the file\n"
            final_code += f"{imports_and_declarations_code}\n"
            final_code += "# Start: Code snippet of interest\n"
            final_code += code_for_prompt + "\n"
            final_code += "\n# End: Code snippet of interest\n"
        else:
            final_code = self.read_code_lines()
            code_for_hash = final_code
        return final_code, code_for_hash

    def get_entities_with_start_line(self, start_line, entities):
        entities = [entity for entity in entities
                    if (entity["start_line"] <= start_line <= entity["end_line"])]
        if len(entities) > 0:
            entity = entities[0]
        else:
            return None
        if entity['nested']:
            nested_entity = self.get_entities_with_start_line(start_line, entity['nested'])
            if nested_entity:
                entity = nested_entity
        return entity

    def get_function_names_from_path(self, start_line=None, show_nested=True):
        if start_line:
            entity = self.get_entities_with_start_line(start_line, self.current_file["entities"])
            file_entities = [{"name": entity["name"], "start_line": entity["start_line"]}]

            entities = self._get_entities_names(file_entities, show_nested)
        else:
            entities = [e[0]['name'] for e in self.get_entities_in_current_file()]
        return entities

    def _get_entities_names(self, file_entities, show_nested):
        entities = []
        for e in file_entities:
            entities.append(e["name"])
            if show_nested and e['nested']:
                self._get_entities_names(e['nested'], show_nested)
        return entities

    def __getstate__(self):
        # Copy the object's dictionary
        state = self.__dict__.copy()
        # Remove the yaml_lock attribute, and any other non-serializable attributes
        del state['yaml_lock']
        return state

    def __setstate__(self, state):
        # Re-create the yaml_lock attribute, and any other non-serializable attributes
        self.yaml_lock = Lock()
        # Set all other attributes
        for key, value in state.items():
            setattr(self, key, value)


# Example usage
if __name__ == "__main__":
    path_parts = '/Users/darias/PycharmProjects/test_project/main3.py'.split("/")
    directory = "/".join(path_parts[:-1])
    file = path_parts[-1]
    summary_yaml = SummaryYAML(directory)
    summary_yaml.set_bookmark([{"directory": Path(directory), "file": file}])
    data = summary_yaml.get_function_names_from_path([11,27])

    # summary_yaml = SummaryYAML(r'/Users/darias/PycharmProjects/test_project')
    # data = summary_yaml.get_directory_summary()
    print(data)

    # summary_yaml = SummaryYAML(r'C:\Users\tamuz\codingAgents\directory_parser\coding_languages\tests')
    # new_path = r"C:\Users\tamuz\Documents\Sample_Projects\pycalc-master"
    # # new_path = r"C:\Users\tamuz\Documents\Commit_Projects\rodradar-app"
    # summary_yaml = SummaryYAML(new_path)
    # summary_yaml.get_subdirectories_in_current_directory()
    # summary_yaml.set_current_file(summary_yaml.get_files_in_current_directory()[3])
    # info_str = summary_yaml.get_all_entities_info_in_current_file()
    # print(info_str)
    # summary_yaml.set_current_entity('MyClass')
    # summary_yaml.get_nested_entities()
    # nested_path = [
    #     {'name': 'MyClass', 'start_line': 27},
    #     {'name': 'NestedClass', 'start_line': 46}
    # ]
    # summary_yaml.set_current_entity(nested_path)
    # summary_yaml = SummaryYAML(PROJECT_ROOT / 'tests', embedding_mode=True)
    # summary_yaml.set_current_file('some/sub/directory', 'example_file.py')
    # summary_yaml.set_current_entity('some_function')
    # summary_yaml.add_field('new_field', 'new_value')
    # embedding = summary_yaml.get_embedding_for_entity('some_function')
    # summary_yaml.save()
