from domains.update_action.utils.pin_code import generate_pin_code


def test_generate_pin_code_length():
    pin_code = generate_pin_code()
    assert len(pin_code) == 6, "Пинкод должен быть длиной 6 символов"


def test_generate_pin_code_is_digit():
    pin_code = generate_pin_code()
    assert pin_code.isdigit(), "Пинкод должен содержать только цифры"
