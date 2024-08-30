import pandas as pd


def extract_donor_id(s: pd.Series):
    donor_pattern = r"([BP]\d+|Ctr\d+|Control\d+)_\d+"
    return s.str.findall(donor_pattern).explode()