from django.test import TestCase
from .models import Studio


class StudioTests(TestCase):
    def setUp(self):
        # Создание студий
        studios = [
            'Toei Animation', 'Studio Ghibli', 'Madhouse', 'Bones', 'Kyoto Animation',
            'Sunrise', 'Gainax', 'A-1 Pictures', 'MAPPA', 'Studio Deen',
            'P.A. Works', 'J.C. Staff', 'Production I.G', 'White Fox', 'Wit Studio',
            'David Production', 'Trigger', 'Shaft', 'CloverWorks', 'Studio Pierrot'
        ]
        
        for studio_name in studios:
            Studio.objects.get_or_create(name=studio_name)
            
    def test_studio_creation(self):
        # Проверка, что все студии были созданы
        studios = Studio.objects.all()
        self.assertEqual(studios.count(), 20)  # Проверка, что 20 студий было создано
        studio_names = [studio.name for studio in studios]
        expected_names = [
            'Toei Animation', 'Studio Ghibli', 'Madhouse', 'Bones', 'Kyoto Animation',
            'Sunrise', 'Gainax', 'A-1 Pictures', 'MAPPA', 'Studio Deen',
            'P.A. Works', 'J.C. Staff', 'Production I.G', 'White Fox', 'Wit Studio',
            'David Production', 'Trigger', 'Shaft', 'CloverWorks', 'Studio Pierrot'
        ]
        self.assertTrue(all(name in studio_names for name in expected_names))