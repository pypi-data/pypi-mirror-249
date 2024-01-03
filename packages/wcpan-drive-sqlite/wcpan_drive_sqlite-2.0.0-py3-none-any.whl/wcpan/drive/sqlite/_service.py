from contextlib import asynccontextmanager
from concurrent.futures import ProcessPoolExecutor
from pathlib import PurePath

from wcpan.drive.core.exceptions import NodeNotFoundError
from wcpan.drive.core.types import ChangeAction, Node, SnapshotService

from ._lib import OffMainProcess
from ._outer import (
    initialize,
    get_node_by_path,
    resolve_path_by_id,
    get_child_by_name,
    get_children_by_id,
    get_trashed_nodes,
    apply_changes,
    find_nodes_by_regex,
    get_current_cursor,
    get_root,
    set_root,
    get_node_by_id,
)


@asynccontextmanager
async def create_service(*, dsn: str):
    with ProcessPoolExecutor() as pool:
        bg = OffMainProcess(dsn=dsn, pool=pool)
        await bg(initialize)
        yield SqliteSnapshotService(bg)


class SqliteSnapshotService(SnapshotService):
    def __init__(self, bg: OffMainProcess) -> None:
        self._bg = bg

    @property
    def api_version(self) -> int:
        return 4

    async def get_current_cursor(self) -> str:
        cursor = await self._bg(get_current_cursor)
        return "" if not cursor else cursor

    async def get_root(self) -> Node:
        root = await self._bg(get_root)
        if not root:
            raise NodeNotFoundError("root")
        return root

    async def set_root(self, node: Node) -> None:
        await self._bg(set_root, node)

    async def get_node_by_id(self, node_id: str) -> Node:
        node = await self._bg(get_node_by_id, node_id)
        if not node:
            raise NodeNotFoundError(node_id)
        return node

    async def get_node_by_path(self, path: PurePath) -> Node:
        if not path.is_absolute():
            raise ValueError("path must be an absolute path")
        node = await self._bg(get_node_by_path, path)
        if not node:
            raise NodeNotFoundError(str(path))
        return node

    async def resolve_path_by_id(self, node_id: str) -> PurePath:
        path = await self._bg(resolve_path_by_id, node_id)
        if not path:
            raise NodeNotFoundError(node_id)
        return path

    async def get_child_by_name(self, name: str, parent_id: str) -> Node:
        node = await self._bg(get_child_by_name, name, parent_id)
        if not node:
            raise NodeNotFoundError(name)
        return node

    async def get_children_by_id(self, parent_id: str) -> list[Node]:
        return await self._bg(get_children_by_id, parent_id)

    async def get_trashed_nodes(self) -> list[Node]:
        return await self._bg(get_trashed_nodes)

    async def apply_changes(
        self,
        changes: list[ChangeAction],
        cursor: str,
    ) -> None:
        return await self._bg(apply_changes, changes, cursor)

    async def find_nodes_by_regex(self, pattern: str) -> list[Node]:
        return await self._bg(find_nodes_by_regex, pattern)
