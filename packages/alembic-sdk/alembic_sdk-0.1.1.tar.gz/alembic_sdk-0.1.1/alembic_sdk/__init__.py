import os

from loguru import logger

from alembic_sdk.config import MIGRATIONS_DIR


def remove_migration_directory(directory_name=MIGRATIONS_DIR):
    """Remove an existing migration directory."""
    import shutil

    if os.path.isdir(directory_name):
        logger.debug(f"Removing migration directory at {directory_name}")
        shutil.rmtree(directory_name)
    else:
        logger.debug(f"No migration directory found at {directory_name}")


def remove_alembic_ini():
    """Remove an existing alembic.ini file."""

    if os.path.isfile("alembic.ini"):
        logger.debug("Removing alembic.ini file")
        os.remove("alembic.ini")
    else:
        logger.debug("No alembic.ini file found")


def remove_alembic_files():
    """Remove an existing alembic.ini file and migration directory."""
    remove_migration_directory()
    remove_alembic_ini()


def create_migration_directory(directory_name=MIGRATIONS_DIR):
    """Create a new migration directory."""
    from alembic import command
    from alembic.config import Config

    # Initialize Alembic configuration
    alembic_config = Config()
    alembic_config.set_main_option("script_location", MIGRATIONS_DIR)
    alembic_config.config_file_name = "alembic.ini"  # Set the config file name

    # Create the Alembic environment
    logger.debug(f"Creating migration directory at {directory_name}")
    command.init(alembic_config, MIGRATIONS_DIR)

    # add "import sqlmodel" to script.py.mako
    logger.debug(f"Updating script.py.mako file")
    with open(f"{directory_name}/script.py.mako", "r") as file:
        filedata = file.read()
    line = "import sqlalchemy as sa"
    filedata = filedata.replace(line, f"{line}\nimport sqlmodel")
    with open(f"{directory_name}/script.py.mako", "w") as file:
        file.write(filedata)


def edit_env_py(
    url,
    import_models_file: str,
    directory_name=MIGRATIONS_DIR,
):
    """
    Edit the env.py file to add the database url and import models.

    Args:
        url (str): The database url.
            E.g.: "sqlite:///database/database.db"
        import_models_file (str): The file to import models from.
            E.g.: "folder/file_that_import_models.py"
    """
    # read .env_template.py file
    with open("alembic_sdk/env_template.py", "r") as file:
        filedata = file.read()

    # after config = context.config,
    # add config.set_main_option("sqlalchemy.url", url)
    line = "config = context.config"
    extra_line = f'config.set_main_option("sqlalchemy.url", "{url}")'
    filedata = filedata.replace(line, f"{line}\n{extra_line}")

    # After the line "### INSERT NEW MODELS below ###"
    # add the models from the models.py file
    line = "### INSERT NEW MODELS below ###"
    with open(import_models_file, "r") as file:
        models_filedata = file.read()
    filedata = filedata.replace(line, f"{line}\n\n{models_filedata}")

    # write the content to env.py
    with open(f"{directory_name}/env.py", "w") as file:
        file.write(filedata)


def create_engine(url):
    """Create a database engine."""
    import sqlmodel

    return sqlmodel.create_engine(url)


def create_db(url):
    """Create a database."""

    engine = create_engine(url)

    if url.startswith("sqlite:///"):
        # Create local folder for sqlite database
        folder_name = os.path.dirname(url).replace("sqlite:///", "")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


def delete_pycache_folders():
    import shutil

    directory_name: str = MIGRATIONS_DIR
    if os.path.isdir(f"{directory_name}/__pycache__"):
        shutil.rmtree(f"{directory_name}/__pycache__")


def generate_revision(revision_name: str = "", directory_name: str = MIGRATIONS_DIR):
    """Generate a new revision using autogenerate."""

    import alembic

    delete_pycache_folders()

    number_of_revisions = len(
        [
            file
            for file in os.listdir(f"{directory_name}/versions")
            if file.endswith(".py")
        ]
    )
    alembicArgs = [
        "--raiseerr",
        "revision",
        "--autogenerate",
        "-m",
        f"v{number_of_revisions + 1}" if not revision_name else f"{revision_name}",
    ]
    try:
        alembic.config.main(argv=alembicArgs)
        return True
    except Exception as e:
        print(e)
        return False


def upgrade_head():
    import alembic

    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    try:
        alembic.config.main(argv=alembicArgs)
        return True
    except Exception as e:
        print(e)
        return False
