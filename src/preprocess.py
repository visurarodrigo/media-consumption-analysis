import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df = df.fillna("Unknown")
    if 'release_year' in df.columns:
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    if 'date_added' in df.columns:
        df['year_added'] = df['date_added'].dt.year
        df['month_added'] = df['date_added'].dt.month

    if 'duration' in df.columns:
        df['duration_minutes'] = df['duration'].str.extract(r'(\d+)').astype(float)
        df['duration_type'] = df['duration'].str.extract(r'([a-zA-Z]+)')
    if 'listed_in' in df.columns:
        df['primary_genre'] = df['listed_in'].astype(str).str.split(',').str[0].str.strip()
    return df