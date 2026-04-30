import pandas as pd

class DataEngine:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self._load_and_clean()

    def _load_and_clean(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.file_path)
            cols = [
                'Be', 'He', 'Ce', 'Oe', 'Cd', 'Od', 'De', 'Dd', 'Ee', 'Fe', 'Ge', 'Ie', 'Id', 
                'Jd', 'Hd', 'Ke', 'Le', 'Me', 'Md', 'Pe', 'Pd', 'Qe', 'Qd', 'Re', 'Ue',
                'be', 'bd', 'ne', 'nd', 'ce', 'oe', 'de', 'dd', 'ee', 'id', 'je', 'jd', 
                'ke', 'le', 'ld', 'me', 'md', 'pd', 'qe', 'qd', 're', 'ue', 'ud'
            ]
            for col in cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return pd.DataFrame()

    def get_analise_subset(self):
        if 'manter_na_analise?' in self.df.columns:
            return self.df[self.df['manter_na_analise?'] == 'Sim'].copy()
        return self.df.copy()

    def get_fontforge_data(self) -> pd.DataFrame:
        """Lê exclusivamente os dados extraídos pelo FontForge para visualização na tabela."""
        try:
            return pd.read_csv("data/metricas_fontes_lote.csv")
        except Exception as e:
            print(f"Aviso - Arquivo do FontForge não encontrado ou erro ao carregar: {e}")
            return pd.DataFrame()