import paddlehub as hub

from paddlehub.dataset.base_nlp_dataset import BaseNLPDataset
import paddle.fluid as fluid


class DemoDataset(BaseNLPDataset):
    """DemoDataset"""

    def __init__(self):
        # 数据集存放位置
        self.dataset_dir = "./example_data"
        super(DemoDataset, self).__init__(
            base_path=self.dataset_dir,
            train_file="train.tsv",
            dev_file="val.tsv",
            # 数据集类别集合
            label_list=[str(i) for i in range(11)])


dataset = DemoDataset()

module = hub.Module(name="ernie_tiny")
inputs, outputs, program = module.context(trainable=True, max_seq_len=128)

# For ernie_tiny, it use sub-word to tokenize chinese sentence
# If not ernie tiny, sp_model_path and word_dict_path should be set None
reader = hub.reader.ClassifyReader(
    dataset=dataset,
    vocab_path=module.get_vocab_path(),
    max_seq_len=128,
    sp_model_path=module.get_spm_path(),
    word_dict_path=module.get_word_dict_path())

# Construct transfer learning network
# Use "pooled_output" for classification tasks on an entire sentence.
# Use "sequence_output" for token-level output.
pooled_output = outputs["pooled_output"]

# Setup feed list for data feeder
# Must feed all the tensor of module need
feed_lists = [
    inputs["input_ids"].name,
    inputs["position_ids"].name,
    inputs["segment_ids"].name,
    inputs["input_mask"].name,
]

# Select finetune strategy, setup config and finetune
strategy = hub.AdamWeightDecayStrategy(
    warmup_proportion=0.1,
    weight_decay=0.01,
    learning_rate=5e-5)

# Setup runing config for PaddleHub Finetune API
configs = hub.RunConfig(
    use_data_parallel=False,
    use_cuda=True,
    num_epoch=1000,
    batch_size=32,
    checkpoint_dir=None,
    strategy=strategy)


# Define a classfication finetune task by PaddleHub's API
class Task(hub.TextClassifierTask):
    def __init__(self,
                 feature,
                 num_classes,
                 feed_list,
                 data_reader,
                 startup_program=None,
                 config=None,
                 hidden_units=None,
                 metrics_choices="default"):
        super(Task, self).__init__(
            data_reader=data_reader,
            feature=feature,
            num_classes=num_classes,
            feed_list=feed_list,
            startup_program=startup_program,
            config=config,
            hidden_units=hidden_units,
            metrics_choices=["acc", "F2", "F3"])

    def _add_metrics(self):
        acc = fluid.layers.accuracy(input=self.outputs[0], label=self.labels[0])
        F2 = fluid.layers.accuracy(input=self.outputs[0], label=self.labels[0], k=2)
        F3 = fluid.layers.accuracy(input=self.outputs[0], label=self.labels[0], k=3)
        return [acc, F2, F3]


cls_task = Task(
    data_reader=reader,
    feature=pooled_output,
    feed_list=feed_lists,
    num_classes=dataset.num_labels,
    config=configs)

# Finetune and evaluate by PaddleHub's API
# will finish training, evaluation, testing, save model automatically
cls_task.finetune_and_eval()
