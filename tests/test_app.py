import os
import tempfile
import json
import shutil
import unittest
from PIL import Image

import app.data as data


class TestDataModule(unittest.TestCase):
    def setUp(self):
        # create a temp dir and override module paths to avoid touching real data
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = self.tmpdir.name
        data.ARQUIVO = os.path.join(self.tmp, "alunos_test.json")
        data.PASTA_FOTOS = os.path.join(self.tmp, "fotos")
        data.FOTO_PADRAO = os.path.join(data.PASTA_FOTOS, "padrao.png")
        os.makedirs(data.PASTA_FOTOS, exist_ok=True)
        # create a dummy padrao file (small valid image)
        img = Image.new('RGB', (10, 10), color=(255, 0, 0))
        os.makedirs(os.path.dirname(data.FOTO_PADRAO), exist_ok=True)
        img.save(data.FOTO_PADRAO, format='PNG')

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_carregar_salvar_alunos_empty(self):
        # should be empty list when file doesn't exist
        if os.path.exists(data.ARQUIVO):
            os.remove(data.ARQUIVO)
        a = data.carregar_alunos()
        self.assertIsInstance(a, list)

        # save and reload
        sample = [{"nome": "Teste", "link": "http://example.com", "foto": data.FOTO_PADRAO}]
        data.salvar_alunos(sample)
        loaded = data.carregar_alunos()
        self.assertEqual(sample, loaded)

    def test_copy_photo(self):
        # create a small valid source image
        src = os.path.join(self.tmp, "src.png")
        img = Image.new('RGB', (1000, 1000), color=(0, 255, 0))
        img.save(src, format='PNG')
        dest_name = "copied.png"
        dest = data.copy_photo(src, dest_name)
        self.assertTrue(os.path.exists(dest))
        # ensure result is a JPEG file (we store as .jpg)
        self.assertTrue(dest.lower().endswith('.jpg'))


if __name__ == "__main__":
    unittest.main()
