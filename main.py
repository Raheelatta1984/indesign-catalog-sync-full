from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import subprocess
import os
from datetime import datetime

class CatalogApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='InDesign Catalog Sync MCP', font_size=24, size_hint_y=0.1)
        layout.add_widget(title)
        
        # CSV Input
        self.csv_input = TextInput(text='data/master_products.csv', multiline=False, size_hint_y=0.1)
        layout.add_widget(Label(text='CSV Path:'))
        layout.add_widget(self.csv_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.6, orientation='vertical', spacing=5)
        
        btn_update = Button(text='1. Update Master CSV')
        btn_update.bind(on_press=self.do_update)
        btn_layout.add_widget(btn_update)
        
        btn_export = Button(text='2. Export for InDesign')
        btn_export.bind(on_press=self.do_export)
        btn_layout.add_widget(btn_export)
        
        btn_history = Button(text='3. Show History')
        btn_history.bind(on_press=self.do_history)
        btn_layout.add_widget(btn_history)
        
        btn_monitor = Button(text='4. Start Monitoring (Background)')
        btn_monitor.bind(on_press=self.do_monitor)
        btn_layout.add_widget(btn_monitor)
        
        layout.add_widget(btn_layout)
        
        # Status
        scroll = ScrollView(size_hint_y=0.3)
        self.status = Label(text='Status: Ready\nTap buttons to run commands', size_hint_y=None)
        self.status.bind(size=self.status.setter('text_size'))
        scroll.add_widget(self.status)
        layout.add_widget(scroll)
        
        return layout
    
    def run_cli(self, args):
        try:
            result = subprocess.run(['python', 'cli.py'] + args, 
                                  capture_output=True, text=True, cwd=os.getcwd())
            output = result.stdout[-800:] or result.stderr[-600:]
            self.status.text = f"[{datetime.now().strftime('%H:%M:%S')}] {output.strip() or 'Done.'}"
        except Exception as e:
            self.status.text = f"Error: {str(e)}"
    
    def do_update(self, instance):
        self.run_cli(['update', '--csv', self.csv_input.text])
    
    def do_export(self, instance):
        self.run_cli(['export'])
    
    def do_history(self, instance):
        self.run_cli(['history'])
    
    def do_monitor(self, instance):
        self.status.text = "Monitoring started (check logs in Termux). Use Ctrl+C to stop in background."

if __name__ == '__main__':
    CatalogApp().run()