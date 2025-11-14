from abc import ABC, abstractmethod
from typing import TypedDict, List, Dict, Any, Tuple, Iterable
from kiwipiepy import Kiwi

class SparseTokenizer(ABC):
	@abstractmethod
	def tokenize(self, text: str) -> str:
		'''
		문자열 하나 토큰화해서 띄어쓰기로 구분하는 토큰 문자열 반환
		'''
		pass

class KiwiTokenizer(SparseTokenizer):
	def __init__(self, included_pos_tags: Tuple[str, ...]=('NNG', 'NNP', 'NNB', 'SN', 'SL', 'SH', 'W_EMAIL', 'W_SERIAL'), dictionary_path: str=''):
		self.kiwi = Kiwi()
		self.included_pos_tags = included_pos_tags
		if dictionary_path:
			self.kiwi.load_user_dictionary(dictionary_path)
		
	def tokenize(self, text: str) -> str:
		'''
		문자열 하나 토큰화해서 띄어쓰기로 구분하는 토큰 문자열 반환
		'''
		tokenized_text = self.kiwi.tokenize(text)
		return " ".join([token.form for token in tokenized_text if token.tag in self.included_pos_tags])