from pathlib import Path
import pandas as pd
import re

def load_documentation_files(repository_path: str = None) -> pd.DataFrame:
    """
    Load all project_documentation.md files for each project within the repository.
    Each file becomes one row with 'project_name' and 'description'.

    Parameters
    ----------
    repository_path: str
        Repository path as a string. If no value is passed, the repository path is found automatically.

    Returns
    -------
    projects: pd.DataFrame
        Pandas dataframe with name and description for each project in the repository.
    """

    if repository_path is None:
        repository_path = find_repository_path()

    projects = []

    for project_folder in repository_path.iterdir():
        if not project_folder.is_dir(): continue
        
        documentation = project_folder / "docs" / "project-description.md"
        readme = project_folder / "README.md"
        
        if documentation.is_file():
            with documentation.open("r", encoding="utf-8") as f:
                lines = f.readlines()

                if not lines: continue

                project_name = clean_md(lines[0].strip())
                description = clean_md("".join(lines[1:]).strip())
        else: continue

        if readme.is_file():
            with readme.open("r", encoding="utf-8") as f:
                lines = f.readlines()

                if not lines: continue

                introduction = clean_md("".join(lines[1:]).strip())
        else: continue

        projects.append({
            "project_name": project_name,
            "description": description,
            "introduction": introduction,
            "folder": project_folder.name
        })

    return pd.DataFrame(projects)


def clean_md(text: str) -> str:
    """
    Remove common Markdown characters like #, *, -, ` from the text.

    Parameters
    ----------
    text: str
        Raw text to be cleaned.

    Returns
    -------
    clean_text: str
        Pre-processed text after cleaning.
    """

    # Remove headings (# at start of line)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove bullets (* or - at start of line)
    text = re.sub(r'^[\*\-]\s+', '', text, flags=re.MULTILINE)
    # Remove inline code/backticks
    text = re.sub(r'`+', '', text)
    # Remove bold/italic marks
    text = text.replace('*', '').replace('_', '')
    # Remove line breaks
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def find_repository_path() -> Path:
    """
    Automatically finds the repository path by finding the current file's path and going up the folder structure.

    Returns
    -------
    repository_path: Path
        Path of the DS-ML-portfolio repository.
    """
    return Path(__file__).resolve().parent.parent.parent
