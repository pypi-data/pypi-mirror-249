import sys

import pytest
from imppkg.harmony import main
from termcolor import colored


@pytest.mark.parametrize(
    "inputs,expected_value",
    [
        (["1", "4", "4"], 2.0),
        (["1", "four", "4"], 0.0),
        (["0", "0", "0"], 0.0),
    ],
)
def test_inputs(inputs, expected_value, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)
    main()

    assert capsys.readouterr().out.strip() == colored(
        expected_value, "red", "on_cyan", attrs=["bold"]
    )
