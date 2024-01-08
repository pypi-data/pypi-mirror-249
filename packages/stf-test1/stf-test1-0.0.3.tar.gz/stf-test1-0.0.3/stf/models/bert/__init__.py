from .tokenization_bert import BasicTokenizer, BertTokenizer
from .tokenization_bert import BasicTokenizer, BertTokenizer, WordpieceTokenizer
from ...utils import is_tokenizers_available, OptionalDependencyNotAvailable

try:
    if not is_tokenizers_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    from .tokenization_bert_fast import BertTokenizerFast
