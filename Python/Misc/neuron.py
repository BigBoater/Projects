def neuron_clas_1d(w0, x):
    """Artifical neuron for 1d classifcation."""
    return (w0 * x > 0).astype(int)
