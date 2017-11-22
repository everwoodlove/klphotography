from __future__ import unicode_literals
from datetime import *
from PIL import Image
from django.shortcuts import render
from klphotography import settings
import requests
import json
import urllib2 as urllib
import io
from collections import namedtuple

categories = {'pets', 'portraits', 'automotive', 'misc', 'weddings'}

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
    # Build URL from params
    # get all images in the folder, including in the preview folder
    # return them

    #TODO
    url = settings.STATIC_URL + '/website/photos/' + category + '/' + date + '/' + name

    landscapes, portraits = get_all_photos(url)
    landscape_photos = []
    portrait_photos = []

    for photo in landscapes:
        photo = photo.replace('/static/', '')
        landscape_photos.append(photo)

    for photo in portraits:
        photo = photo.replace('/static/', '')
        portrait_photos.append(photo)

    context = {'landscapes': landscape_photos, 'portraits': portrait_photos}

    return render(request, 'website/shoot.html', context)

def gallery(request, category):
    url = 'website/gallery/'

    for cat in categories:
        if category == cat:
            url += cat + '.html'
            break

    context = {'photos': get_preview_photos_from(category, 3)}

    return render(request, url, context)

# Its ideal to have landscape photos be the full images
# and portraits to be the half images
# But what if we only have 1 portrait and 2 landscapes?

#TODO for home photos:
# parse through all directories and get most recent 6-7 shoots to display and pick first image of each in the preview folder
# def get_homepage_photos():
#     homepage_photos = []
#     i = 0
#
#     for category in categories:
#         photo_set = get_preview_photos(category, 7)
#         for photo in photo_set:
#             if i == 0:
#                 name = 'landscapes'
#             else:
#                 name = 'portraits'
#
#             if photo.get(name, []):
#                 date = photo.get('date', '')
#                 date_split = date.split('.')
#
#                 if (len(date_split) is 3):
#                     day = date_split[1]
#                     month = date_split[0]
#                     year = date_split[2]
#                 else:
#                     day = ''
#                     month = ''
#                     year = ''
#
#                 shoot_photo = {'name': photo.get('name', ''), 'day': day, 'month': month, 'year': year,
#                                'photo': photo.get(name, [''])[0],
#                                'category': photo.get('category', ''), 'number': i}
#                 i += 1
#
#                 if i > 2:
#                     i = 0
#
#                 homepage_photos.append(shoot_photo)
#
#     return homepage_photos

# def get_preview_photos(category, list_length):
#     #string = 'website/photos/' + category
#     original_path = os.path.join(settings.STATIC_ROOT, 'app/a.txt')
#     #os.path.join(static(string))
#     print original_path
#     dates_directories = get_most_recent_folders_by_date(original_path)
#     photos_to_return = []
#
#     if dates_directories:
#         for date in dates_directories:
#             folder_path = original_path + '/' + date
#             shoot_name_directories = os.listdir(folder_path)
#
#             for shoot_name in shoot_name_directories:
#                 path = folder_path + '/' + shoot_name + '/preview'
#                 preview_photos = get_images(path)
#
#                 landscapes, portraits = sort_images(preview_photos)
#
#                 photo_set = {'name': shoot_name, 'date': date, 'landscapes': landscapes, 'portraits': portraits, 'category': category}
#                 photos_to_return.append(photo_set)
#
#                 if len(photos_to_return) > list_length:
#                     break
#
#             if len(photos_to_return) > list_length:
#                 break
#
#     return photos_to_return
#
# def get_all_photos(path):
#     photo_set = []
#
#     if os.path.isdir(path):
#         photos = get_images(path)
#         photo_set = photo_set + photos
#
#     path = path + '/preview'
#
#     if os.path.isdir(path):
#         photos = get_images(path)
#         photo_set = photo_set + photos
#
#     landscapes, portraits = sort_images(photo_set)
#
#     return landscapes, portraits
#
# def get_most_recent_folders_by_date(path):
#     if os.path.isdir(path):
#         directory_names = os.listdir(path)
#
#         dates_list = []
#
#         for name in directory_names:
#             date_split = name.split('.')
#
#             if (len(date_split) is 3):
#                 folderDate = datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]))
#                 dates_list.append(folderDate)
#
#         folders_to_use = []
#         now = datetime.today()
#
#         list_length = len(dates_list)
#
#
#         for i in xrange(list_length):
#             youngest = max(dt for dt in dates_list if dt < now)
#
#             folders_to_use.append(youngest)
#             dates_list.remove(youngest)
#
#         folders = []
#
#         for i in xrange(list_length):
#             folders.append(folders_to_use[i].strftime('%m.%d.%Y'))
#
#         return folders
#     else:
#         return []
#
# def get_images(path):
#     photos = []
#
#     only_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
#     for file in only_files:
#         if file.endswith(".png") or file.endswith(".jpg"):
#             photo_path = os.path.join(path, file)
#             photos.append(photo_path)
#
#     return photos
#
# def sort_images(images_list):
#     landscapes = []
#     portraits = []
#
#     for image in images_list:
#         im = Image.open(image)
#         width, height = im.size
#
#         # TODO remove this line when going to prod
#         image = image.replace('/static/', '')
#         if width > height:
#             landscapes.append(image)
#         else:
#             portraits.append(image)
#
#     return landscapes, portraits












