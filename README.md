```
# from crispr/ dir
export FLASK_APP=crispr.py
export FLASK_DEBUG=1
flask run
```

Tests:
```
python tests/crispr_tests.py
```

# Dependencies

Python: Flask
Nodejs: Pileup.js (install into `static/js`)

# Configuration

_Example data has been included that works on app start._

You can insert your own data into the `crispr/data` directory under the following scheme:

```
/MyReportName/
   /bam/
   /vcf/
```

To override this data location with your own location.

Create a directory off the root (crispr_results) one called `instance`, create a `config.py` inside and put `DATA_INDEX_DIRECTORY = '<YOUR PATH HERE>'`.
