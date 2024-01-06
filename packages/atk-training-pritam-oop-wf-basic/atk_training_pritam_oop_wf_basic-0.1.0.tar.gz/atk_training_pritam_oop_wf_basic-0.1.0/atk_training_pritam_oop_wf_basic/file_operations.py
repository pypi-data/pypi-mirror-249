import os
import pathlib
from logging import Logger
import yaml
from importlib.machinery import SourceFileLoader
from inspect import isfunction, getmembers
from typing import Iterator, Optional, List, Dict, Tuple, Callable, Any
from atk_training_pritam_oop_wf_basic.base_clases import BaseFileHandler


class FileHandler(BaseFileHandler):

    def __init__(self, logger: Logger, input_filename: str, yml_path,
                 output_filename: Optional[str] = None):

        # logging
        self.logger = logger
        self.input_filename: str = input_filename
        self.yml_path: str = yml_path
        if output_filename is None:
            base_name, extension = os.path.splitext(self.input_filename)
            self.output_filename = f"{base_name}.processed{extension}"
        else:
            self.output_filename: str = output_filename

    def open_file(self) -> Iterator[str]:
        with open(self.input_filename, 'r') as infile:
            return infile.readlines()

    def write_file(self, processed_lines: Iterator[str]) -> None:
        with open(self.output_filename, 'w') as outfile:
            outfile.writelines(processed_lines)
        outfile.close()

    def load_pipeline_steps(self) -> List[str]:
        if self.yml_path is not None:
            try:
                with open(self.yml_path, 'r') as yaml_file:
                    return yaml.safe_load(yaml_file)['pipeline']
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info(f"Returning empty pipline")
                return []
        else:
            return []

    def load_pipeline_steps_with_arguments(self) -> Tuple[List[str], Dict[str, Dict[str, Dict[str, Any]]]]:
        if self.yml_path is not None:
            try:
                with open(self.yml_path, 'r') as yaml_file:
                    pipeline = yaml.safe_load(yaml_file)['pipeline']
                    function_list = []
                    function_args_dict = {}
                    for step in pipeline:
                        if isinstance(step, dict):
                            # Extract function name and arguments
                            function_name = list(step.keys())[0]   #{'a':1,'b':2}->['a','b']
                            function_args = step[function_name]['kwargs']
                            function_list.append(function_name)
                            function_args_dict[function_name] = function_args
                        else:
                            # Append function name directly
                            function_list.append(step)
                return function_list, function_args_dict
            except TypeError as error:
                self.logger.error(f"error occurred during loading the pipline \nError: {error}")
                self.logger.info(f"Returning empty pipline")
                return [], {}
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info(f"Returning empty pipline")
                return [], {}

        else:
            self.logger.info(f"No pipline specified returning empty pipline ....")
            return [], {}

    def load_files_from_path(self, function_path: str) \
            -> Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:

        """Loads files from a path -- uses glob to list all files and uses SourceFileLoader to load the file."""
        functions_dict: Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]] = {}
        for file in pathlib.Path(function_path).glob('*.py'):
            module_name = os.path.basename(os.path.splitext(file)[0])
            loader = SourceFileLoader(module_name, file.as_posix())
            module = loader.load_module()
            functions = getmembers(module, isfunction)
            for (func_name, func) in functions:
                self.logger.info(f"Adding {func_name} in function lookup ....... ")
                functions_dict[func_name] = func
        return functions_dict
