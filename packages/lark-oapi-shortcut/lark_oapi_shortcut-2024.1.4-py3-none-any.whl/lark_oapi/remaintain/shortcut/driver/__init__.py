import dataclasses
from io import BytesIO
from typing import Optional

from typing_extensions import Literal

import lark_oapi.api.drive.v1
from lark_oapi.remaintain.shortcut.compact import FeishuOpenAPICompactSettings
from lark_oapi.remaintain.extra.service.drive_explorer.v2 import (
    Service as ExtraDriverV2Service,
)
from lark_oapi.remaintain.extra.service.drive_explorer.v2 import (
    model as extra_driver_v2_model,
)


class FeishuDriverShortcutOperationError(Exception):
    pass


@dataclasses.dataclass
class FeishuDriverShortcut:
    s: FeishuOpenAPICompactSettings

    extra_driver_v2_service: ExtraDriverV2Service = dataclasses.field(init=False)

    def __post_init__(self):
        conf = self.s.remaintain_extra_config
        self.extra_driver_v2_service = ExtraDriverV2Service(conf)

    def get_self_root_folder_meta(self) -> extra_driver_v2_model.FolderRootMetaResult:
        resp = self.extra_driver_v2_service.folders.root_meta().do()
        if resp.code != 0:
            raise FeishuDriverShortcutOperationError(str(resp))
        return resp.data

    def get_folder_meta(
            self, folder_token: str
    ) -> extra_driver_v2_model.FolderMetaResult:
        resp = (
            self.extra_driver_v2_service.folders.meta()
            .set_folderToken(folder_token)
            .do()
        )
        if resp.code != 0:
            raise FeishuDriverShortcutOperationError(str(resp))
        return resp.data

    def __get_parent_node_by_parent_type(self, pt: str) -> Optional[str]:
        return {
            "doc_image": "doccnFivLCfJfblZjGZtxgabcef",
            "doc_file": "doccnFivLCfJfblZjGZtxgabcef",
            "docx_image": "doxcnHI2QLXas8JryTaUggabcef",
            "docx_file": "doxcnHI2QLXas8JryTaUggabcef",
            "sheet_image": "shtcnb9j0FB9jPxzX5pZqUabcef",
            "sheet_file": "shtcnb9j0FB9jPxzX5pZqUabcef",
            "bitable_image": "bascni70rJDWTKvGNOmGHmabcef",
            "bitable_file": "bascni70rJDWTKvGNOmGHmabcef",
            "ccm_import_open": None,
        }.get(pt)

    def media_upload_all(
            self,
            file_name: str,
            parent_type: Literal[
                "doc_image",
                "sheet_image",
                "doc_file",
                "sheet_file",
                "vc_virtual_background",
                "bitable_image",
                "bitable_file",
                "moments",
                "ccm_import_open",
            ],
            size: int,
            file: BytesIO,
            parent_node: Optional[str] = None,
            extra: Optional[str] = None,
    ) -> lark_oapi.api.drive.v1.UploadAllMediaResponseBody:
        client = self.s.upstream_client
        _parent_node = self.__get_parent_node_by_parent_type(parent_type)
        if parent_node is not None:
            _parent_node = parent_node
        req = (
            lark_oapi.api.drive.v1.UploadAllMediaRequest.builder()
            .request_body(
                lark_oapi.api.drive.v1.UploadAllMediaRequestBody()
                .builder()
                .file_name(file_name)
                .parent_type(parent_type)
                .parent_node(_parent_node)
                .size(size)
                .extra(extra)
                .file(file)
                .build()
            )
            .build()
        )
        resp = client.drive.v1.media.upload_all(req)
        if not resp.success() or not resp.data:
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data

    def slice_media_upload_prepare(
            self,
            file_name: str,
            parent_type: Literal[
                "doc_image",
                "sheet_image",
                "doc_file",
                "sheet_file",
                "vc_virtual_background",
                "bitable_image",
                "bitable_file",
                "moments",
                "ccm_import_open",
            ],
            size: int,
            parent_node: Optional[str] = None,
            extra: Optional[str] = None,
    ) -> lark_oapi.api.drive.v1.UploadPrepareMediaResponseBody:
        client = self.s.upstream_client
        _parent_node = self.__get_parent_node_by_parent_type(parent_type)
        if parent_node is not None:
            _parent_node = parent_node
        req = (
            lark_oapi.api.drive.v1.UploadPrepareMediaRequest.builder()
            .request_body(
                lark_oapi.api.drive.v1.MediaUploadInfo()
                .builder()
                .file_name(file_name)
                .parent_type(parent_type)
                .parent_node(_parent_node)
                .size(size)
                .extra(extra)
                .build()
            )
            .build()
        )
        resp = client.drive.v1.media.upload_prepare(req)
        if not resp.success() or not resp.data or not resp.data.upload_id:
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data

    def slice_media_upload_part(
            self,
            upload_id: str,
            size: int,
            chunked_file: BytesIO,
            seq: int = 0,
            checksum: Optional[str] = None,
    ):
        client = self.s.upstream_client
        req = (
            lark_oapi.api.drive.v1.UploadPartMediaRequest.builder()
            .request_body(
                lark_oapi.api.drive.v1.UploadPartMediaRequestBody()
                .builder()
                .upload_id(upload_id)
                .seq(seq)
                .size(size)
                .checksum(checksum)
                .file(chunked_file)
                .build()
            )
            .build()
        )
        resp = client.drive.v1.media.upload_part(req)
        if not resp.success():
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )

    def slice_media_upload_finish(
            self,
            upload_id: str,
            block_num: int,
    ) -> lark_oapi.api.drive.v1.UploadFinishMediaResponseBody:
        client = self.s.upstream_client
        req = (
            lark_oapi.api.drive.v1.UploadFinishMediaRequest.builder()
            .request_body(
                lark_oapi.api.drive.v1.UploadFinishMediaRequestBody()
                .builder()
                .upload_id(upload_id)
                .block_num(block_num)
                .build()
            )
            .build()
        )
        resp = client.drive.v1.media.upload_finish(req)
        if not resp.success() and not resp.data or not resp.data.file_token:
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data

    def __create_import_task_check_params(
            self,
            file_extension,
            type_,
    ):
        check_failed = False
        if type_ == "docx":
            if file_extension not in {
                "docx",
                "doc",
                "txt",
                "md",
                "mark",
                "markdown",
                "html",
            }:
                check_failed = True
        elif type_ == "sheet":
            if file_extension not in {
                "xlsx",
                "xls",
                "csv",
            }:
                check_failed = True
        elif type_ == "bitable":
            if file_extension not in {
                "xlsx",
                "csv",
            }:
                check_failed = True
        elif type_ == "doc":
            if file_extension not in {
                "docx",
                "doc",
                "txt",
                "md",
                "mark",
                "markdown",
            }:
                check_failed = True
        if check_failed:
            err_msg = f"type/file_extension({type}/{file_extension}) not allowed"
            raise FeishuDriverShortcutOperationError(err_msg)

    def create_import_task(
            self,
            file_extension: Literal[
                "docx",
                "doc",
                "txt",
                "md",
                "mark",
                "markdown",
                "html",
                "xlsx",
                "xls",
                "csv",
            ],
            file_token: str,
            type_: Literal[
                "docx",
                "sheet",
                "bitable",
                "doc",
            ],
            file_name: str,
            mount_key: str,
            mount_type: int = 1,  # 挂载到云空间
    ) -> lark_oapi.api.drive.v1.CreateImportTaskResponseBody:
        self.__create_import_task_check_params(
            file_extension=file_extension,
            type_=type_,
        )
        client = self.s.upstream_client
        req = (
            lark_oapi.api.drive.v1.CreateImportTaskRequest.builder()
            .request_body(
                lark_oapi.api.drive.v1.ImportTask()
                .builder()
                .file_extension(file_extension)
                .file_token(file_token)
                .type(type_)
                .file_name(file_name)
                .point(
                    lark_oapi.api.drive.v1.ImportTaskMountPoint()
                    .builder()
                    .mount_type(mount_type)
                    .mount_key(mount_key)
                    .build()
                )
                .build()
            )
            .build()
        )
        resp = client.drive.v1.import_task.create(req)
        if not resp.success() or not resp.data:
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data

    def get_import_task(
            self, ticket: str
    ) -> lark_oapi.api.drive.v1.GetImportTaskResponseBody:
        client = self.s.upstream_client
        req = (
            lark_oapi.api.drive.v1.GetImportTaskRequest.builder().ticket(ticket).build()
        )
        resp = client.drive.v1.import_task.get(req)
        if not resp.success() or not resp.data:
            raise FeishuDriverShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data
