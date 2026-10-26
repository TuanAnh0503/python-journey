"""Exercise 03: one clear basic inheritance example."""


class Animal:
    """An animal with a name."""

    def __init__(self, name: str) -> None:
        self.name = name


class Dog(Animal):
    """A dog is an animal that can speak."""

    def speak(self) -> str:
        return f"{self.name}: woof"


if __name__ == "__main__":
    dog = Dog("Milo")
    print(dog.speak())
    print("Dog is an Animal because Dog inherits from Animal.")
