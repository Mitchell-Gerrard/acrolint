from acrolint import acrolint
from acrolint import output_file


acros=acrolint(["tests/test_files/main.tex"])
print(acros)
output_file("tests/test_files/output.json", acros)