"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..regexp import rgxp_match



def test_rgxp_match() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert rgxp_match('1', '1')
    assert not rgxp_match('1', ['2', '3'])
    assert rgxp_match('1', ['1', '1'])
    assert not rgxp_match(['1', '2'], ['3'])
    assert not rgxp_match(['1', '2'], ['1'])
    assert rgxp_match(['1', '2'], ['1', '2'])

    assert not rgxp_match('11', '1', True)
    assert rgxp_match('1', '1', True)
