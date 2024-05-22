class Neuron:
    def __init__(self, inputs, weights, bias):
        self.inputs = inputs
        self.weights = weights
        self.bias = bias

    def activate(self):
        # Calculate the weighted sum of the inputs.
        weighted_sum = 0
        for i in range(len(self.inputs)):
            weighted_sum += self.inputs[i] * self.weights[i]

        # Add the bias.
        weighted_sum += self.bias

        # Apply the activation function.
        output = self.activation_function(weighted_sum)

        return output

    def activation_function(self, weighted_sum):
        # This is just a simple example of an activation function.
        if weighted_sum > 0:
            return 1
        else:
            return 0
