#!/usr/bin/env python3
"""
Script de Análisis de Impacto de Tests (TIA)
Determina qué tests ejecutar basándose en archivos cambiados
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali

Uso:
    python impact_analysis.py --changed src/employee.py
    python impact_analysis.py --changed src/leave.py
    python impact_analysis.py --changed src/employee.py src/leave.py
"""
import argparse
import ast
import os
import sys


# ─── Mapa de dependencias ───────────────────────────────────────
# Cada módulo src → lista de archivos test que lo importan
# "direct" = el test importa el módulo directamente
# "indirect" = el test importa otro módulo que a su vez importa este

DEPENDENCY_MAP = {
    "src/employee.py": {
        "direct": ["tests/test_employee.py"],
        "indirect": ["tests/test_reports.py"],  # reports.py importa employee.py
    },
    "src/leave.py": {
        "direct": ["tests/test_leave.py"],
        "indirect": ["tests/test_reports.py"],  # reports.py importa leave.py
    },
    "src/reports.py": {
        "direct": ["tests/test_reports.py"],
        "indirect": [],
    },
}

ALL_TESTS = [
    "tests/test_employee.py",
    "tests/test_leave.py",
    "tests/test_reports.py",
]


def analyze_impact(changed_files):
    """
    Analiza qué tests se ven afectados por los archivos cambiados.
    Retorna (affected_tests, skipped_tests) con detalles de razón.
    """
    affected = {}  # test_file -> razón

    for changed in changed_files:
        # Normalizar path
        changed = changed.replace("\\", "/")

        if changed in DEPENDENCY_MAP:
            deps = DEPENDENCY_MAP[changed]

            # Tests directos
            for test in deps["direct"]:
                reason = f"importa {os.path.basename(changed).replace('.py', '')}"
                affected[test] = f"{test} ({reason})"

            # Tests indirectos
            for test in deps["indirect"]:
                # Encontrar qué módulo intermedio causa la dependencia
                intermediate = find_intermediate(changed, test)
                reason = f"{intermediate} importa {os.path.basename(changed).replace('.py', '')}"
                affected[test] = f"{test} ({reason})"
        else:
            print(f"⚠ Archivo no mapeado: {changed}")

    # Tests no afectados
    skipped = []
    for test in ALL_TESTS:
        if test not in affected:
            skipped.append(f"{test} (no afectado)")

    return affected, skipped


def find_intermediate(source_file, test_file):
    """Encuentra el módulo intermedio entre source y test."""
    # reports.py importa tanto employee.py como leave.py
    if "test_reports" in test_file:
        return "reports"
    return os.path.basename(source_file).replace(".py", "")


def try_dynamic_analysis(changed_files):
    """
    Intenta análisis dinámico parseando imports reales.
    Fallback al mapa estático si falla.
    """
    affected = set()

    for changed in changed_files:
        changed = changed.replace("\\", "/")
        module_name = changed.replace("src/", "").replace(".py", "")

        # Buscar qué archivos de test importan este módulo
        tests_dir = "tests"
        if os.path.isdir(tests_dir):
            for test_file in os.listdir(tests_dir):
                if test_file.startswith("test_") and test_file.endswith(".py"):
                    test_path = os.path.join(tests_dir, test_file)
                    if imports_module(test_path, module_name):
                        affected.add(test_path.replace("\\", "/"))

        # Buscar dependencias indirectas en src/
        src_dir = "src"
        if os.path.isdir(src_dir):
            for src_file in os.listdir(src_dir):
                if src_file.endswith(".py") and src_file != "__init__.py":
                    src_path = os.path.join(src_dir, src_file)
                    if imports_module(src_path, module_name):
                        # Este módulo src importa el archivo cambiado
                        # → buscar tests que importan ESTE módulo
                        intermediate = src_file.replace(".py", "")
                        for test_file in os.listdir(tests_dir):
                            if test_file.startswith("test_") and test_file.endswith(".py"):
                                test_path = os.path.join(tests_dir, test_file)
                                if imports_module(test_path, intermediate):
                                    affected.add(test_path.replace("\\", "/"))

    return affected


def imports_module(file_path, module_name):
    """Verifica si un archivo Python importa un módulo dado usando AST."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if module_name in alias.name:
                        return True
            elif isinstance(node, ast.ImportFrom):
                if node.module and module_name in node.module:
                    return True
    except (SyntaxError, FileNotFoundError):
        pass

    return False


def print_results(changed_files, affected, skipped):
    """Imprime resultados con formato legible."""
    print("=" * 60)
    print("  ANÁLISIS DE IMPACTO DE TESTS (TIA)")
    print("  Proyecto: ejemplo-tia-demo_employee")
    print("=" * 60)
    print()

    # Archivos cambiados
    print("📁 Archivos cambiados:")
    for f in changed_files:
        print(f"   • {f}")
    print()

    # Tests afectados
    print(f"🎯 Tests afectados: {len(affected)}")
    for detail in affected.values():
        print(f"   ✅ {detail}")
    print()

    # Tests omitidos
    print(f"⏭ Tests omitidos: {len(skipped)}")
    for detail in skipped:
        print(f"   ⛔ {detail}")
    print()

    # Resumen
    total = len(affected) + len(skipped)
    pct = (len(skipped) / total * 100) if total > 0 else 0
    print(f"📊 Resumen: {len(affected)}/{total} tests a ejecutar "
          f"({pct:.0f}% omitidos)")
    print()

    # Comando sugerido
    if affected:
        test_files = " ".join(affected.keys())
        print(f"▶ Comando sugerido:")
        print(f"   python -m pytest {test_files} -v")
    print()
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Análisis de Impacto de Tests (TIA) - ejemplo-tia-demo_employee",
        epilog="Ejemplo: python impact_analysis.py --changed src/employee.py"
    )
    parser.add_argument(
        "--changed",
        nargs="+",
        required=True,
        help="Archivos fuente modificados (ej: src/employee.py src/leave.py)"
    )
    parser.add_argument(
        "--dynamic",
        action="store_true",
        help="Usar análisis dinámico de imports (requiere acceso a archivos)"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Formato de salida (default: text)"
    )

    args = parser.parse_args()

    if args.dynamic:
        # Análisis dinámico usando AST
        dynamic_affected = try_dynamic_analysis(args.changed)
        if dynamic_affected:
            print("🔬 Modo: Análisis Dinámico (AST parsing)")
            affected = {}
            for t in dynamic_affected:
                affected[t] = f"{t} (detectado por análisis de imports)"
            skipped = [f"{t} (no afectado)" for t in ALL_TESTS if t not in affected]
            print_results(args.changed, affected, skipped)
        else:
            print("⚠ Análisis dinámico sin resultados, usando mapa estático...")
            affected, skipped = analyze_impact(args.changed)
            print_results(args.changed, affected, skipped)
    else:
        # Análisis estático usando mapa de dependencias
        print("📋 Modo: Mapa Estático de Dependencias")
        affected, skipped = analyze_impact(args.changed)
        print_results(args.changed, affected, skipped)

    if args.output == "json":
        import json
        result = {
            "changed_files": args.changed,
            "affected_tests": list(affected.keys()) if isinstance(affected, dict) else list(affected),
            "skipped_tests": [s.split(" (")[0] for s in skipped],
        }
        print("\n--- JSON ---")
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
