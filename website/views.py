from __future__ import unicode_literals
from datetime import *
from PIL import Image
from django.shortcuts import render
import requests
import json as JSON
import urllib2 as urllib
import io
from collections import namedtuple
from django.core.cache import cache
from copy import copy

CATEGORIES = {'pets', 'portraits', 'automotive', 'misc', 'weddings'}

REPO = 'kl-photography-media'
OWNER = 'everwoodlove'

BASE_URL = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/'


def home(request):
    photos = get_homepage_photos_from_git()
    if photos:
        context = {'photos': photos}
    else:
        context = {}

    return render(request, 'website/home.html', context)


def pricing(request):
    return render(request, 'website/pricing.html')


def about(request):
    return render(request, 'website/about-me.html')


def contact(request):
    return render(request, 'website/contact.html')


def shoot(request, category, date, name):
    url = BASE_URL + category + '/' + date + '/' + name

    all_photos = get_all_photoshoot_photos(url)

    photos_to_use = []

    for photo in all_photos:
        photo_metadata = build_photo_information(photo)
        photos_to_use.append(photo_metadata)

    context = {'photos': photos_to_use}

    return render(request, 'website/shoot.html', context)


def gallery(request, category):
    url = 'website/gallery/'

    for cat in CATEGORIES:
        if category == cat:
            url += cat + '.html'
            break

    photos = get_newest_photoshoot_photos_from_git(category_given=category)
    total_photos = []

    if photos:
        for photo in photos:
            photo_metadata = build_photo_information(photo)
            total_photos.append(photo_metadata)

        total_photos = assign_numbers_to_photos(total_photos)

    context = {'photos': total_photos}

    return render(request, url, context)


def get_homepage_photos_from_git():
    homepage_photos = []

    preview_photos = get_newest_photoshoot_photos_from_git(only_get_preview_photos=True)

    if preview_photos:
        for photo in preview_photos:
            photo_metadata = build_photo_information(photo)
            homepage_photos.append(photo_metadata)

        homepage_photos = assign_numbers_to_photos(homepage_photos)

    return homepage_photos


# This builds the photo's information to be returned as an object containing
# shoot name, date, category, and whether the image is landscape or portrait style
def build_photo_information(photo):
    photo_metadata = {}

    if photo:
        shoot_name, shoot_date, category = parse_photo_path(photo)
        orientation = determine_photo_orientation(photo)

        # photo_metadata['shoot_name'] = shoot_name
        # photo_metadata['shoot_date'] = shoot_date
        # photo_metadata['category'] = category
        # photo_metadata['orientation'] = orientation
        # photo_metadata['url'] = photo.downloadurl

        photo_metadata = {
            'shoot_name': shoot_name,
            'shoot_date': shoot_date,
            'category': category,
            'orientation': orientation,
            'url': photo.downloadurl
        }

    return photo_metadata


# This will take the list of photos, count how many are in each category
# (portrait or landscape) and then assign them a number based on those counts
# 0 = full width, can only be landscape
# 1 = half width, landscape or portrait
# 2 = half width, landscape or portrait
def assign_numbers_to_photos(photo_list):
    i = 0
    landscape_list_index = 0
    portrait_list_index = 0

    list_length = 10

    landscape_photos, portrait_photos = sort_photos_by_aspect(photo_list)

    landscape_length = len(landscape_photos)
    portrait_length = len(portrait_photos)

    assigned_photos = []

    for x in xrange(list_length):
        if i == 0:
            if landscape_list_index < landscape_length:
                new_photo = copy(landscape_photos[landscape_list_index])
                landscape_list_index += 1
                new_photo['block'] = i
                assigned_photos.append(new_photo)
                i += 1
        elif i == 1 or i == 2:
            if portrait_list_index < portrait_length:
                new_photo = copy(portrait_photos[portrait_list_index])
                new_photo['block'] = i
                assigned_photos.append(new_photo)

                i += 1

                if i > 2:
                    i = 0

    return assigned_photos


# This parses the path on the photo object to get the name, date,
# and category of the shoot
def parse_photo_path(photo):
    path_separated = photo.path.split('/')

    shoot_name = path_separated[2]
    shoot_date = path_separated[1]
    shoot_category = path_separated[0]

    return shoot_name, shoot_date, shoot_category


# This will open the image and look at its dimensions
# to determine if the image is portrait style or landscape style
# in terms of its orientation.
def determine_photo_orientation(photo):
    file_data = urllib.urlopen(photo.downloadurl)
    image_file = io.BytesIO(file_data.read())
    image = Image.open(image_file)
    width, height = image.size

    if width > height:
        return 'landscape'
    else:
        return 'portrait'


