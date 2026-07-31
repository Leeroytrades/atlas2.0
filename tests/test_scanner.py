"""
Atlas AI Trading Assistant 3.0

Scanner Tests
"""

from atlas.scanner import ScanResult



def test_scan_result():

    result = ScanResult(

        symbol="TEST",

        dataframe=None,

        score=80,

        bias="BUY",

        confidence=0.85,

    )


    assert result.symbol == "TEST"

    assert result.bias == "BUY"

    assert result.score == 80

    assert result.confidence == 0.85