"""Exercise 01: class, object and methods."""


class Progress:
    """Track completed work out of a total amount."""

    def __init__(self, completed: int, total: int) -> None:
        if total < 1:
            raise ValueError("total must be positive")
        self.completed = completed
        self.total = total

    def percentage(self) -> float:
        """Return completion as a percentage."""
        return self.completed / self.total * 100

    def __str__(self) -> str:
        """Return a short, readable progress summary."""
        return (
            f"Progress: {self.completed}/{self.total} "
            f"({self.percentage():.0f}%)"
        )


if __name__ == "__main__":
    progress = Progress(3, 4)
    print(progress.percentage())
    print(progress)
