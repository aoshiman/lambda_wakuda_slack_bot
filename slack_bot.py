# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals
import random
from random import SystemRandom
from string import ascii_lowercase, digits
import boto3
from settings import config as cfg


def _random(farm):
    return random.choice(farm)


def _create_anchor(image):
    return image + '#' +  ''.join(SystemRandom().choice(digits+ascii_lowercase) for i in xrange(20))


def get_image_list(bucket, key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)
    obj = obj.get()
    body = obj['Body'].read()
    return (body.decode('utf-8').split(','))


def lambda_handler(event, context):
    if not event['token'] == cfg['SLACK_TOKEN']:
        return ""
    msg = _create_anchor(_random(get_image_list(cfg['BUCKET'], cfg['KEY'])))
    payload = {"text": msg}

    return payload


if __name__ == '__main__':
    image = _random(get_image_list(cfg['BUCKET'], cfg['KEY']))
    print(_create_anchor(image))
    post_image(_create_anchor(image))
