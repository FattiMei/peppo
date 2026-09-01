class Function:
    def __init__(self, signature: tuple["Argument"], body: "Value" = None, name: str = None):
        self.signature = signature
        self.name = name

        if body is not None:
            self.set_body(body)

    def set_body(self, body: "Value"):
        """
        This function could potentially check the correctness of the function body.
        In particular I can check that every value is either a constant or depends on an argument
        """
        self.body = body

    def __call__(self, *args) -> "FunctionCall":
        return FunctionCall(self, args)

    def lower_to_llvm(self) -> "":
        return None


