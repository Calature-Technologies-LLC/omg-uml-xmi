def test_conf_py_exists():
    import os
    assert os.path.exists("docs/conf.py"), "docs/conf.py should exist"