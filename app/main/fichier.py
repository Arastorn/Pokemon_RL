from path import Path


def get_team_files():
    teamdir = Path("teams")
    if not teamdir.exists():
        teamdir.mkdir()
    files = teamdir.files()
    files = [file.name for file in files]
    return files
