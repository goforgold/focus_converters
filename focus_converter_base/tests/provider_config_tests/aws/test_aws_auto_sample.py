import os
import pathlib
import tempfile
import unittest

from focus_converter.converter import FocusConverter
from focus_converter.data_loaders.data_loader import DataFormats
from focus_converter.utils.profiler import Profiler
from tests.provider_config_tests.aws import csv_aws_generator



class TestAutoGeneratedAWS(unittest.TestCase):

    def test_auto_generated_dataset(self):
        generator = csv_aws_generator.CSVAWSGenerator()
        file_name = "tests/provider_config_tests/aws/auto-generated_1000.csv"
        generator.generate_and_write_csv(1000, file_name)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = pathlib.Path(temp_dir) / "aws_sample_csv_dataset"

            converter = FocusConverter(
                column_prefix=None  # Optional column prefix if needed else can be set to None
            )
            converter.load_provider_conversion_configs()
            converter.load_data(
                data_path=file_name,
                data_format=DataFormats.CSV,
                parquet_data_format=None,
            )
            converter.configure_data_export(
                export_path=export_path,
                export_include_source_columns=False,
            )
            converter.prepare_horizontal_conversion_plan(provider="aws-cur")
            

            self.execute_converter(converter)

            if os.path.exists(file_name):
                os.remove(file_name)

    @Profiler(csv_format=True)    
    def execute_converter(self, converter):
        converter.convert()

