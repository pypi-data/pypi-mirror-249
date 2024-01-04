import os
import typing

import pandas

from .shared import GenericFileLoader


class CSVLoader(GenericFileLoader):

    async def execute(self, *inputs) -> typing.Any:
        assert len(inputs) == 0
        return pandas.read_csv(
            self.config.get_casted('params.filename', str),
        )

    @staticmethod
    def save_result(path: str, result: typing.Any):
        assert isinstance(result, pandas.DataFrame)
        result.to_pickle(os.path.join(path, 'main.pickle'))

    @staticmethod
    def load_result(path: str):
        return pandas.read_pickle(os.path.join(path, 'main.pickle'))
