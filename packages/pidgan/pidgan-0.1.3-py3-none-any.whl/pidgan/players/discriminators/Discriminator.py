import tensorflow as tf
from tensorflow import keras

LEAKY_ALPHA = 0.1


class Discriminator(keras.Model):
    def __init__(
        self,
        output_dim,
        num_hidden_layers=5,
        mlp_hidden_units=128,
        mlp_dropout_rates=0.0,
        output_activation="sigmoid",
        name=None,
        dtype=None,
    ) -> None:
        super().__init__(name=name, dtype=dtype)
        self._hidden_activation_func = None
        self._hidden_kernel_reg = None
        self._model = None

        # Output dimension
        assert output_dim >= 1
        self._output_dim = int(output_dim)

        # Number of hidden layers
        assert isinstance(num_hidden_layers, (int, float))
        assert num_hidden_layers >= 1
        self._num_hidden_layers = int(num_hidden_layers)

        # Multilayer perceptron hidden units
        if isinstance(mlp_hidden_units, (int, float)):
            assert mlp_hidden_units >= 1
            self._mlp_hidden_units = [int(mlp_hidden_units)] * self._num_hidden_layers
        else:
            mlp_hidden_units = list(mlp_hidden_units)
            assert len(mlp_hidden_units) == self._num_hidden_layers
            self._mlp_hidden_units = list()
            for units in mlp_hidden_units:
                assert isinstance(units, (int, float))
                assert units >= 1
                self._mlp_hidden_units.append(int(units))

        # Dropout rate
        if isinstance(mlp_dropout_rates, (int, float)):
            assert mlp_dropout_rates >= 0.0 and mlp_dropout_rates < 1.0
            self._mlp_dropout_rates = [
                float(mlp_dropout_rates)
            ] * self._num_hidden_layers
        else:
            mlp_dropout_rates = list(mlp_dropout_rates)
            assert len(mlp_dropout_rates) == self._num_hidden_layers
            self._mlp_dropout_rates = list()
            for rate in mlp_dropout_rates:
                assert isinstance(rate, (int, float))
                assert rate >= 0.0 and rate < 1.0
                self._mlp_dropout_rates.append(float(rate))

        # Output activation
        self._output_activation = output_activation

    def _define_arch(self) -> keras.Sequential:
        model = keras.Sequential(name=f"{self.name}_seq" if self.name else None)
        for i, (units, rate) in enumerate(
            zip(self._mlp_hidden_units, self._mlp_dropout_rates)
        ):
            model.add(
                keras.layers.Dense(
                    units=units,
                    activation=self._hidden_activation_func,
                    kernel_initializer="glorot_uniform",
                    bias_initializer="zeros",
                    kernel_regularizer=self._hidden_kernel_reg,
                    name=f"dense_{i}" if self.name else None,
                    dtype=self.dtype,
                )
            )
            if self._hidden_activation_func is None:
                model.add(
                    keras.layers.LeakyReLU(
                        alpha=LEAKY_ALPHA, name=f"leaky_relu_{i}" if self.name else None
                    )
                )
            model.add(
                keras.layers.Dropout(
                    rate=rate, name=f"dropout_{i}" if self.name else None
                )
            )
        model.add(
            keras.layers.Dense(
                units=self._output_dim,
                activation=self._output_activation,
                kernel_initializer="glorot_uniform",
                bias_initializer="zeros",
                name="dense_out" if self.name else None,
                dtype=self.dtype,
            )
        )
        return model

    def _build_model(self, x) -> None:
        if self._model is None:
            self._model = self._define_arch()
        else:
            pass

    def _prepare_input(self, x) -> tf.Tensor:
        if isinstance(x, (list, tuple)):
            x = tf.concat(x, axis=-1)
        return x

    def call(self, x) -> tf.Tensor:
        x = self._prepare_input(x)
        self._build_model(x)
        out = self._model(x)
        return out

    def summary(self, **kwargs) -> None:
        self._model.summary(**kwargs)

    def hidden_feature(self, x, return_hidden_idx=False):
        x = self._prepare_input(x)
        if self._hidden_activation_func is None:
            multiple = 3  # dense + leaky_relu + dropout
        else:
            multiple = 2  # dense + dropout
        hidden_idx = int((self._num_hidden_layers + 1) / 2.0)
        if hidden_idx < 1:
            hidden_idx += 1
        for layer in self._model.layers[: multiple * hidden_idx]:
            x = layer(x)
        if return_hidden_idx:
            return x, hidden_idx
        else:
            return x

    @property
    def output_dim(self) -> int:
        return self._output_dim

    @property
    def num_hidden_layers(self) -> int:
        return self._num_hidden_layers

    @property
    def mlp_hidden_units(self) -> list:
        return self._mlp_hidden_units

    @property
    def mlp_dropout_rates(self) -> list:
        return self._mlp_dropout_rates

    @property
    def output_activation(self):
        return self._output_activation

    @property
    def export_model(self) -> keras.Sequential:
        return self._model
