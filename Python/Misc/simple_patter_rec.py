import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

# Load the dataset
digits = datasets.load_digits()

# Display a sample image
plt.imshow(digits.images[0], cmap=plt.cm.gray_r, interpolation='nearest')
plt.title('Sample Digit')
plt.show()

# Flatten the images, each image is 8x8 pixels
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# Split data into 50% train and 50% test subsets
X_train, X_test, y_train, y_test = train_test_split(data, digits.target, test_size=0.5, random_state=42)

# Train the classifier
classifier.fit(X_train, y_train)

# Predict the value of the digit on the test subset
predicted = classifier.predict(X_test)

# Display the first few test images and predictions
for index, (image, prediction) in enumerate(zip(X_test[:5], predicted[:5])):
    plt.subplot(1, 5, index + 1)
    plt.axis('off')
    plt.imshow(image.reshape(8, 8), cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title(f'Prediction: {prediction}')

plt.show()

# Print classification report
print(f"Classification report for classifier {classifier}:\n"
      f"{metrics.classification_report(y_test, predicted)}\n")

# Print confusion matrix
disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
disp.figure_.suptitle("Confusion Matrix")
plt.show()
