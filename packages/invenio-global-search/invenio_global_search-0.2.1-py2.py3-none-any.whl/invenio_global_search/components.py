# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from __future__ import annotations

from collections.abc import Callable

from flask_principal import Identity
from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_rdm_records.resources.serializers.dublincore import (
    DublinCoreJSONSerializer,
)
from invenio_records_global_search import current_records_global_search
from invenio_records_lom.records import LOMRecord
from invenio_records_lom.utils import LOMMetadata
from invenio_records_marc21.records import Marc21Record
from invenio_records_marc21.services.record import Marc21Metadata
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation

from .serializers import LOMRecordJSONSerializer, Marc21RecordJSONSerializer


def map_metadata_from_a_to_b(
    record,
    serializer_cls=None,
    metadata_cls=None,
    schema=None,
    identity=None,
) -> None:
    """Func."""
    schema_mapping = {
        "rdm": "records",
        "lom": "oer",
        "marc21": "publications",
    }

    record_serializer = serializer_cls()
    data = record.dumps()
    obj = metadata_cls(json=data["metadata"]) if metadata_cls else data
    metadata = record_serializer.dump_obj(obj)
    pid = record["id"]
    path = schema_mapping[schema]
    original = {
        "view": f"{path}/{pid}",
        "schema": schema,
        "pid": pid,
    }
    data = {
        "metadata": metadata,
        "original": original,
    }

    current_records_global_search.records_service.create_or_update(
        identity=identity,
        data=data,
    )


class ComponentOp(Operation):
    """ComponentOp."""

    def __init__(
        self,
        record: RDMRecord,
        func: Callable = map_metadata_from_a_to_b,
        serializer_cls=None,
        metadata_cls=None,
        schema=None,
        identity=None,
    ) -> None:
        """Construct."""
        self._record = record
        self._func = func
        self._serializer_cls = serializer_cls
        self._metadata_cls = metadata_cls
        self._schema = schema
        self._identity = identity

    def on_post_commit(self, uow) -> None:  # noqa: ARG002
        """Post commit."""
        self._func(
            self._record,
            self._serializer_cls,
            self._metadata_cls,
            self._schema,
            self._identity,
        )


class Marc21ToGlobalSearchComponent(ServiceComponent):
    """Marc21ToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: Marc21Record | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=Marc21RecordJSONSerializer,
            metadata_cls=Marc21Metadata,
            schema="marc21",
            identity=identity,
        )
        self.uow.register(cmp_op)


class LOMToGlobalSearchComponent(ServiceComponent):
    """LOMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: LOMRecord | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=LOMRecordJSONSerializer,
            metadata_cls=LOMMetadata,
            schema="lom",
            identity=identity,
        )
        self.uow.register(cmp_op)


class RDMToGlobalSearchComponent(ServiceComponent):
    """RDMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        draft: RDMDraft | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""
        if draft["access"]["record"] != "public":
            return

        cmp_op = ComponentOp(
            record,
            serializer_cls=DublinCoreJSONSerializer,
            schema="rdm",
            identity=identity,
        )
        self.uow.register(cmp_op)