# This returns a list of the most recent preview photos per category.
# It is a list of preview photos from the most recent photoshoots
# The number of photoshoots looked at is determined by "list_length"
# The category the photoshoots are pulled from is determined by "category"
def get_newest_photoshoot_photos_from_git(category_given = None, only_get_preview_photos = False):
    photos_to_return = []

    # 5 categories will return a max of 15 photo shoots
    max_photoshoots_per_category = 3

    categories_to_use = CATEGORIES

    if category_given:
        categories_to_use = [category_given]

    for category in categories_to_use:
        get_url = BASE_URL + category + '/'

        repo_contents_array = get_api_call_contents(get_url)
        photo_date_directories = parse_json_array(repo_contents_array, 'dir')

        newest_photoshoot_dates = get_newest_dates(photo_date_directories, max_photoshoots_per_category)

        if newest_photoshoot_dates:
            for date in newest_photoshoot_dates:
                photoshoot_get_url = get_url + date + '/'
                photoshoot_directories = get_api_call_contents(photoshoot_get_url)
                photoshoot_directories = parse_json_array(photoshoot_directories, 'dir')

                # Get all the photoshoots for that date
                # And get all the preview photos for those photoshoots
                for photo_shoot in photoshoot_directories:
                    preview_photos_json = get_api_call_contents(photoshoot_get_url + photo_shoot.name + '/preview')
                    preview_photos = parse_json_array(preview_photos_json, 'file', '.jpg')

                    regular_photos_json = get_api_call_contents(photoshoot_get_url + photo_shoot.name)
                    regular_photos = parse_json_array(regular_photos_json, 'file', '.jpg')

                    if only_get_preview_photos:
                        photos_to_return  = photos_to_return + preview_photos
                    else:
                        photos_to_return = photos_to_return + preview_photos + regular_photos

    return photos_to_return


def get_all_photoshoot_photos(url):
    photoshoot_photos = get_api_call_contents(url)
    preview_photoshoot_photos = get_api_call_contents(url+ '/preview')

    regular_photos = parse_json_array(photoshoot_photos, 'file', '.jpg')
    preview_photos = parse_json_array(preview_photoshoot_photos, 'file', '.jpg')

    return regular_photos + preview_photos


# This function returns a list of date strings for the newest dates
# From the list of dated folders it is given.
def get_newest_dates(dated_folder_objects, max_folders):
    newest_directories = []
    dates_list = []


    for folder in dated_folder_objects:
        if len(newest_directories) < max_folders:
            directory_path = folder.path
            directory_path = directory_path.split('/')

            # Per static directory structure, the path should always look like this:
            # Category/Shoot date/Shoot name/photos + preview/photos
            date = directory_path[1]
            date = date.split('.')

            if len(date) is 3:
                folderDate = datetime(int(date[2]), int(date[0]), int(date[1]))
                dates_list.append(folderDate)

    now = datetime.today()
    dates_length = len(dates_list)

    for i in xrange(dates_length):
        newest = max(dt for dt in dates_list if dt < now)

        newest_directories.append(newest)
        dates_list.remove(newest)

    # We now have the list of te newest directories by date object, cut by max_folders
    newest_directories = newest_directories[:max_folders]
    dates_list = newest_directories
    newest_directories = []

    for date in dates_list:
        newest_directories.append(date.strftime('%m.%d.%Y'))

    return newest_directories


def sort_photos_by_aspect(photo_list):
    landscape_photos = []
    portrait_photos = []

    for photo in photo_list:
        type = photo.get('orientation')
        if str(type) == 'landscape':
            landscape_photos.append(photo)
        else:
            portrait_photos.append(photo)

    return landscape_photos, portrait_photos


def _json_object_hook(d):
    for key in d.keys():
        new_key = key.replace("_", "")
        if new_key != key:
            d[new_key] = d[key]
            del d[key]

    return namedtuple('X', d.keys())(*d.values())


def parse_json_array(json_array, selector_type = None, name_filter = None):
    array = []
    json_array = JSON.loads(json_array, object_hook=_json_object_hook)

    try:
        for json in json_array:
            if selector_type:
                if json.type and json.type == selector_type:
                    if name_filter:
                        if name_filter in json.name:
                            array.append(json)
                    else:
                        array.append(json)
            else:
                array.append(json)
    except:
        print 'An error occurred and the JSON could not be parsed.'
        print json_array

    return array


def get_api_call_contents(url):
    value = cache.get(url)

    if value:
        return value
    else:
        # TODO do not deploy this!!!!!!
        new_value = requests.get(url, auth=('everwoodlove', '0536d49d6cbd886beeede42c08c19725036f9362')).content
        cache.set(url, new_value)

        return new_value


def get_from_cache(key):
    return cache.get(key)


def set_in_cache(key, value):
    cache.set(key, value)




