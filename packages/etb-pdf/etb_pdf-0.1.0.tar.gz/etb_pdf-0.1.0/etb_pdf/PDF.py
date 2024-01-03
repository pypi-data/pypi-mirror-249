from typing import Any
from PyPDF2 import PdfReader, PdfWriter


class Pdf:
    '''class for filling out PDF forms'''

    def __init__(self, template_file_path: str, output_dir: str = None):
        self.reader = PdfReader(template_file_path)
        # print(self.reader.get_form_text_fields())

        if output_dir is not None:
            self.output_dir = output_dir
        else:
            self.output_dir = ''


    def write(self, rows: list[dict[str, Any]] = None, map: dict[str, Any] = None, 
              naming: dict[str, str] = None):
        '''check the README for more info'''

        if map is not None:
            assert all(value in row for value in map.values() for row in rows)
            data = [{key : row[value] for key, value in map.items()} for row in rows]

        else:
            data = rows

        static_name = naming.get('static_name', '')
        dynamic_name_key = naming.get('dynamic_name_key', '')

        for row in data:
            # print(row)
            writer = PdfWriter()
            page = self.reader.pages[0]

            writer.add_page(page)

            writer.update_page_form_field_values(
                writer.pages[0], row
            )

            output_file_name = f"{self.output_dir}{static_name}_{row.get(dynamic_name_key, '')}.pdf"
            # print(output_file_name)

            with open(output_file_name, "wb") as output_stream:
                writer.write(output_stream)