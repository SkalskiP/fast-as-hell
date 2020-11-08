from src.utils.general import exists, get_or_else


class TestGeneral:

    def test_exists_when_item_exist(self):
        # when
        result = exists("lorem")

        # then
        assert result

    def test_exists_when_item_do_not_exist(self):
        # when
        result = exists(None)

        # then
        assert result is False

    def test_get_or_else_with_not_none_default_element(self):
        # when
        result = get_or_else("lorem", "ipsum")

        # then
        assert result == "lorem"

    def test_get_or_else_with_none_default_element(self):
        # when
        result = get_or_else(None, "ipsum")

        # then
        assert result == "ipsum"