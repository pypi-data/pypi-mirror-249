"""
api.py

MIT Licence

FastPDF Service/Fast Track Technologies
"""

import requests
import json
import mimetypes
import magic
import os
import zipfile

from typing import Union
from io import BytesIO


from dataclasses import asdict

from .exceptions import PDFException
from .models import RenderOptions, Template, StyleFile, ImageFile


def _raise_for_status(response):
    if not response.ok:
        raise PDFException(response)
        
        
def _read_file(file: Union[str, BytesIO, bytes]) -> tuple:
    filename=""
    # If the input is a string, it's treated as a file path
    if isinstance(file, str):
        file_path = file
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
        content_type = magic.from_buffer(file_content, mime=True)

    # If the input is a BytesIO, get the value
    elif isinstance(file, BytesIO):
        #file.seek(0)
        file_content = file.read()
        content_type = magic.from_buffer(file_content, mime=True)
        
    # If the input is bytes, just use it directly
    elif isinstance(file, bytes):
        file_content = file
        content_type = magic.from_buffer(file_content, mime=True)

    else:
        raise ValueError(f"Expected str, BytesIO, or bytes. Unsupported file type: {type(file)}")

    return (filename, file_content, content_type)


def _asdict_skip_none(data):
    return {k: v for k, v in asdict(data).items() if v is not None}


def _parse_dataclass(_obj, _obj_type):
     _dict_obj = {}
     if _obj is not None:
        if isinstance(_obj, _obj_type):
           _dict_obj = _asdict_skip_none(_obj)
        else:
           _dict_obj = _obj   
     return _dict_obj
     
     
def _parse_render_data_obj(_obj):
    if isinstance(_obj, dict):
       return _obj
    if isinstance(_obj, str):
       with open(_obj, 'rb') as f:
            file_content = f.read()
       return json.loads(file_content)
    raise ValueError(f'Expected dict or str (file path). Unsupported render data type: {type(file)}')
    
def _parse_render_data_list(_obj):
    if isinstance(_obj, list):
       return _obj
    if isinstance(_obj, str):
       with open(_obj, 'rb') as f:
            file_content = f.read()
       return json.loads(file_content)
    raise ValueError(f'Expected list or str (file path). Unsupported render data type: {type(file)}')
     
     
