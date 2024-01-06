import os
import subprocess
import tempfile

import pytest

# COLLECT ALL THE INPUT IMAGE FILES.
# We assume that all the files in the `tests/test_data` directory are bitmaps
# whose conversion we wish to test. This relative path means the tests must
# be run from the root of the repository.
TEST_BITMAP_DIRECTORY_PATH = "tests/test_data"
input_bitmap_paths = [os.path.join(TEST_BITMAP_DIRECTORY_PATH, filename) for filename in os.listdir(TEST_BITMAP_DIRECTORY_PATH)]

# There must be available space for temporary file(s).
@pytest.mark.parametrize("input_file_path", input_bitmap_paths)
def test_pypix2svg(input_file_path):
    # CREATE A TEMPORARY FILE TO HOLD THE SVG.
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".svg") as tmp_file:
        expected_output_svg_filepath = tmp_file.name

    try:
        # RUN THE PYPIX2SVG SCRIPT.
        # We shell out rather than just calling the function from Python to make
        # sure that the script entry point is installed correctly too.
        command = ["pypix2svg", input_file_path, '--output', expected_output_svg_filepath]
        result = subprocess.run(command, capture_output = True, text = True)

        # VERIFY THE SCRIPT RAN SUCCESSFULLY.
        if (result.returncode != 0):
            raise AssertionError(
                f'Received a nonzero exit code when running `pypix2svg` from command line!'
                f'\nstdout: {result.stdout}'
                f'\n\nstderr: {result.stderr}')

        # VERIFY THE SVG FILE WAS CREATED.
        # Right now we just make sure the conversion completed without errors;
        # we don't verify the fidelity of the SVG to the original.
        assert os.path.isfile(expected_output_svg_filepath), f"SVG file not created for {input_file_path}"
    finally:
        # DELETE THE TEMPORARY FILE.
        os.remove(expected_output_svg_filepath)
