import xml.etree.ElementTree as ET
import os

META_FILE_NAME = 'metafile.xml'


class RainMetaFileAdapter(object):
    def __init__(self, filename):
        self.metafile = ET.parse(filename)
        self.root = self.metafile.getroot()

    def dump(self):
        self.metafile.dump(META_FILE_NAME)

    def set_metafile_from_string(self,metafile_content):
        self.metafile = ET.XML(metafile_content)
        self.root = self.metafile.getroot()

    def set_metafile(self,filename):
        self.metafile = ET.parse(filename)
        self.root = self.metafile.getroot()


    # Write operations

    def add_cloud(self, cloud_name, access_token):
        cloud = ET.Element('cloud')
        ET.SubElement(cloud, 'name').text = cloud_name
        ET.SubElement(cloud, 'access_token').text = access_token
        self.root.append(cloud)

    def remove_cloud(self, cloud_name):
        self.root.remove(self._get_cloud_elem(cloud_name))

    def add_file(self, cloud_name, local_filename, remote_filename, file_size):
        file = ET.Element('file')
        ET.SubElement(file, 'local_filename').text = local_filename
        ET.SubElement(file, 'remote_filename').text = remote_filename
        ET.SubElement(file, 'file_size').text = file_size

        drive = self._get_cloud_elem(cloud_name)
        drive.append(file)

    def remove_file(self, cloud_name, local_filename):
        cloud_elem = self._get_cloud_elem(cloud_name)
        files = cloud_elem.findall("./file[local_filename='" + local_filename + "']")
        for f in files:
            cloud_elem.remove(f)

    def move_file(self, cloud_name, src_path, dst_path):
        cloud_elem = self._get_cloud_elem(cloud_name)
        target = cloud_elem.find("./file[local_filename='" + src_path + "']")
        target.find("./local_filename").text = dst_path
        target.find("./remote_filename").text = os.path.join("/Rain", dst_path)

    # Read operations

    def _get_cloud_elem(self, cloud_name):
        cloud = self.root.find("./cloud[name='" + cloud_name + "']")
        if cloud is None:
            raise Exception('Cloud ' + cloud_name + 'not found in metafile')
        return cloud

    def get_cloud_name_by_local_filename(self, filename):
        cloud_name = self.root.find(".//file[local_filename='" + filename + "']/..name")
        if cloud_name is None:
            raise KeyError()
        else:
            return cloud_name.text

    def get_all_cloud_name(self):
        names = self.root.findall("./cloud/name")
        return map(lambda x: x.text, names)

    def get_cloud_access_token(self, cloud_name):
        cloud = self._get_cloud_elem(cloud_name)
        return cloud.find('access_token').text

    def get_cloud_capacity(self, cloud_name):
        cloud = self._get_cloud_elem(cloud_name)
        return cloud.find('capacity').text

    def get_file_map(self, cloud_name):
        local_files = self.get_local_file_list(cloud_name)
        remote_files = self.get_remote_file_list(cloud_name)
        return {x: y for x, y in zip(local_files, remote_files)}

    def get_local_file_list(self, cloud_name):
        files = self.root.findall("./cloud[name='" + cloud_name + "']/file/local_filename")
        return [f.text for f in files]

    def get_remote_file_list(self, cloud_name):
        files = self.root.findall("./cloud[name='" + cloud_name + "']/file/remote_filename")
        return [f.text for f in files]

    def get_username(self):
        return self.root.find("./username").text

    def get_raw_xml(self):
        return ET.tostring(self.root)






