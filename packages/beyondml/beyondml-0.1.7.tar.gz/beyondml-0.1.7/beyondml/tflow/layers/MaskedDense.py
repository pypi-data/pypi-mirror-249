import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer


class MaskedDense(Layer):
    """
    Masked fully connected layer. For full documentation of the fully-connected architecture, see the
    TensorFlow Keras Dense layer documentation.

    This layer implements masking consistent with the BeyondML API to support developing sparse models.


    """

    def __init__(
            self,
            units,
            use_bias=True,
            activation=None,
            kernel_initializer='random_normal',
            mask_initializer='ones',
            bias_initializer='zeros',
            **kwargs
    ):
        """
        Parameters
        ----------
        units : int
            The number of artificial neurons to use
        use_bias : bool (default True)
            Whether to use a bias calculation in the outputs
        activation : None, str, or function (default None)
            The activation function to use on the outputs
        kernel_initializer : str or keras initialization function (default 'random_normal')
            The weight initialization function to use
        mask_initializer : str or keras initialization function (default 'ones')
            The mask initialization function to use
        bias_initializer : str or keras initialization function (default 'zeros')
            The bias initialization function to use

        """
        super(MaskedDense, self).__init__(**kwargs)
        self.units = int(units) if not isinstance(units, int) else units
        self.use_bias = use_bias
        self.activation = tf.keras.activations.get(activation)
        self.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self.mask_initializer = tf.keras.initializers.get(mask_initializer)
        self.bias_initializer = tf.keras.initializers.get(bias_initializer)

    def build(self, input_shape):
        """
        Build the layer in preparation to be trained or called. Should not be called directly,
        but rather is called when the layer is added to a model
        """
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer=self.kernel_initializer,
            trainable=True,
            name='weights'
        )
        self.w_mask = self.add_weight(
            shape=self.w.shape,
            initializer=self.mask_initializer,
            trainable=False,
            name='weights_mask'
        )

        if self.use_bias:
            self.b = self.add_weight(
                shape=(self.units,),
                initializer=self.bias_initializer,
                trainable=True,
                name='bias'
            )
            self.b_mask = self.add_weight(
                shape=self.b.shape,
                initializer=self.mask_initializer,
                trainable=False,
                name='bias_mask'
            )

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
        if self.use_bias:
            return self.activation(tf.matmul(inputs, self.w * self.w_mask) + (self.b * self.b_mask))
        else:
            return self.activation(tf.matmul(inputs, self.w * self.w_mask))

    def get_config(self):
        config = super().get_config().copy()
        config.update(
            {
                'units': self.units,
                'use_bias': self.use_bias,
                'activation': tf.keras.activations.serialize(self.activation),
                'kernel_initializer': tf.keras.initializers.serialize(self.kernel_initializer),
                'mask_initializer': tf.keras.initializers.serialize(self.mask_initializer),
                'bias_initializer': tf.keras.initializers.serialize(self.bias_initializer)
            }
        )
        return config

    def set_masks(self, new_masks):
        """
        Set the masks for the layer

        Parameters
        ----------
        new_masks : list of arrays or array-likes
            The new masks to set for the layer
        """
        if not self.use_bias:
            self.set_weights(
                [self.w.numpy() * new_masks[0].astype(np.float32),
                 new_masks[0].astype(np.float32)]
            )
        else:
            self.set_weights(
                [self.w.numpy() * new_masks[0].astype(np.float32), self.b.numpy() * new_masks[1].astype(
                    np.float32), new_masks[0].astype(np.float32), new_masks[1].astype(np.float32)]
            )

    @classmethod
    def from_config(cls, config):
        return cls(
            units=config['units'],
            use_bias=config['use_bias'],
            activation=config['activation'],
            kernel_initializer=config['kernel_initializer'],
            mask_initializer=config['mask_initializer'],
            bias_initializer=config['bias_initializer']
        )
