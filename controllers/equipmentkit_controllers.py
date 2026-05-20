from flask import request, jsonify
from db import execute
from errors import ERRORS


def listar_kit_equipamientos():
