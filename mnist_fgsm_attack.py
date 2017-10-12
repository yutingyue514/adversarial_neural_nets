import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from mnist import build_network, calc_loss
from tensorflow.examples.tutorials.mnist import input_data as mnist_data

# Importing MNIST datasets
mnist = mnist_data.read_data_sets('MNIST_data', one_hot=True)

# Tuned hyperparameters from mnist.py
input_dimension = 784
output_dimension = 10
learning_rate = 0.001
batch_size = 100
l1 = 200
l2 = 300
l3 = 10

def fgsm_attack(image, label):
    """ Perform fast gradient sign method attack on an (image, label) pair to lead mnist classifier to misclassify
    params: image, label pair
    return: perturbed_image
    """
    tf.reset_default_graph()

    # Building the graph
    x = tf.placeholder(tf.float32, [None, input_dimension], name="input")
    y = tf.placeholder(tf.float32, [None, output_dimension], name="labels")
    z3, y_ = build_network(x, l1, l2, l3)
    loss = calc_loss(z3, y)

    epsilon = 0.25

    pertubation = tf.sign(tf.gradients(loss, x))

    #apply pertubation to images
    perturbed_op = tf.squeeze(epsilon * pertubation) + image

    sess=tf.Session()   
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()
    saver.restore(sess, "./tmp/original_mnist_model-8")

    perturbed_image = sess.run(perturbed_op, feed_dict={x: [image], y:[label]})
    return perturbed_image

def predict_mnist_num(image):
    """ Run the mnist model and predict on one single image
    Return: [[]] of 10 numbers indicating the probabilities from 0 - 9
    """
    tf.reset_default_graph()

    # Building the graph
    x = tf.placeholder(tf.float32, [None, input_dimension], name="input")
    y = tf.placeholder(tf.float32, [None, output_dimension], name="labels")
    z3, y_ = build_network(x, l1, l2, l3)

    sess=tf.Session()   
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()
    saver.restore(sess, "./tmp/original_mnist_model-8")

    prediction = sess.run(y_, feed_dict={x: [image]})
    return prediction

def demonstrate_attack_result():
    """ Demonstrate the FGSM attack result by showing
    1. Original image and perturbed image
    2. How the predictions for which number the image is different according to the algorithm
    """
    sample_image = mnist.test.images[1, :]
    sample_label = mnist.test.labels[1, :]
    plt.imshow(sample_image.reshape(28, 28))
    plt.title('Original Image')
    plt.show()
    original_prediction = np.argmax(predict_mnist_num(sample_image), axis=1)
    print("The original picture's prediction says:" + str(original_prediction))

    perturbed_image = fgsm_attack(sample_image, sample_label)

    plt.imshow(perturbed_image.reshape(28, 28))
    plt.title('Perturbed Image')
    plt.show()
    perturbed_prediction = np.argmax(predict_mnist_num(perturbed_image), axis=1)
    print("The perturbed picture's prediction says:" + str(perturbed_prediction))

demonstrate_attack_result()