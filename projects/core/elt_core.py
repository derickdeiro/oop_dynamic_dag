import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from abc import ABC, abstractmethod
from typing import Dict, List

class ExtractData(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def extract_data(self, exec_date) -> List[Dict]:
        """Method to be implemented in the inheriting class to perform data extraction."""
        raise NotImplementedError('Método não implementado.')

class TransformData(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def transform_data(self, exec_date) -> List[Dict]:
        """Method to be implemented in the inheriting class to perform data transformation."""
        
        raise NotImplementedError('Método não implementado.')


class LoadData(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def load_data(self, exec_date) -> str:
        """Este é um método abstrato que deve ser implementado na classe herdeira para realizar as transformações necessárias e criar um DataFrame.

        Returns:
            pd.DataFrame: DataFrame que será utilizado para gerar o Output padrão.
        """       
        
        raise NotImplementedError('Método não implementado.')
