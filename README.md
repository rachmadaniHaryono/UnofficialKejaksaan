# UnofficialKejaksaan
web scraper for kejaksaan.go.id

# Usage

```python
from unofficialKejaksaan import PidanaUmum
# load from page 1
PidanaUmum.load_page(1)
# get first berkas
berkas = PidanaUmum.daftar_berkas[0]
 print berkas.Status # >KEKUATAN HUKUM TETAP
```
