import qrcode
from PIL import Image
import tempfile

from config.env import config
from config.minio_config import minio_client


def get_ticket_object_key(event_id: str):
    return f'tickets/{event_id}'


def get_evite_object_key(evite_id: str):
    return f'evites/{evite_id}.png'


def get_value_from_string(size: str, ref_value: float):
    if size.find('%'):
        arr = size.split('%')
        return round((float(arr[0]) / 100) * ref_value)
    else:
        return int(size)


def get_ticket_url(event_id: str, evite_id: str, ticket_meta):
    file_path = f'{tempfile.tempdir}/{get_ticket_object_key(event_id)}'
    minio_client.fget_object(
        bucket_name=config.env.config['bucket_name'], object_name=get_ticket_object_key(event_id), file_path=file_path
    )

    file_dest_path = f'{tempfile.tempdir}/{get_evite_object_key(event_id)}'
    compose_data_as_qr_on_image(evite_id, file_path, file_dest_path, ticket_meta)

    minio_client.fput_object(
        bucket_name=config.env.config['bucket_name'],
        object_name=get_evite_object_key(evite_id),
        file_path=file_dest_path,
        content_type='image/png'
    )

    return minio_client.presigned_get_object(
        bucket_name=config.env.config['bucket_name'],
        object_name=get_evite_object_key(evite_id),
    )


def compose_data_as_qr_on_image(data: str, file_path: str, file_dest_path: str, ticket_meta):
    img_bg = Image.open(file_path)
    qr = qrcode.QRCode(box_size=4)
    qr.add_data(data)

    qr.make()
    img_qr = qr.make_image()

    # resize the image to new size
    new_size = get_value_from_string(ticket_meta['qrSize'], img_bg.size[1])

    img_qr = img_qr.resize((new_size, new_size), Image.Resampling.LANCZOS)

    # determine pasting position from height of flyer and qr code
    img_bg.paste(img_qr, (
        (get_value_from_string(ticket_meta['qrPositionX'], img_bg.size[0])),
        get_value_from_string(ticket_meta['qrPositionY'], img_bg.size[1]))
                 )

    img_bg.save(file_dest_path)
