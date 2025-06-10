class ViewManager:
    def __init__(self):
        self.subscribers = {}
        self.active_view = None
        self.active_callback = None
    def subscribe(self, attribute, callback, view_name):
        if attribute not in self.subscribers:
            self.subscribers[attribute] = {}
        self.subscribers[attribute][view_name] = callback
    def set_active_view(self, view_name, callback):
        self.active_view = view_name
        self.active_callback = callback
    def notify(self, attribute):
        if attribute in self.subscribers and self.active_view in self.subscribers[attribute]:
            self.subscribers[attribute][self.active_view]()
        elif self.active_callback:
            self.active_callback()