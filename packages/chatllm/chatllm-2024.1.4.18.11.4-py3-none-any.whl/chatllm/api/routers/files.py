#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2023/12/29 14:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo

from meutils.pipe import *
from enum import Enum
from minio import Minio
from openai._types import FileTypes
from openai.types.file_object import FileObject
from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request

router = APIRouter()


class Purpose(str, Enum):
    assistants = "assistants"
    fine_tune = "fine-tune"


def get_minio_client():
    return Minio(
        endpoint=os.getenv('MINIO_ENDPOINT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False)


OPENAI_BUCKET = os.getenv('OPENAI_BUCKET', 'bname')


@router.get("/files/{file_id}")
async def get_files(
    file_id: str,
    client=Depends(get_minio_client)
):  # todo: 返回url
    try:
        response = client.get_object(OPENAI_BUCKET, file_id)
        data = response.read()
        response.close()
        response.release_conn()

        return FileObject(
            id=file_id,
            bytes=len(data),
            created_at=int(time.time()),
            filename=file_id,
            object='file',
            purpose='assistants',
            status='uploaded',
            # status_details=None,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")


@router.post("/files")
async def upload_files(
    file: UploadFile = File(...),
    purpose: Purpose = Form(...),
    client=Depends(get_minio_client)
    # a=Form(...)
):
    if purpose == Purpose.fine_tune:
        # 对于微调，验证上传文件的格式
        content = await file.read()
        try:
            lines = content.decode().split("\n")
            for line in lines:
                record = json.loads(line)
                if "prompt" not in record or "completion" not in record:
                    raise ValueError("Invalid format")
        except:
            raise HTTPException(status_code=400, detail="Invalid file format for fine-tuning")
    elif purpose == Purpose.assistants:
        # 对于助手和消息，你可能需要进行不同的处理
        # todo: 直接解析到es【后面支持队列】

        client.put_object(OPENAI_BUCKET, file.filename, data=file.file, length=file.size)
        client.close()

        return FileObject(
            # id=f"file-{uuid.uuid4()}",
            id=f"{file.filename}",

            bytes=file.size,
            created_at=int(time.time()),
            filename=file.filename,
            object='file',
            purpose='assistants',
            status='uploaded',
            # status_details=None,
        )


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    VERSION_PREFIX = '/v1'

    app = App()
    app.include_router(router, VERSION_PREFIX)
    app.run(port=9000)
