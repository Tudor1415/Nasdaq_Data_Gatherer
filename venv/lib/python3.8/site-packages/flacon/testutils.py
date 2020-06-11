"""Test utils for flacon."""


def setup(flacon, args=None):
    """Setup flacon for testing."""
    args = args or []
    parser = flacon.get_argparser()
    # Make sure we don't use sys.argv.
    args = parser.parse_args(args)
    # Setup everything.
    flacon.setup(args)
