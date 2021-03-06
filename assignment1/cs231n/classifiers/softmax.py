import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  for i in xrange(num_train):
    scores = X[i].dot(W)
    scores -= scores.max()
    scores_exp_sum = np.sum(np.exp(scores))
    correct_class_score_exp = np.exp(scores[y[i]])

    # compute gradient for correct class
    dW[:, y[i]] += (-1) * ((scores_exp_sum - correct_class_score_exp) / scores_exp_sum ) * X[i]
    for j in xrange(num_classes):
      if j == y[i]:
        continue

      # compute gradient for not correct classes
      dW[:, j] += (np.exp(scores[j]) / scores_exp_sum) * X[i]

    loss += -np.log(correct_class_score_exp / scores_exp_sum)

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  dW += 2 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # loss
  # score: N by C matrix containing class scores
  scores = X.dot(W)
  scores -= scores.max()

  scores = np.exp(scores)
  scores_correct_classes = scores[range(num_train), y]

  scores_sums = np.sum(scores, axis=1)

  loss = scores_correct_classes / scores_sums
  loss = -np.sum(np.log(loss))

  loss /= num_train

  loss += reg * np.sum(W * W)

  # grad
  scores = np.divide(scores, scores_sums.reshape(num_train, 1))
  scores[range(num_train), y] = (-1) * (scores_sums - scores_correct_classes) / scores_sums
  dW = X.T.dot(scores)
  
  dW /= num_train
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

