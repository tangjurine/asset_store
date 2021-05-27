import flask
from flask import request, jsonify

import asset_util
import math

def create_app():
    app = flask.Flask(__name__)

    asset_names_to_idx = {}
    assets = []
    page_limit = 5

    def number_of_pages():
        return int(math.ceil(len(assets) / page_limit))

    def decompress_assets(assets):
        return [asset_util.decompress_asset(asset[0], asset[1]) for asset in assets]

    @app.route('/', methods=['GET'])
    def get_all():
        if len(assets) <= page_limit:
            return jsonify(decompress_assets(assets))
        else:
            return 'cannot retrieve all assets at once, use endpoint /page/<page number> , 0-indexed', 413

    @app.route('/page/<int:idx>', methods=['GET'])
    def get_page(idx):
        try:
            if idx >= number_of_pages():
                raise IndexError
            assets_slice = assets[idx*page_limit:(idx+1)*page_limit]
        except IndexError:
            return 'invalid query parameter: page', 400
        return jsonify({
            'current_page': idx,
            'total_pages': number_of_pages(),
            'assets': decompress_assets(assets_slice)
        })

    @app.route('/add', methods=['POST'])
    def create_asset():
        if not asset_util.validate_asset(request.json):
            return 'invalid asset', 400
        if request.json['name'] in asset_names_to_idx:
            return 'name of asset already exists', 400
        asset = request.json
        assets.append((asset['name'], asset_util.compress_asset(asset)))
        asset_names_to_idx[asset['name']] = len(assets) - 1
        return '', 201

    @app.route('/name/<name>', methods=['GET'])
    def get(name):
        try:
            idx = asset_names_to_idx[name]
            asset = asset_util.decompress_asset(*assets[idx])
        except KeyError:
            return 'name not found', 404
        return jsonify(asset)

    if __name__ == '__main__':
        app.run()
    else:
        app.config["DEBUG"] = True

    return app