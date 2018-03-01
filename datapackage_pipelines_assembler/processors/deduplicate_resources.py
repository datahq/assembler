from datapackage_pipelines.wrapper import process


def modify_datapackage(dp, parameters, stats):
    resources_names = set([])
    new_resources = []
    for resource in dp['resources']:
        if resource['name'] not in resources_names:
            new_resources.append(resource)
            resources_names.add(resource['name'])
    dp['resources'] = new_resources
    return dp


process(modify_datapackage=modify_datapackage)
