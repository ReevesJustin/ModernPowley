from modern_powley.later.davis import matching_transcribed_bands, powder_selection_index


def test_davis_formula_is_separate_from_original_namespace():
    assert round(powder_selection_index(0.271, 0.328), 6) == round(20 + 12 / (0.271 * 0.328**0.5), 6)


def test_transcribed_lookup_endpoints_remain_explicitly_overlapping():
    assert len(matching_transcribed_bands(81)) == 1
    assert len(matching_transcribed_bands(91)) == 2
    assert len(matching_transcribed_bands(110)) == 2
    assert len(matching_transcribed_bands(180)) == 1
    assert len(matching_transcribed_bands(180.01)) == 1
