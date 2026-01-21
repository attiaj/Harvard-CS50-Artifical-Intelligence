import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_to_index = {month: i for i, month in enumerate(months)}

        evidence_list = []
        label_list = []

        # Make the correct adjustments for rows that aren't simple floats or ints, 
        # Then add a list of evidence values for each row, followed by a boolean for each row's label
        for row in reader:
            evidence_row = []

            for i, cell in enumerate(row[:17]):
                if i == 10:     # Month row
                    evidence_row.append(month_to_index.get(cell, 0))
                elif i == 15:   # VisitorType row
                    evidence_row.append(1 if cell == "Returning_Visitor" else 0)
                elif i == 16:   # Weekend row
                    evidence_row.append(1 if cell == "TRUE" else 0)
                elif i in [0, 2, 4, 12, 13, 14]:
                    evidence_row.append(int(cell))
                else:
                    evidence_row.append(float(cell))

            label_list.append(1 if row[17] == "TRUE" else 0)
            
            evidence_list.append(evidence_row)

        return (evidence_list, label_list)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Initialize a model on the K-Nearest-Neighbors classifier from scikit-learn,
    # fit the model using data that's already split
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    total_positives = 0
    total_correct_positives = 0
    total_negatives = 0
    total_correct_negatives = 0

    # Calculate total positives and negatives, and check against predictions to see which were guessed correctly
    for i, actual_label in enumerate(labels):
        if actual_label == 1:
            total_positives += 1
            if predictions[i] == 1:
                total_correct_positives += 1
        else:
            total_negatives += 1
            if predictions[i] == 0:
                total_correct_negatives += 1

    return (float(total_correct_positives / total_positives), float(total_correct_negatives / total_negatives))


if __name__ == "__main__":
    main()