# This gets 7 photo shoots worth of preview photos to display on the homepage.
# The list returned should be a list of objects that contain the photo's shoot name,
# category, date (in day/month/year separately), url, and number.

def get_homepage_photos_from_git():
    homepage_photos = []

    preview_photos = get_newest_preview_photoshoot_photos_from_git()
    photo_metadata = build_photo_information(preview_photos)
    homepage_photos.append(photo_metadata)

    landscape_photos, portrait_photos = sort_photos_by_aspect(homepage_photos)
    sorted_photos = {'landscapes': landscape_photos, 'portraits': portrait_photos}

    homepage_photos = assign_numbers_to_photos(sorted_photos)

    return homepage_photos


# This builds the photo's information to be returned as an object containing
# shoot name, date, category, and whether the image is landscape or portrait style
def build_photo_information(photo):
    photo_metadata = {}

    if photo:
        shoot_name, shoot_date, category = parse_photo_path(photo)
        orientation = determine_photo_orientation() #TODO

        photo_metadata['shoot_name'] = shoot_name
        photo_metadata['shoot_date'] = shoot_date
        photo_metadata['category'] = category
        photo_metadata['orientation'] = orientation
        photo_metadata['url'] = photo.url

    return photo_metadata


# This will take the list of photos, count how many are in each category
# (portrait or landscape) and then assign them a number based on those counts
# 0 = full width, can only be landscape
# 1 = half width, landscape or portrait
# 2 = half width, landscape or portrait
def assign_numbers_to_photos(photo_list):
    i = 0
    assigned_photos = []

    for photo in photo_list:
        if i == 0:
            orientation_type = 'landscapes'
        else:
            orientation_type = 'portraits'

        if photo.get(orientation_type, []):
            photo['block'] = i
            i += 1

            if i > 2:
                i = 0

            assigned_photos.append(photo)

    return assigned_photos


# This parses the path on the photo object to get the name, date,
# and category of the shoot
def parse_photo_path(photo):
    path_separated = photo.path.split('/')

    shoot_name = path_separated[1]
    shoot_date = path_separated[2].split('.')
    shoot_category = path_separated[0]

    return shoot_name, shoot_date, shoot_category


# This will open the image and look at its dimensions
# to determine if the image is portrait style or landscape style
# in terms of its orientation.
def determine_photo_orientation(photo):
    file_data = urllib.urlopen(photo.url)
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
def get_newest_preview_photoshoot_photos_from_git():
    repo = 'kl-photography-media'
    owner = 'everwoodlove'
    photos_to_return = []

    # 5 categories will return a max of 15 photo shoots
    max_photoshoots_per_category = 3

    for category in categories:
        get_url = 'https://api.github.com/repos/' + owner + '/' + repo + '/contents/' + category + '/'

        repo_contents_array = requests.get(get_url)
        photo_date_directories = parse_json_array(repo_contents_array, 'dir')

        newest_photoshoot_dates = get_newest_dates(photo_date_directories, max_photoshoots_per_category)

        if newest_photoshoot_dates:
            for date in newest_photoshoot_dates:
                photoshoot_get_url = get_url + date + '/'
                photoshoot_directories = requests.get(photoshoot_get_url)
                photoshoot_directories = parse_json_array(photoshoot_directories, 'dir')

                # Get all the photoshoots for that date
                # And get all the preview photos for those photoshoots
                for photo_shoot in photoshoot_directories:
                    preview_photos_json = requests.get(photoshoot_get_url + photo_shoot.name + '/preview')
                    preview_photos = parse_json_array(preview_photos_json, 'file')

                    photos_to_return.append(preview_photos)


    return photos_to_return


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
    # Want to determine portrait/landscape
    # assign to portrait or landscape list on the
    landscape_photos = []
    portrait_photos = []

    for photo in photo_list:
        if photo.orientation == 'landscape':
            landscape_photos.append(photo)
        else:
            portrait_photos.append(photo)

    return landscape_photos, portrait_photos


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def parse_json_array(json_array, selector_type):
    array = []

    for json in json_array:
        object = json2obj(json)

        if selector_type:
            if object.type == selector_type:
                array.append(object)
        else:
            array.append(object)

    return array


