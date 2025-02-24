from arches.app.models.serializers import ArchesTileSerializer

def filter_out_tile_endpoints(endpoints):
    filtered_endpoints = []
    for endpoint in endpoints:
        (path, path_regex, method, view_function) = endpoint
        serializer_class = view_function.cls().get_serializer_class()
        if issubclass(serializer_class, ArchesTileSerializer):
            continue
        filtered_endpoints.append(endpoint)

    return filtered_endpoints
