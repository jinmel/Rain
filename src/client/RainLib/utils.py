import xml.etree.ElementTree as ET


class RainMetaFileAdapter(object):
    def __init__(self, filename):
        self.metafile = ET.parse(filename)
        self.root = self.metafile.getroot()

    def write(self, filename):
        self.metafile.write(filename)

    # Write operations

    def add_cloud(self, cloud_name, access_token):
        cloud = ET.Element('cloud')
        ET.SubElement(cloud, 'name').text = cloud_name
        ET.SubElement(cloud, 'access_token').text = access_token
        self.root.append(cloud)

    def remove_cloud(self, cloud_name):
        self.root.remove(self.get_cloud(cloud_name))

    def add_file(self, cloud_name, local_filename, remote_filename, file_size):
        file = ET.Element('file')
        ET.SubElement(file, 'local_filename').text = local_filename
        ET.SubElement(file, 'remote_filename').text = remote_filename
        ET.SubElement(file, 'file_size').text = file_size

        drive = self.get_cloud(cloud_name)
        drive.append(file)

    def remove_file(self, cloud_name, local_filename):
        cloud = self.get_cloud(cloud_name)
        files = cloud.findall("./file[local_filename='" + local_filename + "']")
        for f in files:
            cloud.remove(f)

    # Read operations

    def get_cloud(self, cloud_name):
        cloud = self.root.find("./cloud[name='" + cloud_name + "']")
        if cloud is None:
            raise Exception('Cloud ' + cloud_name + 'not found in metafile')
        return cloud

    def get_cloud_access_token(self, cloud_name):
        cloud = self.get_cloud(cloud_name)
        return cloud.find('access_token').text

    def get_cloud_capacity(self, cloud_name):
        cloud = self.get_cloud(cloud_name)
        return cloud.find('capacity').text

    def get_local_file_list(self, cloud_name):
        files = self.root.findall("./cloud[name='" + cloud_name + "']/file")
        return [f.find('local_filename').text for f in files]

    def get_remote_file_list(self, cloud_name):
        files = self.root.findall("./cloud[name='" + cloud_name + "']/file")
        return [f.find('remote_filename').text for f in files]




