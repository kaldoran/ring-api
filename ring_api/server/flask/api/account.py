#
# Copyright (C) 2016 Savoir-faire Linux Inc
#
# Authors:  Seva Ivanov <seva.ivanov@savoirfairelinux.com>
#           Simon Zeni  <simon.zeni@savoirfairelinux.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
#

from flask import jsonify, request
from flask_restful import Resource

from ring_api.server.flask import utils

class Account(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        data = request.args
        if (not data):
            return jsonify({
                'status': 404,
                'message': 'data not found'
            })

        elif ('type' not in data):
            return jsonify({
                'status': 404,
                'message': 'type not found in data'
            })

        account_template = None
        account_types = ['SIP', 'IAX', 'IP2P', 'RING']
        account_type = data.get('type')

        if (account_type in account_types):
            return jsonify({
                'status': 200,
                'details': self.dring.config.get_account_template(account_type)
            })

        return jsonify({
            'status': 400,
            'message': 'wrong account type'
        })

    def post(self):
        data = request.get_json(force=True)

        if (not 'details' in data):
            return jsonify({
                'status': 400,
                'message': 'details not found in request data'
            })

        return jsonify({
            'status': 200,
            'account_id': self.dring.config.add_account(data['details'])
        })

class Accounts(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self):
        return jsonify({
            'status': 200,
            'accounts': self.dring.config.accounts()
        })

    def delete(self, account_id):
        self.dring.config.remove_account(account_id)

        return jsonify({
            'status': 200,
            'accounts': self.dring.config.accounts()
        })

class AccountsDetails(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, account_id):
        data = request.args

        if (not data):
            return jsonify({
                'status': 404,
                'message': 'data not found'
            })

        elif ('type' not in data):
            return jsonify({
                'status': 404,
                'message': 'type not found in data'
            })

        account_type = data.get('type')

        if (account_type == 'default'):
            return jsonify({
                'status': 200,
                'details': self.dring.config.account_details(account_id)
            })

        elif (account_type == 'volatile'):
            pass

        return jsonify({
            'status': 400,
            'message': 'wrong account type'
        })

class AccountsCodecs(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, account_id, codec_id=None):
        if (codec_id):
            return jsonify({
                'status': 200,
                'details': self.dring.config.get_codec_details(
                    account_id, int(codec_id))
            })

        return jsonify({
            'status': 200,
            'details': self.dring.config.get_active_codec_list(account_id)
        })

    def put(self, account_id, codec_id=None):
        data = request.get_json(force=True)

        if (codec_id):
            self.dring.config.set_codec_details(
                account_id, int(codec_id), data['details'])

            return jsonify({
                'status': 200,
                'details': self.dring.config.get_codec_details(
                    account_id, int(codec_id))
            })

        self.dring.config.set_active_codec_list(
                account_id, codec_id, data['list'])

        return jsonify({
            'status': 200,
            'details': self.dring.config.get_active_codec_list(account_id)
        })


class AccountsCall(Resource):
    def __init__(self, dring):
        self.dring = dring

    def post(self, account_id):
        if (not utils.valid_account_format(account_id)):
            return jsonify({
                'status': 400,
                'message': 'account_id not valid'
            })

        accounts = self.dring.config.accounts()

        if (not utils.contained_in(account_id, accounts)):
            return jsonify({
                'status': 400,
                'message': 'account not found'
            })

        data = request.get_json(force=True) # FIXME remove json

        if (not 'ring_id' in data):
            return jsonify({
                'status': 400,
                'message': 'ring_id not found in request data'
            })

        return jsonify({
            'status': 200,
            'call_id': self.dring.call.place_call(account_id, data['ring_id'])
        })

class AccountsCertificates(Resource):
    def __init__(self, dring):
        self.dring = dring

    def get(self, account_id, cert_id):
        # FIXME not tested
        data = request.args

        if (not data):
            return jsonify({
                'status': 404,
                'message': 'data not found'
            })

        elif ('type' not in data):
            return jsonify({
                'status': 404,
                'message': 'type not found in data'
            })

        action = data.get('type')

        if (action == 'validate'):
            certificates = self.dring.config.validate_certificate(
                account_id, cert_id
            )
            return jsonify({
                'status': 200,
                'certificates': certificates
            })

        return jsonify({
            'status': 400,
            'message': 'wrong account type'
        })

    def put(self, account_id, cert_id):
        # FIXME not tested
        data = request.args

        if (not data):
            return jsonify({
                'status': 404,
                'message': 'data not found'
            })

        elif ('status' not in data):
            return jsonify({
                'status': 404,
                'message': 'status not found in data'
            })

        cert_states = ["UNDEFINED", "ALLOWED", "BANNED"]
        cert_state = data.get('type')

        if (not cert_state in cert_states):
            success = self.dring.config.set_certificate_status(
                    account_id, cert_id, status
            )
            return jsonify({
                'status': 200,
                'success': success
            })

        return jsonify({
            'status': 400,
            'message': 'wrong status type'
        })

class AccountsMessage(Resource):
    def __init__(self, dring):
        self.dring = dring

    def post(self, account_id):

        data = request.args
        ring_id = data.get('ring_id')
        mime_type = data.get('mime_type')
        message = data.get('message')

        if (not (ring_id and mime_type and message)):
            return jsonify({
                'status': 400,
                'message': 'required post data not found'
            })

        message_id = self.dring.config.send_account_message(
            account_id, ring_id, {mime_type: message})

        return jsonify({
            'status': 200,
            'message_id': message_id
        })

