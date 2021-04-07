import os
import json


class ClevrDataset(object):
    """Class to convert clevr annotation to coco type."""

    def return_json_file(self, json_path):
        """
        Method to read json files.

        Parameters
        ----------
        json_path: str

        Returns
        -------
        contents: json
        """
        with open(json_path, 'r') as file:
            contents = json.loads(file.read())
        return contents

    def load_clevr_image_data(self, json_path):
        """
        Method to convert <>_image_metadat.json file to image.

        Parameters
        ----------
        json_path: str
            path to file
        Returns
        -------
        category_array: list
        """
        contents = self.return_json_file(json_path)
        image_array = list()
        image_to_id_lookup = dict()
        index = 0
        for keys, values in contents.items():
            image_dict = dict()
            image_dict['id'] = index
            image_dict['file_name'] = keys
            image_dict['width'] = contents[keys]['width']
            image_dict['height'] = contents[keys]['height']
            image_array.append(image_dict)
            image_to_id_lookup[keys] = index
            index += 1
        return image_array, image_to_id_lookup

    def load_clevr_objects(self, json_path):
        """
        Method to load clever object categories.

        Parameters
        ----------
        json_path: str

        Returns
        -------
        category_array: list
        """
        contents = self.return_json_file(json_path)
        category_array = list()
        for index, item in enumerate(contents):
            category_dict = dict()
            category_dict['id'] = index
            category_dict['name'] = item
            category_dict['supercategory'] = 'none'
            category_array.append(category_dict)
        return category_array

    def return_object_dict(self, dictionary):
        """
        Method to return a list processed.

        Parameters
        ----------
        dictionary: dict

        Returns
        -------
        list
        """
        return[dictionary['object'], dictionary['subject']]

    def parse_annotation(self, index, image_id, relation_list):
        """
        Method to parse annotations.

        Parameters
        ----------
        index: int
        image_id: int
        relation_list: list

        Returns
        -------
        index: int
            index for global count of annotations
        unique_object_annotation_list: list
        """
        unique_object_list = list()
        unique_object_annotation_list = list()
        for relation in relation_list:
            returns = self.return_object_dict(relation)
            unique_object_list += returns
        unique_object_list = list(
            {item['category']: item for item in unique_object_list}.values())
        for i in range(len(unique_object_list)):
            annotation_dict = dict()
            annotation_dict['id'] = index
            annotation_dict['image_id'] = image_id
            annotation_dict['category_id'] = unique_object_list[i]['category']
            annotation_dict['bbox'] = unique_object_list[i]['bbox']
            annotation_dict['segmentation'] = []
            annotation_dict['area'] = 0
            annotation_dict['iscrowd'] = 0
            annotation_dict['ignore'] = 0
            index += 1
            unique_object_annotation_list.append(annotation_dict)
        return index, unique_object_annotation_list

    def load_clevr_annotation(self, json_path, image_to_id_lookup):
        """
        Method to load clevr annotations.

        Parameters
        ----------
        json_path: str
        image_to_id_looup: dict

        Returns
        -------
        annotation_array: list
        """
        contents = self.return_json_file(json_path)
        annotation_array = list()
        index = 0
        for keys, values in contents.items():
            image_id = image_to_id_lookup[keys]
            relation_list = values
            index, unique_object_annotation_list = self.parse_annotation(
                index, image_id, relation_list)
            annotation_array += unique_object_annotation_list
        return annotation_array

    def call(self, base_path, file_name, test=False):
        """
        Method to call the class.

        Parameters
        ----------
        base_path: str
        file_name: str
            output filename
        test: bool
            if you are processing training/testing dataset.

        Return
        ------
        None

        """
        object_path = os.path.join(base_path, "objects.json")
        if not test:
            meta_data_path = os.path.join(
                base_path, "train_image_metadata.json")
            annotation_path = os.path.join(base_path, "annotations_train.json")
        else:
            meta_data_path = os.path.join(
                base_path, "test_image_metadata.json")
            annotation_path = os.path.join(base_path, "annotations_test.json")
        t_dict = dict()
        t_dict['images'], image_to_id_lookup = self.load_clevr_image_data(
            meta_data_path)
        t_dict['annotations'] = self.load_clevr_annotation(
            annotation_path, image_to_id_lookup)
        t_dict['category'] = self.load_clevr_objects(object_path)
        print(t_dict['category'])
        save_path = os.path.join(base_path, file_name)
        with open(save_path, 'w') as outfile:
            json.dump(t_dict, outfile)