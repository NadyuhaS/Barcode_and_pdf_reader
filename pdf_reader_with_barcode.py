import PyPDF2
import cv2
from pdf2image import convert_from_path
from zxingcpp import read_barcodes, Position


class Barcode:
    def __init__(self, recognized_text: str, recognized_position: Position):
        self.text = recognized_text
        self.position = recognized_position

    def get_text(self) -> str:
        return self.text

    def get_height(self, point: str = 'min') -> int:
        return max(self.position.bottom_left.y, self.position.top_left.y) if point == 'max' else min(
            self.position.bottom_left.y, self.position.top_left.y)

    def get_width(self, point: str = 'min') -> int:
        return max(self.position.bottom_left.x, self.position.bottom_right.x) if point == 'max' else min(
            self.position.bottom_left.x, self.position.bottom_right.x)


class Image:
    def __init__(self, image_name: str):
        self.image = cv2.imread(image_name)
        self.image_path = image_name

    '''
    Get information about images barcode
    '''
    def get_barcodes(self) -> list:
        return [Barcode(recognized_text=barcode.text, recognized_position=barcode.position) for barcode in
                read_barcodes(self.image)]

    def get_height(self) -> int:
        return self.image.shape[0]

    def get_width(self) -> int:
        return self.image.shape[1]

    def get_image_path(self):
        return self.image_path.split('/')[-1]


class PDF:
    def __init__(self, pdf_filename: str):
        self.pdf_file_name = pdf_filename
        self.pdf_file = PyPDF2.PdfReader(open(pdf_filename, 'rb'))

    '''
    Convert pdf file to images 
    '''
    def convert_pdf_to_png(self, folder_path: str = '') -> list:
        converted_file = convert_from_path(self.pdf_file_name, 500)
        images = []
        for count, image in enumerate(converted_file):
            file_path = f'{folder_path}/{count}.png' if folder_path else f'{count}.png'
            image.save(file_path, 'PNG')
            images.append(Image(image_name=file_path))
        return images

    def get_page_count(self) -> int:
        return len(self.pdf_file.pages)

    '''
    Check barcode position
    '''
    def check_barcode_position(self, barcode: Barcode, image_height: int, image_width: int,
                               x_left_boundary_percent: int = 0,
                               x_right_boundary_percent: int = 100,
                               y_top_boundary_percent: int = 0,
                               y_bottom_boundary_percent: int = 100) -> bool:
        return True if barcode.get_width(point='min') / image_width * 100 >= x_left_boundary_percent \
                       and barcode.get_width(point='max') / image_width * 100 <= x_right_boundary_percent \
                       and barcode.get_height(point='min') / image_height * 100 >= y_top_boundary_percent \
                       and barcode.get_height(point='max') / image_height * 100 <= y_bottom_boundary_percent else False

    def get_text(self) -> dict:
        result = {}
        folder_path = 'test_data'
        images = self.convert_pdf_to_png(folder_path=folder_path)
        for i, page in enumerate(self.pdf_file.pages):
            image = list(filter(lambda image: image.get_image_path() == f'{i}.png', images))[0]
            page_text = page.extract_text()
            result.update({f'page_{i}': self.format_text_to_dict(page_text=page_text, image=image)})
        return result

    '''
    Convert recognized text from pdf file to dictionary format
    '''
    def format_text_to_dict(self, page_text: str, image: Image) -> dict:
        header = page_text[:page_text.find(':')].split('\n')[0]
        page_text = page_text.replace(header + '\n', '')
        result = {}
        for i, barcode in enumerate(image.get_barcodes()):
            if self.check_barcode_position(barcode=barcode, image_height=image.get_height(),
                                           image_width=image.get_width(), y_bottom_boundary_percent=35):
                result.update({f'barcode_info_{i + 1}': barcode.get_text()})
        lines = page_text.splitlines()
        for i, data_line in enumerate(lines):
            while data_line.count(':') > 0:
                key = data_line[: data_line.find(':')]
                if len(key + ':') == len(data_line) or len(key + ': ') == len(data_line):
                    data_line += lines.pop(i + 1)
                data_line = data_line.replace(key + ':', '').strip()
                value = data_line[: data_line.find(' ')] if data_line.count(':') > 0 else data_line
                if (data_line.find(':') - len(value)) <= 1 and data_line.find(':') - len(value) >= 0:
                    value = ''
                data_line = data_line.replace(value, '').strip()
                result.update({key: value})
        for i, barcode in enumerate(image.get_barcodes()):
            if self.check_barcode_position(barcode=barcode, image_height=image.get_height(),
                                           image_width=image.get_width(), y_top_boundary_percent=35):
                result.update({f'TAGGED BY': barcode.get_text()})
        return {header: result}


if __name__ == '__main__':
    pdf_file = PDF(pdf_filename='test_data/test_task.pdf')
    print(pdf_file.get_text())
