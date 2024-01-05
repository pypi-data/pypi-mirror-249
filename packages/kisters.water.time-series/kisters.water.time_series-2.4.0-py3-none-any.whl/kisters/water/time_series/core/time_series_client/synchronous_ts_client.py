from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable, Coroutine, Iterable
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from typing import Any, Literal, TypeVar, overload

import pandas as pd

from ..schema import CommentSupport, EnsembleMember, TimeSeriesComment, TimeSeriesKey, TimeSeriesMetadata
from ..time_series import TimeSeries
from .time_series_client import (
    DataFrameTypedDicts,
    SequenceNotStr,
    TimeSeriesClient,
    TimeSeriesMetadataType,
    TSCommentsTypedDicts,
)

T = TypeVar("T")


class SynchronousTimeSeriesClient:
    def __init__(self, client: TimeSeriesClient):
        self._client = client

    @property
    def comment_support(self) -> CommentSupport:
        return self._client.comment_support

    @property
    def time_series_schema(self) -> type[TimeSeriesMetadata]:
        return self._client.time_series_schema

    def run_sync(self, coroutine: Callable[..., Coroutine[Any, Any, T]], *args: Any, **kwargs: Any) -> T:
        """
        This method safely calls async methods from a sync context.

        Full details on this method can be found in .time_series_client.py, this is
        just an adaption where we do not keep opening the async context.
        """
        if not inspect.iscoroutinefunction(coroutine):
            raise ValueError(f"{coroutine} is not a coroutine")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future: Future[T] = executor.submit(asyncio.run, coroutine(*args, **kwargs))
            return future.result()

    def __enter__(self) -> SynchronousTimeSeriesClient:
        self.run_sync(self._client.__aenter__)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.run_sync(self._client.__aexit__, exc_type, exc_val, exc_tb)

    @overload
    def create_time_series(
        self,
        metadatas: TimeSeriesMetadataType,
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> TimeSeries:
        """"""

    @overload
    def create_time_series(
        self,
        metadatas: Iterable[TimeSeriesMetadataType],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[TimeSeries]:
        """"""

    def create_time_series(
        self,
        metadatas: TimeSeriesMetadataType | Iterable[TimeSeriesMetadataType],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> TimeSeries | list[TimeSeries]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.create_time_series, metadatas, **bulk_kwargs, **kwargs)

    @overload
    def read_time_series(
        self,
        *,
        paths: str,
        ts_filters: None = None,
        metadata_keys: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> TimeSeries:
        """"""

    @overload
    def read_time_series(
        self,
        *,
        paths: SequenceNotStr[str] | None = None,
        ts_filters: Iterable[str] | None = None,
        metadata_keys: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[TimeSeries]:
        """"""

    def read_time_series(
        self,
        *,
        paths: str | Iterable[str] | None = None,
        ts_filters: str | Iterable[str] | None = None,
        metadata_keys: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> TimeSeries | list[TimeSeries]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(
            self._client.read_time_series,
            paths=paths,
            ts_filters=ts_filters,
            metadata_keys=metadata_keys,
            **bulk_kwargs,
            **kwargs,
        )

    def update_time_series(
        self,
        metadatas: TimeSeriesMetadataType
        | Iterable[TimeSeriesMetadataType]
        | dict[str, TimeSeriesMetadataType],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.update_time_series, metadatas, **bulk_kwargs, **kwargs)

    def delete_time_series(
        self,
        paths: str | Iterable[str],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.delete_time_series, paths, **bulk_kwargs, **kwargs)

    @overload
    def read_coverage(
        self,
        keys: TimeSeriesKey | str,
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = (None, None),
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> tuple[datetime, datetime]:
        """"""

    @overload
    def read_coverage(
        self,
        keys: SequenceNotStr[TimeSeriesKey | str],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = (None, None),
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> dict[TimeSeriesKey, tuple[datetime, datetime]]:
        """"""

    def read_coverage(
        self,
        keys: TimeSeriesKey | str | Iterable[TimeSeriesKey | str],
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = (None, None),
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> tuple[datetime, datetime] | dict[TimeSeriesKey, tuple[datetime, datetime]]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.read_coverage, keys, **bulk_kwargs, **kwargs)

    @overload
    def read_ensemble_members(
        self,
        paths: str,
        *,
        t0_start: datetime | None = None,
        t0_end: datetime | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[EnsembleMember]:
        """"""

    @overload
    def read_ensemble_members(
        self,
        paths: SequenceNotStr[str],
        *,
        t0_start: Iterable[datetime] | datetime | None = None,
        t0_end: Iterable[datetime] | datetime | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> dict[TimeSeriesKey, list[EnsembleMember]]:
        """"""

    def read_ensemble_members(
        self,
        paths: str | Iterable[str],
        *,
        t0_start: Iterable[datetime] | datetime | None = None,
        t0_end: Iterable[datetime] | datetime | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[EnsembleMember] | dict[TimeSeriesKey, list[EnsembleMember]]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(
            self._client.read_ensemble_members,
            paths,
            t0_start=t0_start,
            t0_end=t0_end,
            **bulk_kwargs,
            **kwargs,
        )

    @overload
    def read_data_frame(
        self,
        keys: TimeSeriesKey | str,
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        columns: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = lambda: pd.DataFrame(index=pd.DatetimeIndex([])),
        **kwargs: Any,
    ) -> pd.DataFrame:
        """"""

    @overload
    def read_data_frame(
        self,
        keys: SequenceNotStr[TimeSeriesKey | str],
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        columns: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = lambda: pd.DataFrame(index=pd.DatetimeIndex([])),
        **kwargs: Any,
    ) -> dict[TimeSeriesKey, pd.DataFrame]:
        """"""

    def read_data_frame(
        self,
        keys: TimeSeriesKey | str | Iterable[TimeSeriesKey | str],
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        columns: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame | dict[TimeSeriesKey, pd.DataFrame]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(
            self._client.read_data_frame,
            keys,
            start=start,
            end=end,
            columns=columns,
            **bulk_kwargs,
            **kwargs,
        )

    def write_data_frame(
        self,
        data_frames: DataFrameTypedDicts,
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.write_data_frame, data_frames, **bulk_kwargs, **kwargs)

    def delete_data_range(
        self,
        keys: TimeSeriesKey | str | Iterable[TimeSeriesKey | str],
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(
            self._client.delete_data_range, keys, start=start, end=end, **bulk_kwargs, **kwargs
        )

    @overload
    def read_comments(
        self,
        keys: TimeSeriesKey | str,
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[TimeSeriesComment]:
        """"""

    @overload
    def read_comments(
        self,
        keys: SequenceNotStr[TimeSeriesKey | str],
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> dict[TimeSeriesKey, list[TimeSeriesComment]]:
        """"""

    def read_comments(
        self,
        keys: TimeSeriesKey | str | Iterable[TimeSeriesKey | str],
        *,
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> list[TimeSeriesComment] | dict[TimeSeriesKey, list[TimeSeriesComment]]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(
            self._client.read_comments, keys, start=start, end=end, **bulk_kwargs, **kwargs
        )

    def write_comments(
        self,
        comments: TSCommentsTypedDicts,
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.write_comments, comments, **bulk_kwargs, **kwargs)

    def delete_comments(
        self,
        comments: TSCommentsTypedDicts,
        *,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[[], Any] | None = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        bulk_kwargs = self._client.build_bulk_kwargs(
            concurrency_limit, error_handling, default_value, default_factory
        )
        return self.run_sync(self._client.delete_comments, comments, **bulk_kwargs, **kwargs)

    def info(self) -> dict[str, Any]:
        return self.run_sync(self._client.info)
