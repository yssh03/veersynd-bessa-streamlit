from transformers import TokenClassificationPipeline
from transformers.pipelines import AggregationStrategy
import numpy as np




class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, tokenizer, *args, **kwargs):
        super().__init__(
            model=model,
            tokenizer=tokenizer,
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])
