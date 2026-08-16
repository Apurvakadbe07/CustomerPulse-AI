from pathlib import Path

p = Path(r"pages\06_Exploratory Data Analysis.py")
s = p.read_text(encoding="utf-8")

old_data = r'''DATA_PATH = Path(
    r"D:\customer pulse AI project\1 data\02_processed data\customer_360.csv"
)'''

new_data = '''DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "1 data"
    / "02_processed data"
    / "customer_360.csv"
)'''

old_export = r'''export_path = Path(
    r"D:\customer pulse AI project"
) / "1 data" / "03_analysis" / "customer_360_clean.csv"'''

new_export = '''export_path = (
    Path(__file__).resolve().parents[1]
    / "1 data"
    / "03_analysis"
    / "customer_360_clean.csv"
)'''

if old_data in s:
    s = s.replace(old_data, new_data)
    print("DATA_PATH fixed")
else:
    print("DATA_PATH pattern not found")

if old_export in s:
    s = s.replace(old_export, new_export)
    print("export_path fixed")
else:
    print("export_path pattern not found")

p.write_text(s, encoding="utf-8")
print("File saved.")
