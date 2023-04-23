import nox

nox.options.sessions = ["fmt", "lint", "mypy", "test"]


@nox.session
def fmt(session) -> None:
    session.install("black")
    session.run("black", ".")


@nox.session
def lint(session) -> None:
    session.install("ruff")
    session.run("ruff", ".")


@nox.session
def test(session) -> None:
    session.install("-r", "requirements.txt")
    session.install("-r", "dev-requirements.txt")
    session.run(
        "pytest",
        "--cov",
        "--cov-report",
        "term-missing",
        "--cov-report",
        "xml:cov.xml",
    )


@nox.session
def update_deps(session) -> None:
    session.install("pip-tools")
    session.run("pip-compile", "--upgrade", "-o", "requirements.txt", "pyproject.toml")
    session.run(
        "pip-compile",
        "--upgrade",
        "--extra=dev",
        "-o",
        "dev-requirements.txt",
        "pyproject.toml",
    )


@nox.session
def mypy(session) -> None:
    session.install("-r", "requirements.txt")
    session.install("-r", "dev-requirements.txt")
    session.run("mypy", ".")
