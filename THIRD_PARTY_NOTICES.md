# Third-party notices

`third_party/lcd_execution.py` is copied without modification from the supplied
LeetCodeDataset evaluator snapshot (`eval_lcd/execution.py`). Its supplied MIT
license is preserved at `third_party/LICENSE.LeetCodeDataset`, copyright (c) 2025
newfacade. The local snapshot does not record an upstream Git commit; this release
does not claim to match the latest upstream version. Source hashes are recorded
in `RELEASE_MANIFEST.json`.

That execution helper uses the HumanEval-style evaluation approach. Radon,
SciPy, JPype and the Sonar Python analyzer are external dependencies; they are
not bundled or relicensed here. SonarQube binaries and datasets are not included.

No blanket license is assigned to the authors' newly organized files in this
release. Public visibility alone does not grant an open-source license. The
authors should select an appropriate license before advertising the entire
repository as open source; the retained third-party MIT notice applies only to
the third-party material it covers.
