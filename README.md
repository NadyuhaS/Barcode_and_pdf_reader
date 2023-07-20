# Testing task from ERP-aero

## Test task

> Разработать метод, на вход которого подается PDF файл (сам файл предоставляется во вложении). Нужно прочитать всю возможную информацию из файла и на выходе вернуть в виде словаря.
 Используя этот файл как эталон, разработать механизм, проверяющий входящие pdf-файлы на наличие всех элементов и соответствие структуры (расположение на листе). 
Время выполнения задания 2 календарных дня.

## Code structure

Project solution consist
> - test_data/test_task.pdf - input data
> - requirements.txt - file with library which were used
> - pdf_reader_with_barcode.py - task solution

## Launch

0. before launch:
   1. ```brew install poppler```
   2. ```pip install -r requirements.txt```
2. ```python3 pdf_reader_with_barcode.py```

## Result

```application/json
{
  "page_0": {
    "GRIFFON AVIATION SERVICES LLC": 
    {
      "barcode_info_1": "tst",
      "PN": "tst",
      "SN": "123123",
      "DESCRIPTION": "PART",
      "LOCATION": "111",
      "CONDITION": "FN",
      "RECEIVER#": "9",
      "UOM": "EA",
      "EXP DATE": "13.04.2022",
      "PO": "P101",
      "CERT SOURCE": "wef",
      "REC.DATE": "18.04.2022",
      "MFG": "efwfe",
      "BATCH# ": "1",
      "DOM": "3.04.2022",
      "REMARK": "",
      "LOT# ": "1",
      "TAGGED BY": "1",
      "Qty": "",
      "1NOTES": "inspection notes"
    }
  }
}
```
