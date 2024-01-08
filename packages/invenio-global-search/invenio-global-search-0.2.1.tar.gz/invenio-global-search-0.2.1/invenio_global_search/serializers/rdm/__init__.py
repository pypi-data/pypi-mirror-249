# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search rdm searializer."""

# the problem is the parent does not exists in this stage
# from invenio_rdm_records.resources.serializers.dublincore import (
#     DublinCoreJSONSerializer as RDMRecordJSONSerializer,
# )

from .serializer import RDMRecordJSONSerializer

__all__ = ("RDMRecordJSONSerializer",)
