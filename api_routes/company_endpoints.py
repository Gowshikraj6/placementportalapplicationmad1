from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.company_impl import AdminImpl


company_api = Blueprint("company_api", __name__)