from .. import clouddrive


__name__ = 'Box'


class Box(clouddrive.CloudDrive):
    name = "Box"

    def __init__(self, access_token=None):
        self.access_token = access_token
        super(Box, self).__init__(access_token)


