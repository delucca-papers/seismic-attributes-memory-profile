import uuid
import importlib

from pydantic import BaseModel, FilePath, field_validator
from typing import Optional
from enum import Enum


__all__ = ["ProfilerConfig", "Metric", "MemoryUsageBackend", "MemoryUsageUnit"]


class Metric(Enum):
    MEMORY_USAGE = "MEMORY_USAGE"
    TIME = "TIME"


class MemoryUsageBackend(Enum):
    PSUTIL = "PSUTIL"
    RESOURCE = "RESOURCE"
    TRACEMALLOC = "TRACEMALLOC"
    MPROF = "MPROF"
    KERNEL = "KERNEL"


class MemoryUsageUnit(Enum):
    KB = "KB"
    MB = "MB"
    GB = "GB"


class MemoryUsageConfig(BaseModel):
    enabled_backends: list[MemoryUsageBackend] = [MemoryUsageBackend.KERNEL]
    unit: MemoryUsageUnit = MemoryUsageUnit.MB

    @field_validator("enabled_backends", mode="before")
    def uppercase_enabled_backends(cls, v: any) -> list[MemoryUsageBackend]:
        if isinstance(v, list):
            return [
                MemoryUsageBackend(i.upper()) if isinstance(i, str) else i for i in v
            ]

        return v

    @field_validator("unit", mode="before")
    def uppercase_unit(cls, v: any) -> MemoryUsageUnit:
        if isinstance(v, str):
            v = v.upper()

        return MemoryUsageUnit(v)


class ProfilerConfig(BaseModel):
    session_id: str = str(uuid.uuid4())
    enabled_metrics: list[Metric] = [Metric.MEMORY_USAGE, Metric.TIME]
    memory_usage: MemoryUsageConfig
    filepath: Optional[FilePath] = None
    entrypoint: Optional[str] = None
    args: tuple = tuple()
    kwargs: dict = {}

    @field_validator("enabled_metrics", mode="before")
    def uppercase_enabled_transports(cls, v: any) -> list[Metric]:
        if isinstance(v, list):
            return [Metric(i.upper()) if isinstance(i, str) else i for i in v]

        return v

    @field_validator("kwargs", mode="before")
    def parse_kwargs(cls, v: any):
        if isinstance(v, dict):
            return v
        if isinstance(v, list):
            result = {}
            for item in v:
                if "=" in item:
                    key, value = item.split("=", 1)
                    result[key] = value
                else:
                    raise ValueError(f"Invalid format for kwarg: {item}")
            return result

        raise TypeError("kwarg must be a list of strings or a dict")

    @field_validator("entrypoint")
    def check_function_exists(cls, v: any, values):
        if v is None:
            return v
        filepath = values.data.get("filepath")
        if filepath is None:
            raise ValueError("File path must be set before checking function")

        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, v):
            raise ValueError(f"Function '{v}' not found in {filepath}")
        return v