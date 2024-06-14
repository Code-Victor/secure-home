# write test for the hex2Scalar function
import pytest
from secure_home.utils import hex2Scalar


class TestHex2Scalar:
    def test_hex2Scalar(self):
        assert hex2Scalar("#FF00FF") == (255, 0, 255)
        assert hex2Scalar("#000000") == (0, 0, 0)
        assert hex2Scalar("#FFFFFF") == (255, 255, 255)
        assert hex2Scalar("#00FF00") == (0, 255, 0)
        assert hex2Scalar("#0000FF") == (0, 0, 255)
        assert hex2Scalar("#FF0000") == (255, 0, 0)
        assert hex2Scalar("#FFFF00") == (255, 255, 0)
        assert hex2Scalar("#00FFFF") == (0, 255, 255)
        assert hex2Scalar("#C0C0C0") == (192, 192, 192)
        assert hex2Scalar("#808080") == (128, 128, 128)
        assert hex2Scalar("#800000") == (128, 0, 0)
        assert hex2Scalar("#808000") == (128, 128, 0)
        assert hex2Scalar("#008000") == (0, 128, 0)
        assert hex2Scalar("#800080") == (128, 0, 128)
        assert hex2Scalar("#008080") == (0, 128, 128)
        assert hex2Scalar("#000080") == (0, 0, 128)
        assert hex2Scalar("#A52A2A") == (165, 42, 42)
        assert hex2Scalar("#D2691E") == (210, 105, 30)
        assert hex2Scalar("#FF7F50") == (255, 127, 80)
        assert hex2Scalar("#FFA07A") == (255, 160, 122)
        assert hex2Scalar("#FF4500") == (255, 69, 0)
        assert hex2Scalar("#FF6347") == (255, 99, 71)
        assert hex2Scalar("#FFD700") == (255, 215, 0)
        assert hex2Scalar("#FF8C00") == (255, 140, 0)
        assert hex2Scalar("#FFA500") == (255, 165, 0)


if __name__ == "__main__":
    pytest.main()