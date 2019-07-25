from BaseTools import BasicDevice


class Comment(BasicDevice):
    def __init__(self, los=None, **kwargs):
        super().__init__(**kwargs)
        if los is None:
            self.los = []
        else:
            self.los = los

