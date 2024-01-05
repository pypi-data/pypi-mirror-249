import pkg_resources

from ._installers import get_jre_home, get_mzmine2_home

__version__ = pkg_resources.require(__package__.replace(".", "-"))[0].version

# cleanup namespace:
del pkg_resources

if get_mzmine2_home() is None or get_jre_home() is None:

    def init():
        from ._installers import install_jre, install_mzmine2, install_example_files

        install_jre()
        print()
        install_mzmine2()
        print()
        install_example_files()

        import importlib

        importlib.import_module(__name__)

        print()
        print("init done, please create new session to use emzed.ext.mzmine2")

    # cleanup ns
    del get_jre_home
    del get_mzmine2_home

    print("please execute:")
    print()
    print(f"import {__package__}")
    print(f"{__package__}.init()")
    print()

    def __getattr__(name):
        raise ImportError(
            f"\n{__package__}.{name} not available,"
            f" please call {__package__}.init() first"
        )

    def __dir__():
        return ["init"]


else:

    # cleanup ns
    del get_jre_home
    del get_mzmine2_home

    def init():
        print("nothing to do")

    from .remove_shoulder_peaks import (  # noqa: F401
        remove_shoulder_peaks,
        RemoveShoulderPeaksParameters,
    )

    from .pick_peaks import *  # noqa: F401, F403

    from .adduct_search import adduct_search, AdductSearchParameters  # noqa: F401
    from .fragment_search import fragment_search, FragmentSearchParameters  # noqa: F401
    from .isotope_grouper import isotope_grouper, IsotopeGrouperParameters  # noqa: F401
    from .join_aligner import join_aligner  # noqa: F401
    from .join_aligner import IsotopePatternScoreParameters  # noqa: F401
    from .join_aligner import JoinAlignerParameters  # noqa: F401
