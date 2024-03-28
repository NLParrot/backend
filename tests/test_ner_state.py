
# didn't test constructor
# doesn't have intended public variables
# also python has every constructor as public

from chatapp.state_models import NERState


def test_call(mocker):
    # Mocks init since it depends on loading big file
    mock_init = mocker.patch.object(NERState, '__init__', return_value=None)
    mock_classifier = mocker.MagicMock()
    mock_classifier.return_value = [{
        "entity_group": "some_group",
        "word": "some_word"
    }]

    ner_state = NERState()
    ner_state.classifier = mock_classifier

    result = ner_state("This should classify some_word to some_group", None, None)

    assert result == {"some_group": "some_word"}

def test_call_exception(mocker):
    # Mocks init since it depends on loading big file
    mock_init = mocker.patch.object(NERState, '__init__', return_value=None)
    mock_classifier = mocker.MagicMock()
    mock_classifier.return_value = [None]

    ner_state = NERState()
    ner_state.classifier = mock_classifier

    # Should raise an exception since return_value is weird
    result = ner_state(None, None, None)

    assert result == {}


