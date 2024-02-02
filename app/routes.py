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
from flask import request, render_template

data_handler = GeoJSONAssistant()

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_input = request.form['input_place']
        user_input_geocoded = asyncio.run(get_location(user_input))
        if bool(user_input_geocoded) is True:
            data_handler.add_record(user_input_geocoded)
        else:
            pass
    geojson = data_handler.get_data_as_json()
    counts = data_handler.count_places_countries()
    return render_template('index.html', geojsonfile=geojson, places=counts[0], countries=counts[1])