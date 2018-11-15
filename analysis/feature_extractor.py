import pandas as pd

class FeatureExtractor:
    def __init__(self, file):
        self.file = file

    
    def set_file(self, file):
        self.file=file

    def make_df(self):
        with open(self.file) as f:
            df = pd.read_csv(f)

        gb = df.groupby(['file', 'line'])
        groups = {x:gb.get_group(x) for x in gb.groups}

        result = []

        for key, group in groups.items():
            entry = {'file':key[0], 'line':key[1], 'heart_rate':group['heart_rate'].mean(),
            'heart_rate_variability':group['heart_rate_variability'].mean(),
            'gsr':group['gsr_electrode'].mean(), 'skin_temperature':group['object_temperature'].mean(), 'duration':group['timestamp_ms'].count() * 1/90}
            result.append(entry)

        df = pd.DataFrame(result)
        df = df[['file', 'line', 'heart_rate', 'heart_rate_variability', 'gsr', 'skin_temperature', 'duration']]
        return df

    def extract_features(self):
        df = self.make_df()
        return df[['heart_rate', 'heart_rate_variability', 'gsr', 'skin_temperature', 'duration']]
        
    
    def extract_targets(self):
        df = self.make_df()
        return df[['file', 'line']]