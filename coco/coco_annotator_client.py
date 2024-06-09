import io
import json

import PIL.Image
import numpy as np
import requests

"""
GET /info/
GET /info/long_task
GET /user/
GET /user/logout 
GET /image/ 
GET /image/{image_id} 
GET /image/{image_id}/coco 
GET /annotation/
GET /annotation/{annotation_id}
GET /category/
GET /category/data
GET /category/{category_id}
GET /dataset/
GET /dataset/coco/{import_id}
GET GET /dataset/data
GET /dataset/{dataset_id}/coco
GET /dataset/{dataset_id}/data
GET /dataset/{dataset_id}/export
GET /dataset/{dataset_id}/exports
GET /dataset/{dataset_id}/reset/metadata
GET /dataset/{dataset_id}/scan
GET GET /dataset/{dataset_id}/stats
GET /dataset/{dataset_id}/users
GET /export/{export_id}
GET /export/{export_id}/download 
GET /tasks/
GET /tasks/{task_id}/logs
GET /undo/list/
GET /admin/user/{username}
GET /admin/users
GET /annotator/data/{image_id}

POST /user/login
POST /user/password
POST /user/register 
POST /image/
POST /image/copy/{from_id}/{to_id}/annotations
POST /annotation/ 
POST /category/
POST /dataset/
POST /dataset/{dataset_id}
POST /dataset/{dataset_id}/coco
POST /dataset/{dataset_id}/export
POST /dataset/{dataset_id}/generate
POST /dataset/{dataset_id}/share 
POST /undo/
POST /model/dextr/{image_id}
POST /model/maskrcnn
POST /admin/user/
POST /annotator/data 

DELETE /image/{image_id}
DELETE /annotation/{annotation_id}
DELETE /category/{category_id}
DELETE /dataset/{dataset_id}
DELETE /export/{export_id}
DELETE /tasks/{task_id}
DELETE /undo/
DELETE /admin/user/{username}

PUT /annotation/{annotation_id}
PUT /category/{category_id}

"""


