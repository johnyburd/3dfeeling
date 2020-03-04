import magic


def parse_from_bytes(data: bytes) -> str:
    filetype = magic.from_buffer(data, mime=True)
    print(f"detected filetype: {filetype}")
    if filetype == 'application/pdf':
        raise ValueError(f"{filetype} filetype not supported")
    else:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            raise ValueError(f"'{filetype}' filetype not supported")
