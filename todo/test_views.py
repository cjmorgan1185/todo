# correct location (url) correct template used
from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Item

class TestViews(TestCase):
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "todo_list.html")
        
    def test_get_add_item_page(self):
        page = self.client.get("/add")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "item_form.html")
        
    def test_get_edit_item_page(self):
        item = Item(name = 'Create a Test')
        item.save()
        
        page = self.client.get("/edit/{0}".format(item.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "item_form.html")
        
    def test_get_edit_page_for_item_that_doesnt_exist(self):
        page = self.client.get("/edit/1")
        self.assertEqual(page.status_code, 404)
        
    def test_post_create_an_item(self):
        response = self.client.post("/add", {'name': 'Create a Test'})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, False)
        
    def test_post_edit_an_item(self):
        item=Item(name="Test")  
        item.save() #create's record
        id = item.id #sets items id to id
        
        response = self.client.post("/edit/{0}".format(id), {'name':'New'}) #updates item with same id
        item = get_object_or_404(Item, pk=id)
        
        self.assertEqual('New', item.name) #checks item.name is new value
    
    def test_toggle_Status(self):
        item=Item(name="Test")  
        item.save() #create's record
        id = item.id #sets items id to id
        
        response = self.client.post("/toggle/{0}".format(id))
        
        item = get_object_or_404(Item, pk=id)
        self.assertEqual(item.done, True)