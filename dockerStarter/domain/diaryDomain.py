class RequestWriteContext:
    def __init__(self, writer, title, context, date):
        self.writer = writer
        self.title = title
        self.context = context
        self.date = date
        
    def displayRequestWriteContext(self):
        print('writer: {}, title: {}, context: {}, date: {}'.format(self.writer, self.title, self.context, self.date))