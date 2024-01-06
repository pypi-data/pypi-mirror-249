from typing import Optional
import typer
import sys
import logging
from logging import Logger
from atk_training_pritam_oop_wf_basic.processing_functions import FunctionRepository
from atk_training_pritam_oop_wf_basic.StreamFunctionRepository import StreamFunctionRepository
from atk_training_pritam_oop_wf_basic.file_operations import FileHandler
from atk_training_pritam_oop_wf_basic.Processor import Processor
from atk_training_pritam_oop_wf_basic.BasicStreamFunctionRepository import BasicStreamFunctionRepository

app = typer.Typer()


@app.command()
def process_file(input_filename: str,  output_filename: Optional[str] = None) -> None:
    # logging
    logger: Logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    fh = FileHandler(logger, input_filename, output_filename)

    repository = FunctionRepository()
    processor = Processor(logger, fh, [repository])

    processor.process(['upper_case', 'remove_stop_words', 'lower_case', 'uk_to_us', 'capitalized'])


stream_app = typer.Typer()


@stream_app.command()
def process_file_stream_pipeline(input_filename: str,
                                 yml_path: str,
                                 additional_function_path: Optional[str] = None,
                                 output_filename: Optional[str] = None) -> None:
    # logging
    logger: Logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # instantiate File handler
    fh: FileHandler = FileHandler(logger, input_filename, yml_path, output_filename)

    # instantiate Function repositories
    stream_repository: StreamFunctionRepository = StreamFunctionRepository()
    extended_stream_repository: BasicStreamFunctionRepository = BasicStreamFunctionRepository()

    # instantiate processor
    processor: Processor = Processor(logger, fh, [stream_repository, extended_stream_repository])

    # call processor
    processor.stream_process(additional_function_path=additional_function_path)


def process_file_stream_v2(input_filename: str, output_filename: Optional[str] = None) -> None:
    fh: FileHandler = FileHandler(input_filename, output_filename)

    stream_repository: StreamFunctionRepository = StreamFunctionRepository()
    extended_stream_repository: BasicStreamFunctionRepository = BasicStreamFunctionRepository()
    processor: Processor = Processor(fh, [stream_repository, extended_stream_repository])
    processor.stream_process(functions=['stream_lower_case', 'coalesce_empty_lines', 'stream_uk_to_us', 'break_lines',
                                        'number_the_lines', 'stream_capitalized'],
                             break_lines={'max_length': 25})


def process_file_stream_v1(input_filename: str, output_filename: Optional[str] = None) -> None:
    fh = FileHandler(input_filename, output_filename)

    stream_repository = StreamFunctionRepository()
    processor = Processor(fh, [stream_repository])
    processor.stream_process(functions=['coalesce_empty_lines', 'break_lines', 'number_the_lines'],
                             break_lines={'max_length': 25})
