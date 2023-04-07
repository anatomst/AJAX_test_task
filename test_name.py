from unittest.mock import patch
import pytest

from scanner_handler import CheckQr


@pytest.fixture()
def qr_fixture():
    with patch.object(CheckQr, "check_in_db") as mocked_checking_in_db, \
            patch.object(CheckQr, "can_add_device") as mocked_adding_device, \
            patch.object(CheckQr, "send_error") as mocked_sending_error:
        check_qr = CheckQr()
        yield check_qr, mocked_checking_in_db, mocked_adding_device, mocked_sending_error


@pytest.mark.parametrize(
    "qr, expected_result",
    [
        ("333", "Red"),
        ("55555", "Green"),
        ("7777777", "Fuzzy Wuzzy"),
    ],
)
def test__check_qr_by_length_in_db__success(qr_fixture, qr, expected_result):
    """
    Check QR codes of different lengths that are in the database and check whether the program
    assigns the correct color depending on the length of the QR code.
    """
    # arrange
    check_qr, mocked_checking_in_db, mocked_adding_device, mocked_sending_error = qr_fixture
    mocked_checking_in_db.return_value = True

    # act
    check_qr.check_scanned_device(qr)

    # assert
    assert check_qr.color == expected_result
    mocked_adding_device.assert_called_once_with(f"hallelujah {qr}")


@pytest.mark.parametrize(
    "qr",
    [
        "22",
        "4444",
        "666666",
    ],
)
def test__check_qr_by_length_in_db__fail(qr_fixture, qr):
    """
    Negative case in which we check a QR code for the length of which there is no color
    """
    # arrange
    check_qr, mocked_checking_in_db, mocked_adding_device, mocked_sending_error = qr_fixture

    # act
    check_qr.check_scanned_device(qr)

    # assert
    assert check_qr.color is None
    mocked_sending_error.assert_called_once_with(f"Error: Wrong qr length {len(qr)}")


@pytest.mark.parametrize(
    "qr, color",
    [
        ("123", "Red"),
        ("12345", "Green"),
        ("1234567", "Fuzzy Wuzzy")
    ],
)
def test__qr_with_valid_length_but_not_in_db__success(qr_fixture, qr, color):
    """
    Check the QR, which is not in the database
    """
    # arrange
    check_qr, mocked_checking_in_db, mocked_adding_device, mocked_sending_error = qr_fixture
    mocked_checking_in_db.return_value = None

    # act
    check_qr.check_scanned_device(qr)

    # assert
    assert check_qr.color == color
    mocked_sending_error.assert_called_once_with("Not in DB")
