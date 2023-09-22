import qrcode
from PIL import Image
import tempfile

from config.env import config
from config.aws_config import s3_client

TEMP_DIR = tempfile.mkdtemp()


def get_ticket_object_key(event_id: str, store_file=False):
    return f'tickets{"-" if store_file else "/"}{event_id}'


def get_evite_object_key(evite_id: str, store_file=False):
    return f'evites{"-" if store_file else "/"}{evite_id}.png'


def get_value_from_string(size: str, ref_value: float):
    if size.rfind('%') != -1:
        arr = size.split('%')
        return round((float(arr[0]) / 100) * ref_value)
    else:
        return int(size)


def get_ticket_url(event_id: str, evite_id: str, ticket_meta):
    """ Make sure to delete the files in temp dir later, don't saturate container """
    file_path = f'{TEMP_DIR}/{get_ticket_object_key(event_id, True)}'
    s3_client.download_file(
        Bucket=config['bucket_name'], Key=get_ticket_object_key(event_id), Filename=file_path
    )

    file_dest_path = f'{TEMP_DIR}/{get_evite_object_key(event_id, True)}'
    compose_data_as_qr_on_image(evite_id, file_path, file_dest_path, ticket_meta)

    s3_client.upload_file(
        Filename=file_dest_path,
        Bucket=config['bucket_name'],
        Key=get_evite_object_key(evite_id),
        ExtraArgs={'ContentType': 'image/png'}
    )

    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': config['bucket_name'], 'Key': get_evite_object_key(evite_id)},
        ExpiresIn=60 * 60  # 60 minutes (secs)
    )


def compose_data_as_qr_on_image(data: str, file_path: str, file_dest_path: str, ticket_meta):
    img_bg = Image.open(file_path)
    qr = qrcode.QRCode(box_size=4)
    qr.add_data(data)

    qr.make()
    img_qr = qr.make_image()

    # resize the image to new size
    new_size = get_value_from_string(ticket_meta.qrSize, img_bg.size[1])

    img_qr = img_qr.resize((new_size, new_size), Image.Resampling.LANCZOS)

    # determine pasting position from height of flyer and qr code
    img_bg.paste(img_qr, (
        (get_value_from_string(ticket_meta.qrPositionX, img_bg.size[0])),
        get_value_from_string(ticket_meta.qrPositionY, img_bg.size[1]))
                 )

    img_bg.save(file_dest_path)
