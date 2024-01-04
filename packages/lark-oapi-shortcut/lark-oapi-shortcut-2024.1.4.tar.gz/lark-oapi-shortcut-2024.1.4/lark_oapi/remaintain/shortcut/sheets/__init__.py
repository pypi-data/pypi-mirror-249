import dataclasses
import datetime
from typing import Any, List, Optional, Sequence, Tuple, Dict

from typing_extensions import Literal

from lark_oapi.api.sheets.v3 import (
    CreateSpreadsheetRequest,
    Spreadsheet,
    FindSpreadsheetSheetRequest,
    Find,
    FindCondition,
    FindReplaceResult,
    QuerySpreadsheetSheetRequest,
    Sheet,
)
from lark_oapi.remaintain.extra.service.drive_permission.v2.api import (
    Service as ExtraDrivePermissionV2Service,
)
from lark_oapi.remaintain.extra.service.drive_permission.v2 import (
    model as extra_drive_permission_v2_model,
)
from lark_oapi.remaintain.extra.service.sheets.v2 import Service as ExtraSheetsV2Service
from lark_oapi.remaintain.extra.service.sheets.v2 import model as extra_sheets_v2_model
from lark_oapi.remaintain.shortcut.compact import FeishuOpenAPICompactSettings
from lark_oapi.remaintain.shortcut.sheets import utils
from lark_oapi.remaintain.shortcut.sheets.models import SheetRange, CellsRange, CellPos
from lark_oapi.remaintain.shortcut.sheets.models import cell_value_support_data_types


class FeishuSheetsShortcutOperationError(Exception):
    pass


