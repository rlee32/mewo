import reader
training_data, validation_data, test_data = \
  reader.get_neural_network_data("../vault")

import network2
net = network2.Network([25, 10, 3], cost=network2.CrossEntropyCost)
net.SGD(training_data, \
  epochs=30, mini_batch_size=10, eta=0.5, lmda=5.0, \
  evaluation_data=validation_data, monitor_evaluation_accuracy=True)

