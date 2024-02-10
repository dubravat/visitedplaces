# -*- coding: utf-8 -*-
"""
/***************************************************************************
    py file: routes.py
    ---------------------------------------
    Date                 : 01-Jan-2024
    Copyright            : (c) Taras Dubrava
    Email                :
 ***************************************************************************
 *                                                                         *
 *                          Visited Places App                             *
 *                                                                         *
 ***************************************************************************/
"""

# imports
import asyncio
from app import app
from app.locgeoproc import get_location
from app.geojsonproc import GeoJSONAssistant
from flask import request, redirect, url_for, render_template

data_handler = GeoJSONAssistant()


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_input = request.form.get('input_place')
        if bool(user_input) is True:
            user_input_geocoded = asyncio.run(get_location(user_input))
            if bool(user_input_geocoded) is True and not(user_input_geocoded['place'] in data_handler.get_all_places()) is True:
                data_handler.add_place(user_input_geocoded)
            else:  # TODO
                pass
        # TODO
        if request.form['del_last_place'] == 'Delete the last place':
            data_handler.remove_last_place()
        redirect(url_for('index'))

    geojson = data_handler.get_geojson_as_string()
    counts = data_handler.count_places_countries()
    return render_template(template_name_or_list='index.html', geojsonfile=geojson, places=counts[0], countries=counts[1])
