"""Testes dos importadores e do merge do log. Rodar: python3 -m unittest discover tests"""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import importar  # noqa: E402

EX = RAIZ / "tests" / "exemplos"


class Importadores(unittest.TestCase):
    def test_strong(self):
        r = importar.ler(EX / "strong.csv")
        self.assertEqual([x["tipo"] for x in r], ["aquecimento", "trabalho", "trabalho", "trabalho"])
        self.assertEqual(r[1]["inicio"], "2026-11-09T18:30")
        self.assertEqual(r[1]["fim"], "2026-11-09T19:45")
        self.assertEqual(r[2]["rpe"], "9.5")
        self.assertEqual(r[3]["exercicio"], "Leg Press (Machine)")  # apelido
        self.assertEqual(r[0]["fonte"], "strong")

    def test_strong_ponto_virgula_e_colunas_variantes(self):
        r = importar.ler(EX / "strong-ponto-virgula.csv")
        self.assertEqual((r[0]["kg"], r[0]["reps"], r[0]["fim"]), ("50", "12", "2026-11-10T19:40"))

    def test_fitnotes_libras_e_numeracao(self):
        r = importar.ler(EX / "fitnotes.csv")
        self.assertAlmostEqual(float(r[0]["kg"]), 226.8, places=1)
        self.assertEqual([x["serie"] for x in r], ["1", "2", "1"])
        self.assertEqual(r[2]["exercicio"], "Exercicio Inventado")  # sem apelido: mantem o nome

    def test_manual_nomes_em_portugues(self):
        r = importar.ler(EX / "manual.csv")
        self.assertEqual([x["exercicio"] for x in r],
                         ["Dumbbell Row", "Dumbbell Row", "Bench Press (Barbell)", "Pull Up"])
        self.assertEqual(r[0]["tipo"], "aquecimento")
        self.assertEqual(r[1]["tipo"], "trabalho")
        self.assertEqual(r[0]["inicio"], "2026-11-11T00:00")

    def test_hevy_ingles_e_libras(self):
        r = importar.ler(EX / "hevy-en.csv")
        self.assertEqual(r[0]["tipo"], "aquecimento")
        self.assertEqual(r[1]["inicio"], "2026-11-09T18:30")
        self.assertAlmostEqual(float(r[1]["kg"]), 79.83, places=1)

    def test_hevy_portugues(self):
        self.assertEqual(importar.iso(importar.data_texto("4 de nov. de 2026, 18:40")), "2026-11-04T18:40")


class Merge(unittest.TestCase):
    def importar(self, log, arq):
        return subprocess.run([sys.executable, str(RAIZ / "scripts/importar.py"), str(EX / arq), "--log", log],
                              capture_output=True, text=True, check=True).stdout

    def test_merge_de_fontes_e_reimportacao(self):
        with tempfile.TemporaryDirectory() as d:
            log = str(Path(d) / "log.csv")
            self.importar(log, "strong.csv")
            self.importar(log, "manual.csv")
            saida = self.importar(log, "fitnotes.csv")
            self.assertIn("Exercicio Inventado", saida)  # avisa NAO MAPEADOS
            self.importar(log, "strong.csv")  # reimportar nao duplica
            linhas = list(csv.DictReader(Path(log).read_text(encoding="utf-8").splitlines()))
            self.assertEqual(len(linhas), 4 + 4 + 3)
            self.assertEqual({x["fonte"] for x in linhas}, {"strong", "manual", "fitnotes"})
            r = subprocess.run([sys.executable, str(RAIZ / "scripts/treino.py"), log, "--semanas", "2"],
                               capture_output=True, text=True, check=True).stdout
            self.assertIn("NAO MAPEADOS", r)
            self.assertIn("Bench Press (Barbell): 11/11 76x8 (1s RPE 9)", r)


if __name__ == "__main__":
    unittest.main()
