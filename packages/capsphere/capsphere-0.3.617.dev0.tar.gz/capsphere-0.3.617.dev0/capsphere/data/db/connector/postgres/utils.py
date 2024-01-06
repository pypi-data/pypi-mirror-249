def build_connection_args(host: str, dbname: str,
                          user: str, password: str,
                          port: str, ssl_cert_path: str) -> dict:
    """
    Builds connection arguments for the database.
    """
    sslmode = 'require' if ssl_cert_path else 'prefer'
    connection_args = {
        "host": host,
        "dbname": dbname,
        "user": user,
        "password": password,
        "port": port,
        "sslmode": sslmode,
    }
    if ssl_cert_path:
        connection_args["sslrootcert"] = ssl_cert_path
    return connection_args
