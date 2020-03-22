class SimpleImgConvPool(fluid.dygraph.Layer):
    def __init__(self,
                 num_channels,
                 num_filters,
                 filter_size,
                 pool_size,
                 pool_stride,
                 pool_padding=0,
                 pool_type='max',
                 global_pooling=False,
                 conv_stride=1,
                 conv_padding=0,
                 conv_dilation=1,
                 conv_groups=1,
                 act=None,
                 use_cudnn=False,
                 param_attr=None,
                 bias_attr=None):
        super(SimpleImgConvPool, self).__init__()

        self._conv2d = fluid.dygraph.Conv2D(
            num_channels=num_channels,
            num_filters=num_filters,
            filter_size=filter_size,
            stride=conv_stride,
            padding=conv_padding,
            dilation=conv_dilation,
            groups=conv_groups,
            param_attr=param_attr,
            bias_attr=bias_attr,
            act=act,
            use_cudnn=use_cudnn)

        self._pool2d = fluid.dygraph.Pool2D(
            pool_size=pool_size,
            pool_type=pool_type,
            pool_stride=pool_stride,
            pool_padding=pool_padding,
            global_pooling=global_pooling,
            use_cudnn=use_cudnn)

    def forward(self, inputs):
        x = self._conv2d(inputs)
        x = self._pool2d(x)
        return x

with fluid.dygraph.guard():
    epoch_num = 5
    BATCH_SIZE = 64

    mnist = MNIST()
    adam = fluid.optimizer.AdamOptimizer(learning_rate=0.001, parameter_list=mnist.parameters())
    train_reader = paddle.batch(
        paddle.dataset.mnist.train(), batch_size= BATCH_SIZE, drop_last=True)

    np.set_printoptions(precision=3, suppress=True)
    for epoch in range(epoch_num):
        for batch_id, data in enumerate(train_reader()):
            dy_x_data = np.array(
                [x[0].reshape(1, 28, 28)
                 for x in data]).astype('float32')
            y_data = np.array(
                [x[1] for x in data]).astype('int64').reshape(BATCH_SIZE, 1)

            img = fluid.dygraph.to_variable(dy_x_data)
            label = fluid.dygraph.to_variable(y_data)
            label.stop_gradient = True

            cost = mnist(img)
            loss = fluid.layers.cross_entropy(cost, label)
            avg_loss = fluid.layers.mean(loss)

            dy_out = avg_loss.numpy()

            avg_loss.backward()
            adam.minimize(avg_loss)
            mnist.clear_gradients()

            dy_param_value = {}
            for param in mnist.parameters():
                dy_param_value[param.name] = param.numpy()

            if batch_id % 20 == 0:
                print("Loss at step {}: {}".format(batch_id, avg_loss.numpy()))
    print("Final loss: {}".format(avg_loss.numpy()))
    print("_simple_img_conv_pool_1_conv2d W's mean is: {}".format(mnist._simple_img_conv_pool_1._conv2d._filter_param.numpy().mean()))
    print("_simple_img_conv_pool_1_conv2d Bias's mean is: {}".format(mnist._simple_img_conv_pool_1._conv2d._bias_param.numpy().mean()))