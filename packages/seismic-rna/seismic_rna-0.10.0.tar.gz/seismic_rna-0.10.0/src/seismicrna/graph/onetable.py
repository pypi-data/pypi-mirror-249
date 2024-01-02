from abc import ABC, abstractmethod
from functools import cached_property
from itertools import chain
from pathlib import Path

from .base import (GraphBase,
                   GraphRunner,
                   GraphWriter,
                   cgroup_table,
                   get_action_name,
                   make_index,
                   make_path_subject,
                   make_title_action_sample)
from ..core.parallel import dispatch
from ..table.base import Table, PosTable


class OneTableGraph(GraphBase, ABC):
    """ Graph of data from one Table. """

    def __init__(self, *,
                 table: Table | PosTable,
                 order: int | None,
                 clust: int | None,
                 **kwargs):
        super().__init__(**kwargs)
        self.table = table
        self.order = order
        self.clust = clust

    @property
    def sample(self):
        return self.table.sample

    @property
    def ref(self):
        return self.table.ref

    @property
    def sect(self):
        return self.table.sect

    @property
    def seq(self):
        return self.table.seq

    @cached_property
    def action(self):
        """ Action that generated the data. """
        return get_action_name(self.table)

    @cached_property
    def row_index(self):
        return make_index(self.table.header, self.order, self.clust)

    @property
    def col_index(self):
        return None

    @cached_property
    def path_subject(self):
        return make_path_subject(self.action, self.order, self.clust)

    @cached_property
    def title_action_sample(self):
        return make_title_action_sample(self.action, self.sample)


class OneTableWriter(GraphWriter, ABC):

    def __init__(self, table_file: Path):
        super().__init__(table_file)

    @cached_property
    def table(self):
        """ The table providing the data for the graph(s). """
        return self.load_table_file(self.table_files[0])

    @abstractmethod
    def get_graph(self, *args, **kwargs) -> OneTableGraph:
        """ Return a graph instance. """

    def iter_graphs(self,
                    rels: tuple[str, ...],
                    cgroup: str,
                    **kwargs):
        for cparams in cgroup_table(self.table, cgroup):
            for rels_group in rels:
                yield self.get_graph(rels_group, **kwargs | cparams)


class OneTableRunner(GraphRunner, ABC):

    @classmethod
    def run(cls,
            input_path: tuple[str, ...], *,
            max_procs: int,
            parallel: bool,
            **kwargs):
        # Generate a table writer for each table.
        writer_type = cls.get_writer_type()
        writers = [writer_type(table_file)
                   for table_file in cls.list_table_files(input_path)]
        return list(chain(*dispatch([writer.write for writer in writers],
                                    max_procs,
                                    parallel,
                                    pass_n_procs=False,
                                    kwargs=kwargs)))
