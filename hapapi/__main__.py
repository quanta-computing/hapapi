"""
Main script for running HApAPI

"""

def main():
    """
    Main function for HApAPI

    """
    import argparse
    from hapapi.api import setup
    parser = argparse.ArgumentParser(
        description='HApAPI is a REST API to interact with HAproxy unix socket interface',
        epilog='Copyright Quanta 2015',
    )
    parser.add_argument('-b', '--bind', default='127.0.0.1',
        help='On wich ip address we listen for incoming connections'
    )
    parser.add_argument('-p', '--port', type=int, default=5000,
        help='On wich port we listen for incoming connections'
    )
    parser.add_argument('-f', '--config', default='/etc/haproxy/hapapi.cfg',
        help='Path to a config file'
    )
    opts = parser.parse_args()
    setup(opts.config).run(opts.bind, opts.port)


if __name__ == "__main__":
    main()
