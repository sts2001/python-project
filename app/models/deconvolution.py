from pydantic import BaseModel


class DeconvolutionInputData(BaseModel):
    base64_img: str


class DeconvolutionOutputData(BaseModel):
    job_id: int
    result_id: int
    base64_img: str


class WatchResult(BaseModel):
    result_id: int


class Results(BaseModel):
    ids: list[int]
