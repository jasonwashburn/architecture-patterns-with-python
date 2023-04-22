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
    session.install("pytest")
    session.install("pytest-xdist")
    session.install("pytest-cov")
    session.run("pytest", "--cov", "--cov-report", "term-missing")


@nox.session
def mypy(session) -> None:
    session.install("mypy")
    session.run("mypy", ".")
