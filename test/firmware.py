import os
from zipfile import ZipFile


def fw_unpack(fw_path, outdir):

    # Unzip firmware package
    with ZipFile(fw_path, 'r') as zipObj:
        zipObj.extractall(outdir)

        list_dir = os.listdir(outdir)

        firmware_file_name = list(filter(lambda x: 'firmware' in x, list_dir))
        config_file_name = list(filter(lambda x: 'config' in x, list_dir))
        schema_file_name = list(filter(lambda x: 'schema' in x and 'uischema' not in x, list_dir))

        assert len(firmware_file_name) == 1
        assert len(config_file_name) == 1
        assert len(schema_file_name) == 1

        firmware_file_name = firmware_file_name[0]
        config_file_name = config_file_name[0]
        schema_file_name = schema_file_name[0]

        firmware_file_path = os.path.join(outdir, firmware_file_name)
        config_file_path = os.path.join(outdir, config_file_name)
        schema_file_path = os.path.join(outdir, schema_file_name)

    return {'firmware_path': firmware_file_path,
            'config_path': config_file_path,
            'schema_path': schema_file_path,
            'firmware_name': firmware_file_name,
            'config_name': config_file_name,
            'schema_name': schema_file_name }