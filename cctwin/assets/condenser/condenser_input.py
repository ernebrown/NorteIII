from cctwin.assets.block.ambient_conditions import AmbientConditions


class CondenserInput:
    def __init__(self,
                 ambient_conditions: AmbientConditions
                 ):
        self.ambient_conditions = ambient_conditions
