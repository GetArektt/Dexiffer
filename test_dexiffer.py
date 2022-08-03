import pytest
import dexiffer




def test_valid_ifd_key():
    my_dict = {"0th": {271: "Samsung"}, "Exif": {42036: "Sony", 42037: None}}
    assert dexiffer.valid_ifd_key(my_dict["0th"][271]) is True
    assert dexiffer.valid_ifd_key(my_dict["Exif"][42036]) is True
    assert dexiffer.valid_ifd_key(my_dict["Exif"][42037]) is False
    with pytest.raises(TypeError):
        dexiffer.valid_ifd_key(True)


def test_valid_string():
    assert dexiffer.valid_string("b\'Foo\'") == "Foo"
    assert dexiffer.valid_string("Normal_string123") == "Normal_string123"
    with pytest.raises(TypeError):
        dexiffer.valid_string(None)
