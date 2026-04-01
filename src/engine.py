import pandas as pd

class DataEngine:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self._load_and_clean()

    def _load_and_clean(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.file_path)
            cols = [
                'Be', 'He', 'Ce', 'Oe', 'Cd', 'Od', 'De', 'Dd', 'Ee', 'Fe', 'Ge', 'Ie', 'Id', 'Ke', 'Le', 'Me', 'Md', 'Ne', 'Nd', 'Pe', 'Qe', 'Qd', 'Re', 'Ue',
                'bd', 'ne', 'ce', 'oe', 'de', 'dd', 'ee', 'ge', 'hd', 'id', 'je', 'jd', 'ke', 'le', 'ld', 'me', 'md', 'nd', 'pd', 'qe', 'qd', 're', 'ue', 'ud'
            ]
            for col in cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        except Exception as e:
            return pd.DataFrame()

    def get_analise_subset(self):
        if 'manter_na_analise?' in self.df.columns:
            return self.df[self.df['manter_na_analise?'] == 'Sim'].copy()
        return self.df.copy()