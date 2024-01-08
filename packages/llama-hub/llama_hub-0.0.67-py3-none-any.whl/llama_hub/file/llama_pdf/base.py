import httpx
import mimetypes
import requests
import time
from enum import Enum
from typing import List

from llama_index.bridge.pydantic import Field
from llama_index.readers.base import BasePydanticReader
from llama_index.schema import Document


class ParsingMode(str, Enum):
    """The parsing mode for the PDF reader."""
    FAST = "fast"
    WITH_OCR = "withOCR"
    WITH_LLM = "withLLM"
    WITH_OCR_AND_LLM = "withOCRwithLLM"


class ResultType(str, Enum):
    """The result type for the PDF reader."""
    TXT = "txt"
    MD = "md"


class LlamaPDFReader(BasePydanticReader):
    """A smart-reader for PDF files."""
    base_url: str = Field(default="http://51.20.128.156:3000/", description="The base URL of the Llama PDF reader.")
    parse_mode: ParsingMode = Field(default=ParsingMode.FAST, description="The parsing mode for the PDF reader.")
    result_type: ResultType = Field(default=ResultType.TXT, description="The result type for the PDF reader.")
    check_interval: int = Field(default=1, description="The interval in seconds to check if the parsing is done.")
    max_timeout: int = Field(default=60, description="The maximum timeout in seconds to wait for the parsing to finish.")

    def load_data(self, file_path: str, extra_info: dict) -> List[Document]:
        """Load data from the input directory."""
        extra_info = extra_info or {}
        extra_info["file_path"] = file_path

        # load data, set the mime type
        with open(file_path, "rb") as f:
            mime_type = mimetypes.guess_type(file_path)[0]
            files = {'pdf': (f.name, f, mime_type)}
        
        # send the request, start job
        url = f"{self.base_url.strip("/")}parse/{self.mode}"
        headers = {'Content-Type': 'multipart/form-data'}
        response = requests.post(url, headers=headers, files=files)
        if not response.ok:
            raise Exception(f"Failed to parse the PDF file: {response.text}")

        # check the status of the job, return when done
        token = response.json()["token"]
        result_url = f"{self.base_url.strip('/')}/status/{token}"

        start = time.time()
        while True:
            time.sleep(self.check_interval)
            response = requests.get(result_url)
            if response.ok:
                result = response.json()
                if result[self.result_type.value] != False:
                    return [
                        Document(
                            text=result[self.result_type.value],
                            metadata=extra_info,
                        )
                    ]
                    
            if time.time() - start > self.max_timeout:
                raise Exception(f"Timeout while parsing the PDF file: {response.text}")

    async def aload_data(self, file_path: str, extra_info: dict) -> List[Document]:
        """Load data from the input directory."""
        extra_info = extra_info or {}
        extra_info["file_path"] = file_path

        # load data, set the mime type
        with open(file_path, "rb") as f:
            mime_type = mimetypes.guess_type(file_path)[0]
            files = {'pdf': (f.name, f, mime_type)}
        
        # send the request, start job
        url = f"{self.base_url.strip('/')}parse/{self.mode}"
        headers = {'Content-Type': 'multipart/form-data'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, files=files)
            if not response.ok:
                raise Exception(f"Failed to parse the PDF file: {response.text}")

        # check the status of the job, return when done
        token = response.json()["token"]
        result_url = f"{self.base_url.strip('/')}/status/{token}"

        start = time.time()
        while True:
            time.sleep(self.check_interval)
            async with httpx.AsyncClient() as client:
                response = await client.get(result_url)
                if response.ok:
                    result = response.json()
                    if result[self.result_type.value] != False:
                        return [
                            Document(
                                text=result[self.result_type.value],
                                metadata=extra_info,
                            )
                        ]
                        
                if time.time() - start > self.max_timeout:
                    raise Exception(f"Timeout while parsing the PDF file: {response.text}")
