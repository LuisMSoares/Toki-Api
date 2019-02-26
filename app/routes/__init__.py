def json_verification(json_data, keys):
    return all( [ k in keys for k in json_data.keys() ] )