class COCOAnnotatoryClient:
    def __init__(self, address, port=5000):
        self._address = address
        self._port = port
        self._sess = requests.Session()

    def __del__(self):
        if self._sess is not None:
            self._sess.close()

    def _get(self, api) -> requests.Response:
        url = f"http://{self._address}:{self._port}/api{api}"
        res = self._sess.get(url)
        # res.raise_for_status()
        return res

    def _post(self, api, params) -> requests.Response:
        url = f"http://{self._address}:{self._port}/api{api}"
        res = self._sess.post(url, json=params)
        # res.raise_for_status()
        return res

    def _delete(self, api) -> requests.Response:
        raise NotImplementedError
        url = f"http://{self._address}:{self._port}/api{api}"
        res = self._sess.delete(url)
        # res.raise_for_status()
        return res

    def _put(self, api, params) -> requests.Response:
        url = f"http://{self._address}:{self._port}/api{api}"
        res = self._sess.put(url, json=params)
        # res.raise_for_status()
        return res

    def _patch(self, api, params) -> requests.Response:
        url = f"http://{self._address}:{self._port}/api{api}"
        res = self._sess.patch(url, json=params)
        # res.raise_for_status()
        return res

    def get_info(self) -> dict:
        """GET /info/"""
        res = self._get('/info/')
        return json.loads(res.text)

    def get_info_long_task(self) -> dict:
        """GET /info/long_task"""
        res = self._get('/info/long_task')
        return json.loads(res.text)

    def get_user(self) -> dict:
        """GET /user/
        Get information of current user.
        """
        res = self._get('/user/')
        return json.loads(res.text)

    def get_user_logout(self) -> dict:
        """GET /user/logout"""
        res = self._get('/user/logout')
        return json.loads(res.text)

    def get_image(self) -> dict:
        """GET /image/        
        Returns all images.
        """
        res = self._get('/image/')
        return json.loads(res.text)

    def get_image_(self, image_id: int, return_type='bytes'):
        """GET /image/{image_id}"""
        def _bytes_to_pil_image(buf: bytes):
            return PIL.Image.open(io.BytesIO(buf))

        def _pil_image_to_numpy(img: PIL.Image):
            return np.array(img)

        res = self._get(f'/image/{image_id}')
        if return_type == 'bytes':
            img = res.content
        elif return_type == 'pil':
            img = _bytes_to_pil_image(res.content)
        elif return_type == 'numpy':
            pil_img = _bytes_to_pil_image(res.content)
            img = _pil_image_to_numpy(pil_img)
        else:
            raise ValueError

        return img

    def get_image__coco(self, image_id: int):
        """GET /image/{image_id}/coco
        Returns coco of image and annotations.
        """
        res = self._get(f'/image/{image_id}/coco')
        return json.loads(res.text)

    def get_annotation(self):
        """GET /annotation/
        Returns all annotations.
        """
        res = self._get('/annotation/')
        return json.loads(res.text)

    def get_annotation_(self, annotation_id):
        """GET /annotation/{annotation_id}
        Returns annotation by ID.
        """
        res = self._get(f'/annotation/{annotation_id}')
        return json.loads(res.text)

    def get_category(self):
        """GET 
        Returns all categories.
        """
        res = self._get('/category/')
        return json.loads(res.text)

    def get_category_data(self):
        """GET /category/data
        Endpoint called by category viewer client.
        """
        res = self._get('/category/data')
        return json.loads(res.text)

    def get_category_(self, category_id):
        """GET /category/{category_id}
        Returns all categories.
        """
        res = self._get(f'/category/{category_id}')
        return json.loads(res.text)

    def get_dataset(self):
        """GET /dataset/
        Returns all datasets.
        """
        res = self._get('/dataset/')
        return json.loads(res.text)

    def get_dataset_coco_import_(self, import_id):
        """GET /dataset/coco/{import_id}
        Returns current progress and errors of a coco import.
        """
        raise NotImplementedError
        res = self._get(f'/dataset/coco/{import_id}')
        return json.loads(res.text)

    def get_dataset_data(self):
        """GET /dataset/data
        Endpoint called by dataset viewer client.
        """
        res = self._get('/dataset/data')
        return json.loads(res.text)

    def get_dataset__coco(self, dataset_id):
        """GET /dataset/{dataset_id}/coco
        Returns coco of images and annotations in the dataset (only owners).
        """
        res = self._get(f'/dataset/{dataset_id}/coco')
        return json.loads(res.text)

    def get_dataset__data(self, dataset_id):
        """GET /dataset/{dataset_id}/data
        """
        res = self._get(f'/dataset/{dataset_id}/data')
        return json.loads(res.text)

    def get_dataset__export(self, dataset_id):
        """GET /dataset/{dataset_id}/export
        """
        res = self._get(f'/dataset/{dataset_id}/export')
        return json.loads(res.text)

    def get_dataset__exports(self, dataset_id):
        """GET /dataset/{dataset_id}/exports
        Returns exports of images and annotations in the dataset (only owners).
        """
        res = self._get(f'/dataset/{dataset_id}/exports')
        return json.loads(res.text)

    def get_dataset__reset_metadata(self, dataset_id):
        """GET /dataset/{dataset_id}/reset/metadata
        """
        res = self._get(f'/dataset/{dataset_id}/reset/metadata')
        return json.loads(res.text)

    def get_dataset__scan(self, dataset_id):
        """GET /dataset/{dataset_id}/scan
        """
        res = self._get(f'/dataset/{dataset_id}/scan')
        return json.loads(res.text)

    def get_dataset__stats(self, dataset_id):
        """GET /dataset/{dataset_id}/stats
        """
        res = self._get(f'/dataset/{dataset_id}/stats')
        return json.loads(res.text)

    def get_dataset__users(self, dataset_id):
        """GET /dataset/{dataset_id}/users
        """
        res = self._get(f'/dataset/{dataset_id}/users')
        return json.loads(res.text)

    def get_export_(self, export_id):
        """GET /export/{export_id}
        Returns exports"""
        res = self._get(f'/export/{export_id}')
        return json.loads(res.text)

    def get_export__download(self, export_id):
        """GET /export/{export_id}/download
        """
        res = self._get(f'/export/{export_id}/download')
        return json.loads(res.text)

    def get_tasks(self):
        """GET /tasks/
        Returns all tasks.
        """
        res = self._get('/tasks/')
        return json.loads(res.text)

    def get_tasks__logs(self, task_id):
        """GET /tasks/{task_id}/logs
        Returns all tasks.
        """
        res = self._get(f'/tasks/{task_id}/logs')
        return json.loads(res.text)

    def get_undo_list(self):
        """GET /undo/list/
        Returns all partially delete models.
        """
        res = self._get('/undo/list/')
        return json.loads(res.text)

    def get_admin_user_(self, username):
        """GET /admin/user/{username}
        Get a users.
        """
        res = self._get(f'/admin/user/{username}')
        return json.loads(res.text)

    def get_admin_users(self):
        """GET /admin/users
        Get list of all users.
        """
        res = self._get('/admin/users')
        return json.loads(res.text)

    def get_annotator_data_(self, image_id):
        """GET /annotator/data/{image_id}
        """
        res = self._get(f'/annotator/data/{image_id}')
        return json.loads(res.text)

    def post_user_login(self, username, password):
        """POST /user/login
        Logs user in.
        """
        params = {
            "username": username,
            "password": password,
        }
        res = self._post('/user/login', params)
        return json.loads(res.text)

    def post_user_password(self, password, email=None, name=None):
        """POST /user/password
        Set password of current user.
        """
        raise NotImplementedError
        params = {
            "password": password,
            "email": email,
            "name": name,
        }
        res = self._post('/user/password', params)
        return json.loads(res.text)

    def post_user_register(self, username, password, email=None, name=None):
        """POST /user/register 
        Creates user.
        """
        raise NotImplementedError
        params = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
        }
        res = self._post('/user/register', params)
        return json.loads(res.text)

    def post_image(self, image, folder=None):
        """/image/ 
        Creates an image.
        """
        raise NotImplementedError
        params = {
            "image": image,
            "folder": folder,
        }
        res = self._post('/image/', params)
        return json.loads(res.text)

    def post_image_copy___annotations(self, from_id, to_id, category_ids=None):
        """POST /image/copy/{from_id}/{to_id}/annotations
        """
        raise NotImplementedError
        params = {
            "category_ids": category_ids,
        }
        res = self._post(f'/image/copy/{from_id}/{to_id}/annotations', params)
        return json.loads(res.text)

    def post_annotation(self, image_id, category_id, isbbox, metadata, segmentation, keypoints, color):
        """POST /annotation/ 
        Creates an annotation.
        """
        raise NotImplementedError
        params = {
            "image_id": image_id,
            "category_id": category_id,
            "isbbox": isbbox,
            "metadata": metadata,
            "segmentation": segmentation,
            "keypoints": keypoints,
            "color": color,
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_category(self, name, supercategory, color, metadata, keypoint_edges, keypoint_labels, keypoint_colors):
        """POST /category/ 
        Creates a category.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset(self, name):
        """POST /dataset/ 
        Creates a dataset.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset_(self, dataset_id, categories, default_annotation_metadata):
        """POST /dataset/{dataset_id} 
        Updates dataset by ID.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset__coco(self, dataset_id, coco):
        """POST /dataset/{dataset_id}/coco 
        Adds coco formatted annotations to the dataset.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset__export(self, dataset_id, coco):
        """POST /dataset/{dataset_id}/export 
        Adds coco formatted annotations to the dataset.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset__generate(self, dataset_id, keywords, limit):
        """POST /dataset/{dataset_id}/generate 
        Adds images found on google to the dataset.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_dataset__share(self, dataset_id, users):
        """POST /dataset/{dataset_id}/share
        .
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_undo(self, id_, instance):
        """POST /undo/ 
        Undo a partial delete give id and instance.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_model_dextr_(self, image_id, points, padding, threshold):
        """POST /model/dextr/{image_id} 
        COCO data test.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_model_maskrcnn(self, image):
        """POST /model/maskrcnn 
        COCO data test.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_admin_user(self, username, password, email=None, name=None, isAdmin=None):
        """POST /admin/user/ 
        Create a new user.
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def post_annotator_data(self):
        """POST /annotator/data
        .
        """
        raise NotImplementedError
        params = {
        }
        res = self._post('', params)
        return json.loads(res.text)

    def delete_image_(self, image_id):
        """DELETE /image/{image_id}
        Deletes an image by ID.
        """
        raise NotImplementedError
        res = self._delete(f'/image/{image_id}')
        return json.loads(res.text)

    def delete_annotation_(self, annotation_id):
        """DELETE /annotation/{annotation_id}
        Deletes an annotation by ID.
        """
        raise NotImplementedError
        res = self._delete(f'/annotation/{annotation_id}')
        return json.loads(res.text)

    def delete_category_(self, category_id):
        """DELETE /category/{category_id}
        Deletes a category by ID.
        """
        raise NotImplementedError
        res = self._delete(f'/category/{category_id}')
        return json.loads(res.text)

    def delete_dataset_(self, dataset_id):
        """DELETE /dataset/{dataset_id}
        Deletes dataset by ID (only owners).
        """
        raise NotImplementedError
        res = self._delete(f'/dataset/{dataset_id}')
        return json.loads(res.text)

    def delete_export_(self, export_id):
        """DELETE /export/{export_id}
        """
        raise NotImplementedError
        res = self._delete(f'/export/{export_id}')
        return json.loads(res.text)

    def delete_task_(self, task_id):
        """DELETE /tasks/{task_id}
        Deletes task.
        """
        raise NotImplementedError
        res = self._delete(f'/tasks/{task_id}')
        return json.loads(res.text)

    def delete_undo(self):
        """DELETE /undo/
        Undo a partial delete give id and instance.
        """
        raise NotImplementedError
        res = self._delete('/undo/')
        return json.loads(res.text)

    def delete_admin_user_(self, username):
        """DELETE /admin/user/{username}
        Delete a user.
        """
        raise NotImplementedError
        res = self._delete(f'/admin/user/{username}')
        return json.loads(res.text)

    def put_annotation_(self, annotation_id, params):
        """PUT /annotation/{annotation_id}
        Updates an annotation by ID.
        """
        raise NotImplementedError
        params = {
            "category_id": None,
            "annotation_id": None,
        }
        res = self._put(f'/annotation/{annotation_id}', params)
        return json.loads(res.text)

    def put_category_(self, category_id, params):
        """PUT /category/{category_id}
        Updates a category name by ID.
        """
        raise NotImplementedError
        params = {
            "name": None,
            "supercategory": None,
            "color": None,
            "metadata": None,
            "keypoint_edges": None,
            "keypoint_labels": None,
            "keypoint_colors": None,
            "category_id": None,
        }
        res = self._put(f'/category/{category_id}', params)
        return json.loads(res.text)

    def patch_admin_user_(self, username):
        """PATCH /admin/user/{username}
        Edit a user.
        """
        raise NotImplementedError
        params = {
            "name": None,
            "password": None,
            "username": None,
        }
        res = self._patch(f'/admin/user/{username}', params)
        return json.loads(res.text)


if __name__ == '__main__':
    client = COCOAnnotatoryClient(address="127.0.0.1")
    info = client.get_info()
    print(info)
