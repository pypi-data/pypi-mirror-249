"""DynamoFL local model"""
import shortuuid

from ..file_transfer.upload_v2 import (
    FileUploaderV2,
    MultipartFileUploadResponse,
    ParamsArgsV2,
    UploadedFile,
)
from ..models.model import Model
from ..Request import _Request

try:
    from typing import List, Optional
except ImportError:
    from typing_extensions import List, Optional

CHUNK_SIZE = 1024 * 1024  # 1MB
MODEL_WITH_MULTIPLE_FILES_FLAG = True


class LocalModel(Model):
    """LocalModel"""

    def __init__(self, request, name: str, key: str, model_id: str, config, size: int) -> None:
        self.request = request
        self.size = size
        super().__init__(
            request=request,
            name=name,
            key=key,
            config=config,
            model_type="LOCAL",
            model_id=model_id,
        )

    @staticmethod
    def create_and_upload(
        request: _Request,
        name: str,
        key: Optional[str],
        model_file_path: Optional[str],
        model_file_paths: Optional[List[str]],
        checkpoint_json_file_path: Optional[str],
        architecture: Optional[str],
        config,
        peft_config_path: Optional[str] = None,
    ):
        if MODEL_WITH_MULTIPLE_FILES_FLAG:
            LocalModel.validate_model_file_paths(
                model_file_path=model_file_path,
                model_file_paths=model_file_paths,
                checkpoint_json_file_path=checkpoint_json_file_path,
            )

            model_file_paths = model_file_paths if model_file_paths else []
            if model_file_path:
                model_file_paths.append(model_file_path)

            model_entity_key = shortuuid.uuid() if not key else key
            model_ckpts_keys = []
            model_file_size = 0

            for model_path in model_file_paths:
                uploaded_model_file: UploadedFile = LocalModel.upload_model_file(
                    request=request, key=model_entity_key, model_file_path=model_path
                )
                model_ckpts_keys.append(uploaded_model_file.object_key)
                model_file_size += uploaded_model_file.file_size

            if checkpoint_json_file_path:
                uploaded_model_file: UploadedFile = LocalModel.upload_model_file(
                    request=request, key=model_entity_key, model_file_path=checkpoint_json_file_path
                )
                config["checkpointJsonS3Key"] = uploaded_model_file.object_key

            config["objKeys"] = model_ckpts_keys
            # This acts as a backward compatibility for the old models where model_architecture was
            # provided in the config. It will get overriden if explicitly provided via architecture
            # attribute
            # Question: Can we remove this backward compatibility? (simply have architecture
            # attribute and remove config from sdk create_model method completely as there's no
            # other attribute that API uses from the config)
            if architecture:
                config["model_architecture"] = architecture

        else:
            # TODO: Remove this else block once the model with multiple files is supported
            if (
                model_file_path is None
                or model_file_paths is not None
                or checkpoint_json_file_path is not None
            ):
                raise ValueError(
                    "Validation Error: You need to provide model_file_path and you can't provide "
                    "model_file_paths or checkpoint_json_file_path"
                )
            uploaded_file: UploadedFile = LocalModel.upload_model_file(
                request=request, key=key, model_file_path=model_file_path
            )

            model_entity_key = uploaded_file.entity_key
            config["objKey"] = uploaded_file.object_key
            model_file_size = uploaded_file.file_size

        if peft_config_path:
            config["peftConfigS3Key"] = LocalModel.upload_peft_file(
                request=request, peft_config_path=peft_config_path
            )

        model_id = Model.create_ml_model_and_get_id(
            request=request,
            name=name,
            key=model_entity_key,
            model_type="LOCAL",
            config=config,
            size=model_file_size,
        )

        return LocalModel(
            request=request,
            name=name,
            key=model_entity_key,
            config=config,
            model_id=model_id,
            size=model_file_size,
        )

    @staticmethod
    def validate_model_file_paths(
        model_file_path: Optional[str],
        model_file_paths: Optional[List[str]],
        checkpoint_json_file_path: Optional[str],
    ):
        if model_file_path is None and model_file_paths is None:
            raise ValueError(
                "Validation Error: Either model_file_path or model_file_paths must be provided"
            )

        if model_file_path is not None:
            if model_file_paths is not None or checkpoint_json_file_path is not None:
                raise ValueError(
                    "Validation Error: If model_file_path is provided, "
                    "model_file_paths should not be and checkpoint_json_file_path "
                    "should not be there"
                )

        if model_file_paths is not None:
            if len(model_file_paths) <= 1 or checkpoint_json_file_path is None:
                raise ValueError(
                    "Validation Error: If model_file_paths is provided,"
                    " its size must be > 1 and checkpoint_json_file_path must be "
                    "provided for it"
                )

    @staticmethod
    def upload_peft_file(request: _Request, peft_config_path) -> str:
        response: UploadedFile = LocalModel.upload_model_file(
            request=request, key=None, model_file_path=peft_config_path
        )
        return response.object_key

    @staticmethod
    def upload_model_file(
        request: _Request, key: Optional[str], model_file_path: str
    ) -> UploadedFile:
        def construct_params_v2(params_args: ParamsArgsV2):
            params = {
                "filename": params_args.filename,
                "parts": params_args.parts,
            }
            if key:
                params["key"] = key
            return params

        file_uploader_v2 = FileUploaderV2(request)
        response_v2: MultipartFileUploadResponse = file_uploader_v2.multipart_upload(
            file_path=model_file_path,
            presigned_endpoint_url="/ml-model/multipart-presigned-urls",
            construct_params=construct_params_v2,
        )
        return UploadedFile(
            object_key=response_v2.multipart_upload.obj_key,
            entity_key=response_v2.multipart_upload.entity_key,
            file_size=response_v2.file_metadata.size,
        )
