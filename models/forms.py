from fastapi import Form, UploadFile, File
from typing import Optional
from dataclasses import dataclass

@dataclass
class BookForm:
    title: str = Form(...)
    author: str = Form(...)
    file: UploadFile = File(...)
    description: Optional[str] = Form(None)

@dataclass
class BookUpdateForm:
    title: str = Form(...)
    author: str = Form(...)
    file: UploadFile = File(None)
    description: Optional[str] = Form(None)
