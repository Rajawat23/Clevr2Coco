# Clevr2Coco
The repository is build to convert Clevr annotation file to COCO type.
The idea is to pre-process dataset for easier Object detection/Segmentation training experience.

COCO dataset format
```
{
    "images": [image],
    "annotations": [annotation],
    "categories": [category]
}


image = {
    "id": int,
    "width": int,
    "height": int,
    "file_name": str,
}

annotation = {
    "id": int,
    "image_id": int,
    "category_id": int,
    "segmentation": RLE or [polygon],
    "area": float,
    "bbox": [x,y,width,height],
    "iscrowd": 0 or 1,
}

categories = [{
    "id": int,
    "name": str,
    "supercategory": str,
}]
```

Thanks to authors at https://github.com/StanfordVL/ReferringRelationships for providing annotations.