import sys, json
from run_regression import run_seed, ROOT

seed = int(sys.argv[1])
bug = "--bug" in sys.argv
r = run_seed(seed, bug)
(ROOT / "runs" / f"seed_{seed}" / "result.json").write_text(json.dumps(r))
print(json.dumps(r))
