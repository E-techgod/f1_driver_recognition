from pathlib import Path


def test_project_has_core_files(project_root: Path):
    for fname in ["recognizeFace.py", "addFaces.py", "server.py", "dashboard.py"]:
        assert (project_root / fname).exists(), f"Missing {fname} in project root"


def test_cascade_file_exists(project_root: Path):
    cascade = project_root / "data" / "haarcascade_frontalface_default.xml"
    assert cascade.exists(), "Missing Haar cascade XML in data/ (commit this file!)"


def test_assets_folders_exist(project_root: Path):
    assert (project_root / "data" / "logos").exists()
    assert (project_root / "data" / "flags").exists()
