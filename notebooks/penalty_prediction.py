from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import random

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)


data = json.load(open('facts.json'))
penalty = json.load(open('penalty.json'))
penalty_numb = []
for i in penalty:
    try:
        val = float(i)
        penalty_numb.append(i)
    except:
        penalty_numb.append(0)
pen_data = list(zip(data,penalty_numb))
random.shuffle(pen_data)
num_exp = len(pen_data)

train_data = pen_data[:int(0.8*num_exp)]
eval_data = pen_data[len(train_data):]
# Preparing train data
aFrame(train_data)
train_df.columns = ["text", "labels"]

# Preparing eval data

eval_df = pd.DataFrame(eval_data)
eval_df.columns = ["text", "labels"]

# Enabling regression
# Setting optional model configuration
model_args = ClassificationArgs()
model_args.num_train_epochs = 10
model_args.regression = True

# Create a ClassificationModel
model = ClassificationModel(
    "roberta",
    "roberta-base",
    num_labels=1,
    args=model_args
)

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df)
