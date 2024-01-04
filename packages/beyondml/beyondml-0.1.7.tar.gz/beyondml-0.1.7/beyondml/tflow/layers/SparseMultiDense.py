from tensorflow.keras.layers import Layer
import tensorflow as tf


class SparseMultiDense(Layer):
    """
    Sparse implementation of the MultiDense layer. If used in a model, must be saved and loaded via pickle
    """

    def __init__(
        self,
        weight,
        bias,
        activation=None,
        **kwargs
    ):
        """
        Parameters
        ----------
        weight : tf.Tensor
            The kernel tensor
        bias : tf.Tensor
            The bias tensor
        activation : None, str or keras activation function (default None)
            The activation function to use

        """
        super().__init__(**kwargs)
        self.w = {
            i: tf.sparse.from_dense(weight[i]) for i in range(weight.shape[0])
        }
        self.b = {
            i: tf.sparse.from_dense(bias[i]) for i in range(bias.shape[0])
        }
        self.activation = tf.keras.activations.get(activation)

    def build(self, input_shape):
        """
        Build the layer in preparation to be trained or called. Should not be called directly,
        but rather is called when the layer is added to a model
        """
        pass

    def call(self, inputs):
        """
        This is where the layer's logic lives and is called upon inputs

        Parameters
        ----------
        inputs : TensorFlow Tensor or Tensor-like
            The inputs to the layer

        Returns
        -------
        outputs : TensorFlow Tensor
            The outputs of the layer's logic
        """

        output_tensor = [
            tf.matmul(inputs[i], tf.sparse.to_dense(self.w[i])) + tf.sparse.to_dense(self.b[i]) for i in range(len(inputs))
        ]
        return [
            self.activation(tensor) for tensor in output_tensor
        ]

    def get_config(self):
        config = super().get_config().copy()
        config['activation'] = tf.keras.activations.serialize(self.activation)
        return config

    @classmethod
    def from_layer(cls, layer):
        """
        Create a layer from an instance of another layer
        """
        weights = layer.get_weights()
        w = weights[0]
        b = weights[1]
        activation = layer.activation
        return cls(
            w,
            b,
            activation
        )

    @classmethod
    def from_config(cls, config):
        return cls(**config)
