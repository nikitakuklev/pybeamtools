class SimController:
    def __init__(self, inputs, outputs, eval_fn=None) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.eval_fn = eval_fn

    def read(self, name):
        # print(f'SimCtr: request for {name}')
        assert name in self.outputs
        return self.eval_fn(name)
