"""Shared wire-contract datatypes for the Continuous Tracking platform.

This package is the single source of truth for the *hand-written* contract types
shared between the producer (``continuous-tracking/tracking-orchestrator``) and the
consumer (``cognitive-companion``): the canonical dementia-signal vocabulary and
severity levels. It deliberately has no protobuf dependency so either side can adopt
it without pulling the generated SDK.

The generated protobuf bindings (``continuoustracking.v1.*_pb2``) are a separate,
heavier concern; see ``README.md`` for the two-problem strategy and migration plan.
"""

from __future__ import annotations

from cts_contracts.signals import (
    DementiaSignalKind,
    DementiaSignalSeverity,
)

__all__ = [
    "DementiaSignalKind",
    "DementiaSignalSeverity",
]

__version__ = "0.1.0"
