import pickle
import pandas as pd 
from simpletransformers.classification import (
    MultiLabelClassificationModel, MultiLabelClassificationArgs
)
import pandas as pd
import logging
import random 


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

data = pickle.load(open('multi_class_data.pkl','rb'))
random.shuffle(data)

train_df.columns = ["text", "labels"]
tdata,vdata,edata = data[:4174],data[4174:5565],data[5565:]

train_df = pd.DataFrame(tdata)
train_df.columns = ["text", "labels"]

# Preparing eval data

eval_df = pd.DataFrame(vdata)
eval_df.columns = ["text", "labels"]

# Optional model configuration
model_args = MultiLabelClassificationArgs(num_train_epochs=10,sliding_window=True)

# Create a MultiLabelClassificationModel
model = MultiLabelClassificationModel(
    "bert", "sebi_bert", num_labels=50,
)

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(
    eval_df
)


