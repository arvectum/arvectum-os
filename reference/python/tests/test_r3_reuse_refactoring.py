from __future__ import annotations

import ast
import inspect
import unittest

import arvectum_os_ref.governed_execution as governed_execution_module
import arvectum_os_ref.product_contract as product_contract_module
import arvectum_os_ref.runtime as historical_runtime_module
from arvectum_os_ref.runtime import RuntimeExecutionRequest


class R3ReuseRefactoringTests(unittest.TestCase):
    """Lock the evidence-backed R3 reuse disposition without inventing a new framework."""

    @staticmethod
    def _imported_modules(module) -> set[str]:
        tree = ast.parse(inspect.getsource(module))
        return {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }

    def test_product_contract_entry_uses_governed_execution_not_historical_composition(self) -> None:
        imported = self._imported_modules(product_contract_module)
        source = inspect.getsource(product_contract_module)

        self.assertNotIn("runtime", imported)
        self.assertNotIn("RuntimeComposition", source)
        self.assertIn("start_governed_execution(", source)

    def test_governed_execution_does_not_depend_on_historical_p201_composition(self) -> None:
        imported = self._imported_modules(governed_execution_module)
        source = inspect.getsource(governed_execution_module)

        self.assertNotIn("runtime", imported)
        self.assertNotIn("RuntimeComposition", source)
        self.assertNotIn("RuntimeOperations", source)

    def test_historical_request_is_not_generalized_to_fit_second_workflow(self) -> None:
        fields = set(RuntimeExecutionRequest.__dataclass_fields__)

        self.assertIn("material_input", fields)
        self.assertNotIn("material_inputs", fields)
        self.assertIn("authorization_basis_ref", fields)
        self.assertIn("organizational_authority_basis_ref", fields)
        self.assertNotIn("required_gates", fields)
        self.assertNotIn("product_contract", fields)

    def test_historical_module_declares_reference_only_r3_disposition(self) -> None:
        module_doc = " ".join(
            (inspect.getdoc(historical_runtime_module) or "").replace("**", "").split()
        )
        composition_doc = " ".join(
            (inspect.getdoc(historical_runtime_module.RuntimeComposition) or "").split()
        )

        self.assertIn("historical reference-composition compatibility boundary", module_doc)
        self.assertIn("not the reusable Phase 2 Core Runtime entry point", module_doc)
        self.assertIn("MUST NOT be expanded", composition_doc)


if __name__ == "__main__":
    unittest.main()
