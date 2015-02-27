"""
Main script for running HApAPI

"""

def main():
    """
    Main function for HApAPI

    """
    from hapapi.api import setup
    setup().run(debug=True)


if __name__ == "__main__":
    main()
