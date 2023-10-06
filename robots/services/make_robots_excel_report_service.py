from datetime import datetime
import io
from string import ascii_uppercase
from typing import Iterable, Union

import openpyxl
from openpyxl.styles import Font, Border, Side
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook

from robots.services import DATETIME_FILE_FORMAT, ADDITIONAL_COLUMN_WIDTH


class MakeExcelReportService:

    def __init__(
            self, robots: Iterable[dict], headers: list[str]) -> None:
        self._columns = self._get_column_names(headers)
        self._headers = headers
        self._robots = robots

    def _bold_cells(self, worksheet: Worksheet) -> None:
        font_bold = Font(bold=True)
        for row in worksheet:
            for cell in row:
                cell.font = font_bold

    def _bordered_cells(self, worksheet: Worksheet) -> None:
        bottom_border = Border(
            left=Side('thin'),
            right=Side('thin'),
            top=Side('thin'),
            bottom=Side('thin')
        )
        for row in worksheet:
            for cell in row:
                cell.border = bottom_border

    def _get_data(self, workbook: Workbook) -> bytes:
        with io.BytesIO() as buffer:
            workbook.save(buffer)
            data = buffer.getvalue()
        return data

    def _get_column_names(self, headers: list[str]) -> list:
        column_names = []
        for i in range(len(headers)):
            column_names.append(ascii_uppercase[i])
        return column_names

    def _load_row_to_excel(
            self, robots: Union[list, tuple], worksheet: Worksheet) -> None:
        worksheet.append(robots)

    def _set_column_width(self, worksheet: Worksheet) -> None:
        for i in range(len(self._headers)):
            worksheet.column_dimensions[self._columns[i]].width = len(
                self._headers[i]) + ADDITIONAL_COLUMN_WIDTH

    def _set_headers(self, worksheet: Worksheet) -> None:
        worksheet.append(self._headers)

    def generate_filename(
            self, filename: str, extension: str = '.xlsx') -> str:
        return datetime.now().strftime(
            DATETIME_FILE_FORMAT) + filename + extension


class MakeExcelRobotsSummaryService(MakeExcelReportService):

    def _set_styled_headers(self, worksheet: Worksheet) -> None:
        self._set_headers(worksheet)
        self._bold_cells(worksheet)
        self._bordered_cells(worksheet)
        self._set_column_width(worksheet)

    def create_report(self) -> bytes:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        model = ''
        first_sheet = True
        for robot in self._robots:
            if first_sheet:
                first_sheet = False
                model = robot.get('model')
                worksheet.title = model
                self._set_styled_headers(worksheet)
            if robot.get('model') != model:
                model = robot.get('model')
                worksheet = workbook.create_sheet()
                worksheet.title = model
                self._set_styled_headers(worksheet)
            self._load_row_to_excel(list(robot.values()), worksheet)
        data = self._get_data(workbook)
        workbook.close()
        return data