@dataclasses.dataclass
class FeishuSheetsShortcut:
    s: FeishuOpenAPICompactSettings

    extra_sheets_v2_service: ExtraSheetsV2Service = dataclasses.field(init=False)
    extra_drive_permission_v2_service: ExtraDrivePermissionV2Service = (
        dataclasses.field(init=False)
    )

    def __post_init__(self):
        conf = self.s.remaintain_extra_config
        self.extra_sheets_v2_service = ExtraSheetsV2Service(conf)
        self.extra_drive_permission_v2_service = ExtraDrivePermissionV2Service(conf)

    def change_spreadsheet_permission(
        self,
        ss_token: str,
        link_share_entity: Literal[
            "tenant_readable", "tenant_editable", "anyone_readable", "anyone_editable"
        ],
    ) -> None:
        """
        :param link_share_entity:
        "tenant_readable" - 组织内获得链接的人可阅读
        "tenant_editable" - 组织内获得链接的人可编辑
        "anyone_readable" - 获得链接的任何人可阅读
        "anyone_editable" - 获得链接的任何人可编辑
        """
        resp = self.extra_drive_permission_v2_service.publics.update(
            body=extra_drive_permission_v2_model.PublicUpdateReqBody(
                token=ss_token,
                type="sheet",
                link_share_entity=link_share_entity,
            ),
        ).do()
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def create_spreadsheet(
        self,
        folder_token: str,
        title: str,
        auto_share_in_tenant: bool = False,
    ) -> Spreadsheet:
        client = self.s.upstream_client
        req = (
            CreateSpreadsheetRequest.builder()
            .request_body(
                Spreadsheet.builder()
                .title(
                    title,
                )
                .folder_token(
                    folder_token,
                )
                .build()
            )
            .build()
        )
        resp = client.sheets.v3.spreadsheet.create(req)
        if not resp.success() or not resp.data or not resp.data.spreadsheet:
            raise FeishuSheetsShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        if auto_share_in_tenant:
            ss_token = resp.data.spreadsheet.spreadsheet_token
            if ss_token:
                self.change_spreadsheet_permission(
                    ss_token=ss_token, link_share_entity="tenant_editable"
                )
        return resp.data.spreadsheet

    def get_spreadsheet_sheets(
        self,
        ss_token: str,
    ) -> List[Sheet]:
        client = self.s.upstream_client
        req = QuerySpreadsheetSheetRequest.builder().spreadsheet_token(ss_token).build()
        resp = client.sheets.v3.spreadsheet_sheet.query(req)
        if not resp.success() or not resp.data or not resp.data.sheets:
            raise FeishuSheetsShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data.sheets

    def find_cell_locations_in_sheet(
        self,
        ss_token: str,
        sheet_id: str,
        text: str,
        cond_cells_range: Optional[CellsRange] = None,
        cond_match_case: bool = False,
        cond_match_entire_cell: bool = False,
        cond_search_by_regex: bool = False,
        cond_include_formulas: bool = False,
    ) -> FindReplaceResult:
        client = self.s.upstream_client
        range_ = sheet_id
        if isinstance(cond_cells_range, CellsRange):
            cond_cells_range_literal = cond_cells_range.to_param_range_pos_part()
            range_ = f"{sheet_id}!{cond_cells_range_literal}"
        req = (
            FindSpreadsheetSheetRequest.builder()
            .spreadsheet_token(ss_token)
            .sheet_id(sheet_id)
            .request_body(
                Find.builder()
                .find(text)
                .find_condition(
                    FindCondition.builder()
                    .range(range_)
                    .match_case(cond_match_case)
                    .match_entire_cell(cond_match_entire_cell)
                    .search_by_regex(cond_search_by_regex)
                    .include_formulas(cond_include_formulas)
                    .build(),
                )
                .build()
            )
            .build()
        )
        resp = client.sheets.v3.spreadsheet_sheet.find(req)
        if not resp.success() or not resp.data or not resp.data.find_result:
            raise FeishuSheetsShortcutOperationError(
                str(
                    (
                        resp.get_log_id(),
                        resp.code,
                        resp.msg,
                    )
                )
            )
        return resp.data.find_result

    def recursive_find_cell_locations_in_sheet(
        self,
        ss_token: str,
        sheet_id: str,
        texts: List[str],
        cond_cells_range: Optional[CellsRange] = None,
        cond_match_case: bool = False,
        cond_match_entire_cell: bool = False,
        cond_search_by_regex: bool = False,
        cond_include_formulas: bool = False,
    ) -> Optional[FindReplaceResult]:
        further_cell_range = cond_cells_range
        result = None
        for text in texts:
            result = self.find_cell_locations_in_sheet(
                ss_token=ss_token,
                sheet_id=sheet_id,
                text=text,
                cond_cells_range=further_cell_range,
                cond_match_case=cond_match_case,
                cond_match_entire_cell=cond_match_entire_cell,
                cond_search_by_regex=cond_search_by_regex,
                cond_include_formulas=cond_include_formulas,
            )
            cp_texts = []
            if cond_include_formulas:
                if result.matched_formula_cells:
                    cp_texts = result.matched_formula_cells
                elif result.matched_cells:
                    cp_texts = result.matched_cells
            else:
                if result.matched_cells:
                    cp_texts = result.matched_cells
                elif result.matched_formula_cells:
                    cp_texts = result.matched_formula_cells
            if not cp_texts:
                break
            cp_texts.sort(key=lambda t: CellPos.from_literal(t))
            try:
                start_cp, end_cp = CellPos.from_literal(
                    cp_texts[0]
                ), CellPos.from_literal(cp_texts[-1])
            except:
                break
            if start_cp.x == end_cp.x:
                start_cp.x = end_cp.x = ""
            else:
                start_cp.y = end_cp.y = 0
            further_cell_range = CellsRange(start_pos=start_cp, end_pos=end_cp)

        return result

    def batch_handle_sheets(
        self,
        ss_token: str,
        add_sheet: Optional[extra_sheets_v2_model.AddSheet] = None,
        copy_sheet: Optional[extra_sheets_v2_model.CopySheet] = None,
        delete_sheet: Optional[extra_sheets_v2_model.DeleteSheet] = None,
        update_sheet: Optional[extra_sheets_v2_model.UpdateSheet] = None,
    ):
        req_params = dict(
            add_sheet=add_sheet,
            copy_sheet=copy_sheet,
            delete_sheet=delete_sheet,
            update_sheet=update_sheet,
        )
        r = extra_sheets_v2_model
        req = r.SpreadsheetsSheetsBatchUpdateReqBody(
            requests=r.Request(
                **req_params,
            ),
        )
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.sheets_batch_update(
                req,
            )
            .set_spreadsheetToken(
                ss_token,
            )
            .do()
        )
        return resp

    def create_sheet(
        self,
        ss_token: str,
        title: str,
        index: int = 0,
    ) -> Dict[str, str]:
        r = extra_sheets_v2_model
        op_sheet = r.AddSheet(
            properties=r.Properties(
                title=title,
                index=index,
            )
        )
        resp = self.batch_handle_sheets(
            ss_token=ss_token,
            add_sheet=op_sheet,
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))
        sheet_name__sheet_id = {}
        for rp in resp.data.replies:
            if rp.add_sheet:
                rpp = rp.add_sheet.properties
                sheet_name__sheet_id[rpp.title] = rpp.sheet_id
        return sheet_name__sheet_id

    def remove_sheet(
        self,
        ss_token: str,
        sheet_id: str,
    ) -> None:
        r = extra_sheets_v2_model
        op_sheet = r.DeleteSheet(sheet_id=sheet_id)
        resp = self.batch_handle_sheets(
            ss_token=ss_token,
            delete_sheet=op_sheet,
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def merge_cells(
        self,
        ss_token: str,
        sheet_id: str,
        cr: CellsRange,
        merge_type: Literal["MERGE_ALL", "MERGE_ROWS", "MERGE_COLUMNS"] = "MERGE_ALL",
    ) -> None:
        r = extra_sheets_v2_model
        range_text = f"{sheet_id}!" + cr.to_param_range_pos_part()
        req = r.SpreadsheetsMergeCellsReqBody(
            spreadsheet_token=ss_token,
            range=range_text,
            merge_type=merge_type,
        )
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.merge_cells(
                req,
            )
            .set_spreadsheetToken(
                ss_token,
            )
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def unmerge_cells(
        self,
        ss_token: str,
        sr: SheetRange,
    ) -> None:
        r = extra_sheets_v2_model
        range_text = sr.to_param_range()
        req = r.SpreadsheetsUnmergeCellsReqBody(
            range=range_text,
        )
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.unmerge_cells(
                req,
            )
            .set_spreadsheetToken(
                ss_token,
            )
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def prepend_insert_values(
        self,
        ss_token: str,
        sheet_id: str,
        cr: Optional[CellsRange] = None,
        values: Optional[Sequence[Sequence[Any]]] = None,
        headers: Sequence[Any] = (),
    ) -> None:
        if not values:
            raise FeishuSheetsShortcutOperationError("input invalid")
        converted_values = []
        n_max_cols = 0
        n_rows = 0
        _headers = list(headers)
        if _headers:
            converted_values.append(_headers)
            n_rows += 1
        for row in values:
            n_max_cols = max(n_max_cols, len(row))
            converted_values.append(list(row))
            n_rows += 1
        if not isinstance(cr, CellsRange):
            cr = CellsRange()
        if not cr.start_pos:
            cr.start_pos = CellPos(x="A", y=1)
        if not cr.end_pos:
            cr.end_pos = CellPos(x="")
        cr.end_pos.x = cr.end_pos.x or utils.column_number_to_name(n_max_cols)
        cr.end_pos.y = cr.end_pos.y or (n_rows + cr.start_pos.y)
        range_text = f"{sheet_id}!" + cr.to_param_range_pos_part()
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.values_prepend(
                extra_sheets_v2_model.SpreadsheetsValuesPrependReqBody(
                    value_range=extra_sheets_v2_model.ValueRange(
                        range=range_text,
                        values=converted_values,
                    )
                )
            )
            .set_spreadsheetToken(ss_token)
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def append_insert_values(
        self,
        ss_token: str,
        sheet_id: str,
        cr: Optional[CellsRange] = None,
        values: Optional[Sequence[Sequence[Any]]] = None,
        headers: Sequence[Any] = (),
        insert_data_option: Literal["OVERWRITE", "INSERT_ROWS"] = "OVERWRITE",
    ) -> None:
        if not values:
            raise FeishuSheetsShortcutOperationError("input invalid")
        converted_values = []
        n_max_cols = 0
        n_rows = 0
        _headers = list(headers)
        if _headers:
            converted_values.append(_headers)
            n_rows += 1
        for row in values:
            n_max_cols = max(n_max_cols, len(row))
            converted_values.append(list(row))
            n_rows += 1
        if not isinstance(cr, CellsRange):
            cr = CellsRange()
        if not cr.start_pos:
            cr.start_pos = CellPos(x="A", y=1)
        if not cr.end_pos:
            cr.end_pos = CellPos(x="")
        cr.end_pos.x = cr.end_pos.x or utils.column_number_to_name(n_max_cols)
        cr.end_pos.y = cr.end_pos.y or (n_rows + cr.start_pos.y)
        range_text = f"{sheet_id}!" + cr.to_param_range_pos_part()
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.values_append(
                extra_sheets_v2_model.SpreadsheetsValuesAppendReqBody(
                    value_range=extra_sheets_v2_model.ValueRange(
                        range=range_text,
                        values=converted_values,
                    )
                )
            )
            .set_insertDataOption(insert_data_option)
            .set_spreadsheetToken(ss_token)
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def batch_update_values(
        self,
        ss_token: str,
        sheet_id: str,
        cr_values: List[Tuple[CellsRange, Sequence[Sequence[Any]]]],
    ) -> None:
        if not cr_values:
            raise FeishuSheetsShortcutOperationError("input invalid")
        value_ranges = []
        for cr, values in cr_values:
            converted_values = []
            n_max_cols = 0
            n_rows = 0
            for row in values:
                n_max_cols = max(n_max_cols, len(row))
                converted_values.append(list(row))
                n_rows += 1
            if not cr.start_pos:
                cr.start_pos = CellPos(x="A", y=1)
            if not cr.end_pos:
                cr.end_pos = CellPos(x="")
            cr.end_pos.x = cr.end_pos.x or utils.column_number_to_name(n_max_cols)
            cr.end_pos.y = cr.end_pos.y or (n_rows + cr.start_pos.y)
            range_text = f"{sheet_id}!" + cr.to_param_range_pos_part()
            value_ranges.append(
                extra_sheets_v2_model.ValueRange(
                    range=range_text,
                    values=converted_values,
                ),
            )
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.values_batch_update(
                extra_sheets_v2_model.SpreadsheetsValuesBatchUpdateReqBody(
                    value_ranges=value_ranges,
                )
            )
            .set_spreadsheetToken(ss_token)
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def batch_read_values(
        self,
        ss_token: str,
        sheet_id: str,
        crs: List[CellsRange],
        value_render_option: Literal[
            "ToString", "FormattedValue", "Formula", "UnformattedValue"
        ] = "ToString",
        date_time_render_option: str = "FormattedString",
    ) -> Dict[str, List[list]]:
        if not crs:
            raise FeishuSheetsShortcutOperationError("input invalid")
        range_texts = ",".join(
            [f"{sheet_id}!" + cr.to_param_range_pos_part() for cr in crs]
        )
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.values_batch_get()
            .set_spreadsheetToken(ss_token)
            .set_ranges(range_texts)
            .set_valueRenderOption(value_render_option)
            .set_dateTimeRenderOption(date_time_render_option)
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))
        range_cr__values = {}
        for vr in resp.data.value_ranges:
            range_cr__values[
                SheetRange.from_literal(vr.range).to_param_range_pos_part()
            ] = vr.values
        return range_cr__values

    def update_formula_value_cell(
        self,
        ss_token: str,
        sheet_id: str,
        formula_text: str,
        result_cell_pos: CellPos,
        auto_merge_cells_range: Optional[CellsRange] = None,
    ) -> None:
        values = [
            [
                cell_value_support_data_types.Formula(text=formula_text).dict(),
            ]
        ]
        self.batch_update_values(
            ss_token=ss_token,
            sheet_id=sheet_id,
            cr_values=[
                (
                    CellsRange(start_pos=result_cell_pos, end_pos=result_cell_pos),
                    values,
                ),
            ],
        )
        if auto_merge_cells_range:
            self.merge_cells(
                ss_token=ss_token,
                sheet_id=sheet_id,
                cr=auto_merge_cells_range,
            )

    def update_formula_value_cell_using_sum_of_cell_range(
        self,
        ss_token: str,
        sheet_id: str,
        target_cells_range: CellsRange,
        result_cell_pos: CellPos,
        auto_merge_cells_range: Optional[CellsRange] = None,
    ) -> None:
        self.update_formula_value_cell(
            ss_token=ss_token,
            sheet_id=sheet_id,
            formula_text=f"=SUM({target_cells_range.to_param_range_pos_part()})",
            result_cell_pos=result_cell_pos,
            auto_merge_cells_range=auto_merge_cells_range,
        )

    def insert_dimension(
        self,
        ss_token: str,
        sheet_id: str,
        dimension: Literal["ROWS", "COLUMNS"] = "ROWS",
        start_index=0,
        end_index=1,
        inherit_style=None,
    ) -> None:
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.insert_dimension_range(
                extra_sheets_v2_model.SpreadsheetsInsertDimensionRangeReqBody(
                    dimension=extra_sheets_v2_model.Dimension(
                        sheet_id=sheet_id,
                        major_dimension=dimension,
                        start_index=start_index,
                        end_index=end_index,
                    ),
                    inherit_style=inherit_style,
                )
            )
            .set_spreadsheetToken(
                ss_token,
            )
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def delete_dimension(
        self,
        ss_token: str,
        sheet_id: str,
        dimension: Literal["ROWS", "COLUMNS"] = "ROWS",
        start_index=1,
        end_index=1,
    ) -> None:
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.dimension_range_delete(
                extra_sheets_v2_model.SpreadsheetsDimensionRangeDeleteReqBody(
                    dimension=extra_sheets_v2_model.Dimension(
                        sheet_id=sheet_id,
                        major_dimension=dimension,
                        start_index=start_index,
                        end_index=end_index,
                    ),
                )
            )
            .set_spreadsheetToken(
                ss_token,
            )
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))

    def truncate_sheet(
        self,
        ss_token: str,
        sheet_id: str,
    ):
        sheet_id__sheet = {
            s.sheet_id: s
            for s in self.get_spreadsheet_sheets(
                ss_token=ss_token,
            )
        }
        sheet = sheet_id__sheet.get(sheet_id)
        if not sheet:
            raise FeishuSheetsShortcutOperationError(
                f"not found sheet:{sheet_id} in {ss_token}"
            )
        sg = sheet.grid_properties
        n_rows, n_columns = 0, 0
        if sg:
            n_rows, n_columns = sg.row_count, sg.column_count
        if n_rows <= 0 or n_columns <= 0:
            raise FeishuSheetsShortcutOperationError("fetch sheet properties failed")
        self.insert_dimension(
            ss_token=ss_token,
            sheet_id=sheet_id,
        )
        N_MAX_DELETE_LINE = 5000
        n_inserted = 1
        start_index = 1 + n_inserted
        end_index = n_rows + n_inserted
        for st, ed in [
            (i, min(i + N_MAX_DELETE_LINE, end_index))
            for i in range(
                start_index,
                end_index + 1,
                N_MAX_DELETE_LINE,
            )
        ][::-1]:
            self.delete_dimension(
                ss_token=ss_token,
                sheet_id=sheet_id,
                start_index=st,
                end_index=ed,
            )

    def replace_sheet_by_values(
        self,
        ss_token: str,
        sheet_id: str,
        values: List[list],
        headers: Sequence[Any] = (),
    ):
        self.truncate_sheet(
            ss_token=ss_token,
            sheet_id=sheet_id,
        )
        self.prepend_insert_values(
            ss_token=ss_token,
            sheet_id=sheet_id,
            values=values,
            headers=headers,
        )

    def insert_image_to_cell(
        self,
        ss_token: str,
        sheet_id: str,
        cell_pos: CellPos,
        image_byte_array: List[int],
        image_name: str = "",
    ):
        cp = cell_pos.to_param_range()
        if not image_name:
            image_name = f"photo-{cp}-{str(datetime.datetime.now())}"
        body_range = f"{sheet_id}!{cp}:{cp}"
        resp = (
            self.extra_sheets_v2_service.spreadsheetss.values_image(
                body=extra_sheets_v2_model.SpreadsheetsValuesImageReqBody(
                    range=body_range,
                    image=image_byte_array,
                    name=image_name,
                )
            )
            .set_spreadsheetToken(ss_token)
            .do()
        )
        if resp.code != 0:
            raise FeishuSheetsShortcutOperationError(str(resp))
