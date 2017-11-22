import datapackage
from datapackage_pipelines.wrapper import ingest, spew
from datapackage_pipelines.lib.load_resource import ResourceLoader
from datapackage_pipelines.utilities.resources import PROP_STREAMED_FROM
from planner.utilities import s3_path

import logging

class PrivateResourceLoader(ResourceLoader):

    def __init__(self):
        super(ResourceLoader, self ).__init__()
        self.parameters, self.dp, self.res_iter = ingest()

    def process_datapackage(self, dp_):
        cached_paths = {}
        for i, res in enumerate(dp_.resources):
            # res.source = signed-url throws AttributError: can't set attribute
            # So we need to create new DataPackage object with resource path=signed-url
            # And modify res.source that way.
            cached_paths[i] = res.descriptor['path']
            dp_.descriptor['resources'][i]['path'] = s3_path(res.source)

        modified_dp = datapackage.DataPackage(dp_.descriptor)
        for i, res in enumerate(modified_dp.resources):
            # We want back original paths. This can be modified directly
            res.descriptor['path'] = cached_paths[i]
        return modified_dp


if __name__ == '__main__':
    PrivateResourceLoader()()
