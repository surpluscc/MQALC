"""Whole-file CoC using the original Sonar Python analyzer via JPype."""
import argparse
import hashlib
from pathlib import Path

from .common import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--sonarqube", type=Path, required=True)
    parser.add_argument("--jvm", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import jpype

    jars = sorted(args.sonarqube.glob("lib/**/*.jar"))
    plugins = [p for p in jars if p.name.startswith("sonar-python-plugin-")]
    if len(plugins) != 1:
        parser.error("Expected exactly one sonar-python-plugin JAR under lib/")
    if not args.source.exists():
        parser.error("Source does not exist")
    paths = [args.source] if args.source.is_file() else sorted(args.source.rglob("*.py"))
    if not paths:
        parser.error("No Python source files found")
    jpype.startJVM(args.jvm, "-Xmx768m", classpath=[str(p) for p in jars])
    try:
        source_parser = jpype.JClass("org.sonar.python.parser.PythonParser").create()
        maker = jpype.JClass("org.sonar.python.tree.PythonTreeMaker")()
        visitor = jpype.JClass("org.sonar.python.metrics.CognitiveComplexityVisitor")
        rows = []
        for path in paths:
            row = {"file": path.name if args.source.is_file()
                   else path.relative_to(args.source).as_posix()}
            try:
                raw = path.read_bytes()
                row["sha256"] = hashlib.sha256(raw).hexdigest()
                tree = maker.fileInput(source_parser.parse(raw.decode("utf-8-sig")))
                maker.setParents(tree)
                row.update(status="ok", CoC=int(visitor.complexity(tree, None)))
            except Exception as exc:
                row.update(status="error", error=type(exc).__name__)
            rows.append(row)
        plugin = plugins[0]
        write_json(args.output, {"analyzer": plugin.name,
                   "analyzer_sha256": hashlib.sha256(plugin.read_bytes()).hexdigest(),
                   "java_version": str(jpype.JClass("java.lang.System").getProperty("java.version")),
                   "scope": "whole file", "files": rows})
    finally:
        jpype.shutdownJVM()
    if any(r["status"] != "ok" for r in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