class PDFClient:
    def __init__(self, api_key: str,
                 base_url: str ="https://data.fastpdfservice.com",
                 api_version: str = "v1"):
        self.api_version = api_version
        self.base_url = "{}/{}".format(base_url, api_version)
        self.api_key = api_key
        self.headers = {'Authorization': self.api_key}
        self.supported_image_formats = [
            'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico', 'pdf', 
            'psd', 'ai', 'eps', 'cr2', 'nef', 'sr2', 'orf', 'rw2', 'dng', 
            'arw', 'heic'
        ]

    def validate_token(self) -> bool:
        """
        Validate the API token.

        :return: True if the token is valid, False otherwise.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            is_valid = client.validate_token()
        """
        response = requests.get(
             url=f"{self.base_url}/token",
             headers=self.headers
        )
        _raise_for_status(response)
        return response.status_code == 200


    def split(self, file: Union[str, BytesIO, bytes], splits: list[int]) -> bytes:
        """
        Split a PDF file at the given pages.

        :param file: Path to the file or file-like object of the PDF to split.
        :param splits: List of page numbers where to split the file.
        :return: Content of the splitted PDF files as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            splitted_pdf_content = client.split('path/to/your.pdf', [3, 6])
        """
        files = {'file':_read_file(file)}
        data = {'splits': json.dumps(splits)}
        response = requests.post(
             url=f"{self.base_url}/pdf/split",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content


    def split_zip(self, file: Union[str, BytesIO, bytes], splits: list[list[int]]) -> bytes:
        """
        Split a PDF file at the given pages and return a zip file containing the split files.

        :param file: Path to the file or file-like object of the PDF to split.
        :param splits: List of page ranges where to split the file.
        :return: Content of the zip file as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            zip_content = client.split_zip('path/to/your.pdf', [[1, 3], [4, 6]])
        """
        files = {'file':_read_file(file)}
        data = {'splits': json.dumps(splits)}
        response = requests.post(
             url=f"{self.base_url}/pdf/split-zip",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content

    def extract(self, zip_bytes: bytes, output_path: str = None) -> None:
        if output_path is None:
            files = []
            with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_ref:
                for name in zip_ref.namelist():
                    with zip_ref.open(name) as f:
                        file_content = f.read()
                    files.append(file_content)
            return files

        with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_ref:
            zip_ref.extractall(output_path)


    def save(self, content, file_path: str = None):
        """
        Save the given FastPDF response to a file or return as a BytesIO object.

        :param content: Content to save.
        :param file_path: (Optional) Path to the file where to save the content. If not provided, returns a BytesIO object.
        :return: BytesIO object if file_path is not provided, None otherwise.

        Example usage::

            client = PDFClient('your-api-key')
            pdf_content = client.url_to_pdf('https://www.example.com')

            # Save to file
            client.save(pdf_content, 'path/to/save/your.pdf')

            # Get as BytesIO
            content_io = client.save(pdf_content)
        """
        if file_path:
            with open(file_path, 'wb') as fd:
                fd.write(content)
        else:
            return BytesIO(content)
        
        
    def edit_metadata(self, file: Union[str, BytesIO, bytes], metadata: dict[str, str]) -> bytes:
        """
        Edit the metadata of a PDF file.

        :param file: Path to the file or file-like object of the PDF to edit.
        :param metadata: Metadata to set in the PDF file.
        :return: Content of the PDF file with the new metadata as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            pdf_content_with_new_metadata = client.edit_metadata('path/to/your.pdf', {'Title': 'New Title', 'Author': 'New Author'})
        """
        files = {'file':_read_file(file)}
        data = {'metadata': json.dumps(metadata)}
        response = requests.post(
             url=f"{self.base_url}/pdf/metadata",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content
        
        
    def merge(self, file_paths: list[Union[str, BytesIO, bytes]]) -> bytes:
        """
        Merge multiple PDF files into one.

        :param file_paths: List of file paths or file-like objects of the PDFs to merge.
        :return: Content of the merged PDF file as bytes.

        Raises ValueError if less than 2 or more than 100 files are given.
        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            merged_pdf_content = client.merge(['path/to/first.pdf', 'path/to/second.pdf'])
        """

        if len(file_paths) < 2:
            raise ValueError('You need at least 2 files in order to merge.')
        if len(file_paths) > 10:
            raise ValueError('You can merge a maximum of 100 files at once.')

        files = {}
        for i, f in enumerate(file_paths):
            files['file'+str(i)] = _read_file(f)
        
        response = requests.post(
            url=f"{self.base_url}/pdf/merge",
            headers=self.headers,
            files=files,
        )
        
        _raise_for_status(response)
        return response.content
        
        
    def to_image(self, file: Union[str, BytesIO, bytes], output_format: str) -> bytes:
        """
        Convert a PDF file to an image.
 
        :param file: Path to the file or file-like object of the PDF to convert.
        :param output_format: Format of the output image. Must be one of the supported formats.
        :return: Content of the image as bytes.

        Raises ValueError if an unsupported output format is given.
        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            image_content = client.to_image('path/to/your.pdf', 'png')
            client.save("path/to/output.png", image_content)
        """
        output_format = output_format.lower()
        if output_format.lower() not in self.supported_image_formats:
            raise ValueError(f'Unsupported output format. Must be one of: {self.supported_image_formats}')

        files = {'file':_read_file(file)}
        response = requests.post(
             url=f"{self.base_url}/pdf/image/{output_format}",
             headers=self.headers,
             files=files,
        )
        
        _raise_for_status(response)
        return response.content
        

    def compress(self, file: Union[str, BytesIO, bytes], options:dict=None) -> bytes:
        """
        Compress a PDF file.

        :param file: Path to the file or file-like object of the PDF to compress.
        :param options: Optional compression options.
        :return: Content of the compressed PDF file as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            compressed_pdf_content = client.compress('path/to/your.pdf', options={'quality': 'high'})
        """
        files = {'file':_read_file(file)}
        data = {'options': json.dumps(options) if options else None} 
        response = requests.post(
             url=f"{self.base_url}/pdf/compress",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content
        
    
    def encrypt(self, file: Union[str, BytesIO, bytes], password: str) -> bytes:
       """
       Encrypt a PDF file with a password.

       :param file: Path to the file or file-like object of the PDF to encrypt.
       :param password: Password to encrypt the PDF.
       :return: Content of the encrypted PDF file as bytes.

       Raises PDFException if the request to the FastPDF service fails.

       Example usage::

           client = PDFClient('your-api-key')
           encrypted_pdf_content = client.encrypt('path/to/your.pdf', password='your_password')
       """
       files = {'file': _read_file(file)}
       options = {'encrypt_password': password}
       data = {'options': json.dumps(options)}
       response = requests.post(
           url=f"{self.base_url}/pdf/encrypt",
           headers=self.headers,
           files=files,
           data=data
       )
       _raise_for_status(response)
       return response.content

        
    def url_to_pdf(self, url: str) -> bytes:
        """
        Convert a web page to a PDF file.

        :param url: URL of the web page to convert.
        :return: Content of the resulting PDF file as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage:
            client = PDFClient('your-api-key')
            pdf_content = client.url_to_pdf('https://www.example.com')
        """
        data = {'url':url}
        response = requests.post(
            url=f"{self.base_url}/pdf/url",
            headers=self.headers,
            data=data
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_barcode(self, data: str, barcode_format: str = 'code128', 
                        render_options: RenderOptions=None) -> bytes:
        """
        Renders a barcode PDF based on the provided data and barcode format.

        :param data: The data to encode in the barcode.
        :param barcode_format: The format of the barcode, default is "code128".
            Refer to documentation for the list of available formats.
        :param render_options: The rendering options as a RenderOptions object.
        :return: The rendered barcode PDF in bytes.

        Raises ValueError if the provided barcode format is not supported.
        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            barcode = client.render_barcodes('1234567890')
            client.save(barcode, "path/to/barcode.pdf")
        """
        barcode_format = barcode_format.lower()
        _available_formats = [
            'codabar', 'code128', 'code39', 'ean', 'ean13', 'ean13-guard',
            'ean14', 'ean8', 'ean8-guard', 'gs1', 'gs1_128', 'gtin', 'isbn',
            'isbn10', 'isbn13', 'issn', 'itf', 'jan', 'nw-7', 'pzn', 'upc',
            'upca', 'qr', 'pdf417', 'datamatrix', 'ean5', 'postnet', 'msi'
        ]
        if barcode_format not in _available_formats:
           raise ValueError(f'Invalid barcode type: {barcode_format}')
        
        _render_options_obj = _parse_dataclass(render_options, RenderOptions)
        _data_obj = {'data':data, 'barcode_format': barcode_format}
        
        request_data = {
           "data" : _data_obj, 
           "render_options": _render_options_obj
        }

        response = requests.post(
            url=f"{self.base_url}/render/barcode",
            headers=self.headers,
            json=request_data,
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_image(self, image: Union[str, BytesIO, bytes], render_options: RenderOptions=None) -> bytes:
        """
        Renders an image to PDF.

        :param image: The image to render. Can be a path to the image, BytesIO, or bytes.
        :param render_options: The rendering options as a RenderOptions object.
        :return: The rendered image in bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            rendered_image = client.render_image('path/to/image.png')
            client.save(rendered_image, "path/to/image.pdf")

        """
        _data_obj = {
            "render_options": json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        _files = {  
            'image': _read_file(image)
        }
        
        response = requests.post(
            url=f"{self.base_url}/render/img",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content


    def render_image_from_id(self, image_id: str, render_options: RenderOptions = None) -> bytes:
        """
        Renders an image to PDF based on its id.

        :param image_id: The ID of the image to render.
        :param render_options: The rendering options as a RenderOptions object.
        :return: The rendered image in bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            rendered_image = client.render_image_from_id('image_id')
            client.save(rendered_image, "path/to/image.pdf")

        """
        _data_obj = {
            "render_options": json.dumps(_parse_dataclass(render_options, RenderOptions))
        }

        response = requests.get(
            url=f"{self.base_url}/img/{image_id}",
            headers=self.headers,
            data=_data_obj
        )
        _raise_for_status(response)
        return response.content
        
        
    def get_all_templates(self, limit=None) -> list:
        """
        Retrieves all templates.

        This function makes a GET request to the /template endpoint and retrieves all the templates.
        It optionally accepts a limit parameter to limit the number of templates retrieved.

        :param limit: An optional integer specifying the maximum number of templates to retrieve.
        :return: A list of dictionaries where each dictionary represents a template.

        Raises PDFException if the request fails.

        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        response = requests.get(
            url=f"{self.base_url}/template",
            headers=self.headers,
            params=params,
        )
        _raise_for_status(response)
        return response.json()

    def get_template(template_id) -> dict:
        """
        Retrieves a specific template from the service.

        This function makes a GET request to the /template endpoint with the provided template_id and retrieves the corresponding template.

        :param template_id: A string representing the unique identifier of the template to be retrieved.
        :return: A dictionary representing the retrieved template.

        Raises PDFException if the request fails.

        """
        response = requests.get(
            url=f"{self.base_url}/template/{template_id}",
            headers=self.headers,
        )
        _raise_for_status(response)
        return response.json()

    def add_template(self, file_data: Union[str, BytesIO, bytes], template_data: Template, 
                     header_data: Union[str, BytesIO, bytes] = None,
                     footer_data: Union[str, BytesIO, bytes] = None) -> dict:
        """
        Adds a new template.

        :param file_data: The main file data for the template. This can be a str (filepath), bytes, or BytesIO object.
        :param template_data: An instance of the Template dataclass that holds template data.
        :param header_data: (Optional) The header file data for the template. This can be a str (filepath), bytes, or BytesIO object.
        :param footer_data: (Optional) The footer file data for the template. This can be a str (filepath), bytes, or BytesIO object.
        :return: A dictionary with the response data from the FastPDF service.

        Raises PDFException if the request fails.

        """
        files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
        }
        response = requests.post(
            url=f"{self.base_url}/template",
            headers=self.headers,
            data=_data_obj,
            files=files
        )
        _raise_for_status(response)
        return response.json()
      
      
    def render(self, file_data: Union[str, BytesIO, bytes], template_data: Template = None,
               render_data: Union[dict, str] = {},
               header_data: Union[str, BytesIO, bytes] = None,
               footer_data: Union[str, BytesIO, bytes] = None,
               format_type: str="pdf",
               render_options: RenderOptions=None) -> bytes:
        """
        Renders a document based on the provided data, without prior Template upload.

        :param file_data: The main content file. Can be a path to the file, BytesIO, or bytes.
        :param template_data: The template data as a Template object. If not provided, a default template is used.
        :param render_data: The data to populate the template with. Can be a dict or a JSON string.
        :param header_data: The header content file. Can be a path to the file, BytesIO, or bytes.
        :param footer_data: The footer content file. Can be a path to the file, BytesIO, or bytes.
        :param format_type: The output format of the rendered document, default is "pdf".
        :param render_options: The rendering options as a RenderOptions object.
        :return: The rendered document in bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key'à
            template_data = Template(name="test-tmplt", format="html")
            # Render
            response = client.render('path/to/file.html', template_data, 'path/to/data.json')
            client.save(response, 'path/to/file.pdf')

        """
        if template_data is None:
            template_data = Template(name="fastpdf-document", format="html", title_header_enabled=False)
        format_type = format_type.lower()
        _files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
         'render_data': json.dumps(_parse_render_data_obj(render_data)),
         'render_options': json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_many(self, file_data: Union[str, BytesIO, bytes], template_data: Template = None,
               render_data: Union[list, str] = [{}],
               header_data: Union[str, BytesIO, bytes] = None,
               footer_data: Union[str, BytesIO, bytes] = None,
               format_type: str="pdf",
               render_options: RenderOptions=None) -> bytes:
        """
        Renders multiple documents based on the provided data and template,
        without prior template upload.

        :param file_data: The main content file. Can be a path to the file, BytesIO, or bytes.
        :param template_data: The template data as a Template object. If not provided, a default template is used.
        :param render_data: The list of data to populate the templates with. Can be a list or a JSON string.
        :param header_data: The header content file. Can be a path to the file, BytesIO, or bytes.
        :param footer_data: The footer content file. Can be a path to the file, BytesIO, or bytes.
        :param format_type: The output format of the rendered documents, default is "pdf".
        :param render_options: The rendering options as a RenderOptions object.
        :return: The rendered documents in bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            template_data = Template(name="test-tmplt", format="html")
            response = client.render('path/to/file.html', template_data,  render_data=[data1, data2])
            client.save(response, 'path/to/file.pdf')

        """

        if template_data is None:
            template_data = Template(name="fastpdf-document", format="html", title_header_enabled=False)
        format_type = format_type.lower()
        _files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
         'render_data': json.dumps(_parse_render_data_list(render_data)),
         'render_options': json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/batch",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content
      
        
    def add_stylesheet(self, template_id: str,
                       file_data: Union[str, BytesIO, bytes],
                       template_data: StyleFile) -> dict:
        """
        Adds a stylesheet to a specific template.

        :param template_id: The unique identifier of the template to add the stylesheet to.
        :param file_data: The data of the stylesheet file.
        :param template_data: The data related to the stylesheet.
        :return: The response from the FastPDF service in the form of a dictionary.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            file_data = ...  # filepath str, encoded css string, or BytesIO
            template_data = StyleFile(...)  # fill with your template data
            response = client.add_stylesheet('your-template-id', file_data, template_data)
        """
        _files = {
            'file_data': _read_file(file_data), 
        }
        _data_obj = {
            'template_data': json.dumps(_parse_dataclass(template_data, StyleFile)),
        }
        response = requests.post(
            url=f"{self.base_url}/template/css/{template_id}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.json()
        
    def add_image(self, template_id: str,
                  file_data:  Union[str, BytesIO, bytes],
                  template_data: ImageFile) -> dict:
        """
        Adds an image to a specific template.

        :param template_id: The unique identifier of the template to add the image to.
        :param file_data: The data of the image file.
        :param template_data: The data related to the image.
        :return: The response from the FastPDF service in the form of a dictionary.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::
        
            client = PDFClient('your-api-key')
            file_data = ... # filepath str, encoded css string, or BytesIO
            template_data = ImageFile(...)  # fill with your template data
            response = client.add_image('your-template-id', file_data, template_data)
         
        .. html

        
        """
        _files = {
            'file_data': _read_file(file_data), 
        }
        _data_obj = {
            'template_data': json.dumps(_parse_dataclass(template_data, ImageFile)),
        }
        response = requests.post(
            url=f"{self.base_url}/template/img/{template_id}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.json()


    def delete_template(self, template_id: str) -> bool:
        """
        Deletes a specific template.

        :param template_id: The unique identifier of the template to be deleted.
        :return: True if the deletion was successful, False otherwise.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            success = client.delete_template('your-template-id')
        """
        response = requests.delete(
            url=f"{self.base_url}/template/{template_id}",
            headers=self.headers,
        )
        _raise_for_status(response)
        return response.status_code == 204
        
        
    def render_template(self, template_id: str, 
                        render_data: Union[dict, str],
                        render_options: RenderOptions=None,
                        format_type: str="pdf") -> bytes:
        """
        Renders a template with provided render data and options.

        :param template_id: The unique identifier of the template to be rendered.
        :param render_data: The data required for rendering the template.
        :param render_options: The options for rendering the template.
        :param format_type: The format of the rendered template (default is "pdf").
        :return: The rendered template data as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            render_data = {...}
            render_options = RenderOptions(...)
            rendered_document = client.render_template(your-template-id', render_data, render_options=render_options)
            client.save(rendered_document, "output/path/document.pdf")
        """
        format_type = format_type.lower()
        data = {
         'render_data': json.dumps(_parse_render_data_obj(render_data)),
         'render_options':  json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/{template_id}",
            headers=self.headers,
            data=data,
        )
        _raise_for_status(response)
        return response.content
    
    def render_template_many(self, template_id: str, 
                             render_data: Union[list, str],
                             render_options: RenderOptions=None,
                             format_type: str="pdf") -> bytes:

        """
        Renders a template with provided multiple render data and options.

        :param template_id: The unique identifier of the template to be rendered.
        :param render_data: A list of data required for rendering the template.
        :param render_options: The options for rendering the template.
        :param format_type: The format of the rendered template (default is "pdf").
        :return: The rendered template data as bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            render_data_list = [...]
            render_options = RenderOptions(...)
            rendered_documents_zip = client.render_template_many('your-template-id', render_data_list, render_options=render_options)
            client.save(rendered_documents_zip, "output/path/document.zip")
        """

        format_type = format_type.lower()
        data = {
          'render_data': json.dumps(_parse_render_data_list(render_data)),
          'render_options':  json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/batch/{template_id}",
            headers=self.headers,
            data=data,
        )
        _raise_for_status(response)
        return response.content
              
        
    def delete_stylesheet(self, stylesheet_id: str) -> bool:
        """
        Deletes a stylesheet.

        :param stylesheet_id: The unique identifier of the stylesheet to be deleted.
        :return: True if the deletion was successful, False otherwise.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            success = client.delete_stylesheet('your-stylesheet-id')
        """
        response = requests.delete(
            url=f"{self.base_url}/template/css/{stylesheet_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.status_code == 204


    def get_template_file(self, template_id: str) -> bytes:
        """
        Retrieves the file data of a specific template from the FastPDF service.

        :param template_id: The unique identifier of the template.
        :return: The file data associated with the template as bytes.

        Raises HTTPError if the request to the FastPDF service fails.

        """
        response = requests.get(
            url=f"{self.base_url}/template/file/{template_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.content


    def get_stylesheet(self, stylesheet_id: str) -> bytes:
        """
        Retrieves the file data of a specific stylesheet from the FastPDF service.

        :param stylesheet_id: The unique identifier of the stylesheet.
        :return: The file data associated with the stylesheet as bytes.

        Raises HTTPError if the request to the FastPDF service fails.

        Example usage::

            client = FastPDFClient('your-api-key')
            file_data = client.get_stylesheet('your-stylesheet-id')
            client.save(file_data, 'stylesheet.css')
        """
        response = requests.get(
            url=f"{self.base_url}/template/css/file/{stylesheet_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.content
        
        
    def delete_image(self, image_id: str) -> bool:
        """
        Deletes a specific image from the FastPDF service.

        :param image_id: The unique identifier of the image to be deleted.
        :return: True if the deletion was successful, False otherwise.

        Raises HTTPError if the request to the FastPDF service fails.

        Example usage::

            client = FastPDFClient('your-api-key')
            success = client.delete_image('your-image-id')
        """
        response = requests.delete(
            url=f"{self.base_url}/template/img/{image_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.status_code == 204


    def get_image(self, image_id: str) -> bytes:
        """
        Retrieves the image file associated with a given image ID.

        :param image_id: The unique identifier for the image.
        :return: The image file in bytes.

        Raises PDFException if the request to the FastPDF service fails.

        Example usage::

            client = PDFClient('your-api-key')
            image_file = client.get_image('your-image-id')
        """
        response = requests.get(
            url=f"{self.base_url}/template/img/file/{image_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.content
        
        
    # Convenience functions for each format
    def render_template_to_pdf(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='pdf')

    def render_template_to_docx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='docx')

    def render_template_to_odp(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='odp')

    def render_template_to_ods(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='ods')

    def render_template_to_odt(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='odt')

    def render_template_to_pptx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='pptx')

    def render_template_to_xlx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='xlx')

    def render_template_to_xls(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, format_type='xls')
        
        
        
